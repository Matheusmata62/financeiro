"""
Fase 2: Banco de Dados e Histórico

Gerenciador SQLite para:
- Registrar financiamentos
- Histórico de parcelas pagas
- Aportes extras (amortização acelerada)
- Entradas extras (lucros de revenda)
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import asdict
from decimal import Decimal

from src.amortizacao import PlanoAmortizacao, Parcela


DB_PATH = Path(__file__).parent.parent / "data" / "financiamentos.db"


class GerenciadorBancoDados:
    """Gerencia o banco de dados SQLite de financiamentos"""
    
    def __init__(self, db_path: Path = DB_PATH):
        """Inicializa conexão com banco de dados"""
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._criar_tabelas()
    
    def _conexao(self) -> sqlite3.Connection:
        """Cria conexão com banco de dados"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
        return conn
    
    def _criar_tabelas(self):
        """Cria tabelas se não existirem"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        # Tabela de financiamentos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financiamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                saldo_inicial REAL NOT NULL,
                saldo_atual REAL NOT NULL,
                taxa_mensal REAL NOT NULL,
                parcela_fixa REAL NOT NULL,
                data_inicio DATE NOT NULL,
                data_quitacao_estimada DATE,
                ativo BOOLEAN DEFAULT 1,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de parcelas pagas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parcelas_pagas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                financiamento_id INTEGER NOT NULL,
                numero_parcela INTEGER NOT NULL,
                data_pagamento DATE NOT NULL,
                valor_parcela REAL NOT NULL,
                juros REAL NOT NULL,
                principal REAL NOT NULL,
                saldo_anterior REAL NOT NULL,
                saldo_posterior REAL NOT NULL,
                FOREIGN KEY(financiamento_id) REFERENCES financiamentos(id)
            )
        """)
        
        # Tabela de aportes extras
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS aportes_extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                financiamento_id INTEGER NOT NULL,
                numero_parcela INTEGER NOT NULL,
                data_aporte DATE NOT NULL,
                valor_aporte REAL NOT NULL,
                origem TEXT,  -- 'revenda', 'salario', 'bonus', etc
                descricao TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(financiamento_id) REFERENCES financiamentos(id)
            )
        """)
        
        # Tabela de entradas extras (receitas de revenda)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entradas_extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                financiamento_id INTEGER NOT NULL,
                data_entrada DATE NOT NULL,
                valor REAL NOT NULL,
                descricao TEXT,
                produto_vendido TEXT,
                alocado_para_aporte BOOLEAN DEFAULT 0,
                aporte_id INTEGER,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(financiamento_id) REFERENCES financiamentos(id),
                FOREIGN KEY(aporte_id) REFERENCES aportes_extras(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    # ============= FINANCIAMENTOS =============
    
    def criar_financiamento(self, nome: str, saldo_inicial: float, 
                           taxa_mensal: float, parcela_fixa: float,
                           descricao: Optional[str] = None) -> int:
        """
        Cria um novo financiamento
        
        Returns:
            ID do financiamento criado
        """
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO financiamentos 
            (nome, descricao, saldo_inicial, saldo_atual, taxa_mensal, 
             parcela_fixa, data_inicio)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, descricao, saldo_inicial, saldo_inicial, 
              taxa_mensal, parcela_fixa, datetime.now().date()))
        
        conn.commit()
        financiamento_id = cursor.lastrowid
        conn.close()
        
        return financiamento_id
    
    def obter_financiamento(self, financiamento_id: int) -> Optional[Dict]:
        """Obtém um financiamento específico"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM financiamentos WHERE id = ?", 
                      (financiamento_id,))
        resultado = cursor.fetchone()
        conn.close()
        
        return dict(resultado) if resultado else None
    
    def listar_financiamentos(self, apenas_ativos: bool = True) -> List[Dict]:
        """Lista todos os financiamentos"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        if apenas_ativos:
            cursor.execute("SELECT * FROM financiamentos WHERE ativo = 1")
        else:
            cursor.execute("SELECT * FROM financiamentos")
        
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in resultados]
    
    def atualizar_saldo_financiamento(self, financiamento_id: int, 
                                     novo_saldo: float):
        """Atualiza o saldo atual de um financiamento"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE financiamentos 
            SET saldo_atual = ?, atualizado_em = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (novo_saldo, financiamento_id))
        
        conn.commit()
        conn.close()
    
    # ============= PARCELAS PAGAS =============
    
    def registrar_parcela_paga(self, financiamento_id: int, 
                              numero_parcela: int, valor_parcela: float,
                              juros: float, principal: float,
                              saldo_anterior: float, saldo_posterior: float,
                              data_pagamento: Optional[datetime] = None):
        """Registra uma parcela como paga"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        data_pagamento = data_pagamento or datetime.now().date()
        
        cursor.execute("""
            INSERT INTO parcelas_pagas
            (financiamento_id, numero_parcela, data_pagamento, valor_parcela,
             juros, principal, saldo_anterior, saldo_posterior)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (financiamento_id, numero_parcela, data_pagamento, valor_parcela,
              juros, principal, saldo_anterior, saldo_posterior))
        
        conn.commit()
        conn.close()
    
    def obter_parcelas_pagas(self, financiamento_id: int) -> List[Dict]:
        """Obtém todas as parcelas pagas de um financiamento"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM parcelas_pagas 
            WHERE financiamento_id = ?
            ORDER BY numero_parcela ASC
        """, (financiamento_id,))
        
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in resultados]
    
    def total_juros_pago(self, financiamento_id: int) -> float:
        """Calcula total de juros pagos"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(juros), 0) as total
            FROM parcelas_pagas
            WHERE financiamento_id = ?
        """, (financiamento_id,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado['total'] if resultado else 0
    
    # ============= APORTES EXTRAS =============
    
    def registrar_aporte(self, financiamento_id: int, numero_parcela: int,
                        valor_aporte: float, origem: str = "manual",
                        descricao: Optional[str] = None, data_aporte: Optional[datetime] = None) -> int:
        """
        Registra um aporte extra
        
        Args:
            financiamento_id: ID do financiamento
            numero_parcela: Parcela onde fazer o aporte
            valor_aporte: Valor do aporte
            origem: Tipo de aporte ('revenda', 'salario', 'bonus', 'manual')
            descricao: Descrição do aporte
            data_aporte: Data do aporte (default: hoje)
        
        Returns:
            ID do aporte criado
        """
        conn = self._conexao()
        cursor = conn.cursor()
        
        data_aporte = data_aporte or datetime.now().date()
        
        cursor.execute("""
            INSERT INTO aportes_extras
            (financiamento_id, numero_parcela, data_aporte, valor_aporte,
             origem, descricao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (financiamento_id, numero_parcela, data_aporte, valor_aporte,
              origem, descricao))
        
        conn.commit()
        aporte_id = cursor.lastrowid
        conn.close()
        
        return aporte_id
    
    def obter_aportes(self, financiamento_id: int) -> List[Dict]:
        """Obtém todos os aportes de um financiamento"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM aportes_extras
            WHERE financiamento_id = ?
            ORDER BY data_aporte ASC
        """, (financiamento_id,))
        
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in resultados]
    
    def total_aportes(self, financiamento_id: int) -> float:
        """Calcula total de aportes realizados"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(valor_aporte), 0) as total
            FROM aportes_extras
            WHERE financiamento_id = ?
        """, (financiamento_id,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado['total'] if resultado else 0
    
    def obter_aportes_dict(self, financiamento_id: int) -> Dict[int, float]:
        """Retorna aportes no formato {numero_parcela: valor}"""
        aportes = self.obter_aportes(financiamento_id)
        return {a['numero_parcela']: a['valor_aporte'] for a in aportes}
    
    # ============= ENTRADAS EXTRAS =============
    
    def registrar_entrada_extra(self, financiamento_id: int, valor: float,
                               descricao: Optional[str] = None, produto_vendido: str = None,
                               data_entrada: datetime = None) -> int:
        """
        Registra uma entrada extra (receita de revenda)
        
        Args:
            financiamento_id: ID do financiamento
            valor: Valor da venda
            descricao: Descrição da venda
            produto_vendido: Produto que foi vendido
            data_entrada: Data da venda (default: hoje)
        
        Returns:
            ID da entrada criada
        """
        conn = self._conexao()
        cursor = conn.cursor()
        
        data_entrada = data_entrada or datetime.now().date()
        
        cursor.execute("""
            INSERT INTO entradas_extras
            (financiamento_id, data_entrada, valor, descricao, produto_vendido)
            VALUES (?, ?, ?, ?, ?)
        """, (financiamento_id, data_entrada, valor, descricao, produto_vendido))
        
        conn.commit()
        entrada_id = cursor.lastrowid
        conn.close()
        
        return entrada_id
    
    def obter_entradas_extras(self, financiamento_id: int) -> List[Dict]:
        """Obtém todas as entradas extras de um financiamento"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM entradas_extras
            WHERE financiamento_id = ?
            ORDER BY data_entrada DESC
        """, (financiamento_id,))
        
        resultados = cursor.fetchall()
        conn.close()
        
        return [dict(r) for r in resultados]
    
    def total_entradas_extras(self, financiamento_id: int) -> float:
        """Calcula total de entradas extras"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0) as total
            FROM entradas_extras
            WHERE financiamento_id = ?
        """, (financiamento_id,))
        
        resultado = cursor.fetchone()
        conn.close()
        
        return resultado['total'] if resultado else 0
    
    def alocar_entrada_para_aporte(self, entrada_id: int, aporte_id: int):
        """Aloca uma entrada extra para um aporte específico"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE entradas_extras
            SET alocado_para_aporte = 1, aporte_id = ?
            WHERE id = ?
        """, (aporte_id, entrada_id))
        
        conn.commit()
        conn.close()
    
    # ============= RELATÓRIOS =============
    
    def gerar_resumo_financiamento(self, financiamento_id: int) -> Dict:
        """Gera um resumo completo do financiamento"""
        fin = self.obter_financiamento(financiamento_id)
        parcelas = self.obter_parcelas_pagas(financiamento_id)
        aportes = self.obter_aportes(financiamento_id)
        entradas = self.obter_entradas_extras(financiamento_id)
        
        return {
            'financiamento': fin,
            'parcelas_pagas': len(parcelas),
            'total_juros_pago': self.total_juros_pago(financiamento_id),
            'total_principal_pago': sum(p['principal'] for p in parcelas),
            'aportes_realizados': len(aportes),
            'total_aportes': self.total_aportes(financiamento_id),
            'entradas_extras': len(entradas),
            'total_entradas': self.total_entradas_extras(financiamento_id),
            'progresso_percentual': (fin['saldo_inicial'] - fin['saldo_atual']) / fin['saldo_inicial'] * 100 if fin['saldo_inicial'] > 0 else 0
        }
    
    def limpar_banco(self):
        """Limpa completamente o banco (para testes)"""
        conn = self._conexao()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM entradas_extras")
        cursor.execute("DELETE FROM aportes_extras")
        cursor.execute("DELETE FROM parcelas_pagas")
        cursor.execute("DELETE FROM financiamentos")
        
        conn.commit()
        conn.close()


# Exemplo de uso
def exemplo_uso():
    print("=" * 80)
    print("EXEMPLO: Banco de Dados de Financiamentos")
    print("=" * 80)
    
    bd = GerenciadorBancoDados()
    
    # 1. Criar financiamento
    print("\n1. CRIANDO FINANCIAMENTO")
    print("-" * 80)
    fin_id = bd.criar_financiamento(
        nome="Moto 2026",
        saldo_inicial=15000,
        taxa_mensal=0.012,
        parcela_fixa=400,
        descricao="Honda CG 160 - Financiamento"
    )
    print(f"  Financiamento criado com ID: {fin_id}")
    
    # 2. Registrar parcelas pagas
    print("\n2. REGISTRANDO PARCELAS PAGAS")
    print("-" * 80)
    bd.registrar_parcela_paga(
        fin_id, numero_parcela=1, valor_parcela=400,
        juros=180, principal=220,
        saldo_anterior=15000, saldo_posterior=14780
    )
    bd.registrar_parcela_paga(
        fin_id, numero_parcela=2, valor_parcela=400,
        juros=177.36, principal=222.64,
        saldo_anterior=14780, saldo_posterior=14557.36
    )
    print(f"  2 parcelas registradas")
    
    # 3. Registrar aporte
    print("\n3. REGISTRANDO APORTES EXTRAS")
    print("-" * 80)
    aporte_id = bd.registrar_aporte(
        fin_id, numero_parcela=3, valor_aporte=500,
        origem="revenda", descricao="Venda de acessórios"
    )
    print(f"  Aporte de R$ 500 registrado (ID: {aporte_id})")
    
    # 4. Registrar entrada extra
    print("\n4. REGISTRANDO ENTRADAS EXTRAS")
    print("-" * 80)
    entrada_id = bd.registrar_entrada_extra(
        fin_id, valor=300,
        descricao="Venda de correias",
        produto_vendido="Correias para moto"
    )
    print(f"  Entrada de R$ 300 registrada")
    
    # Alocar para aporte
    bd.alocar_entrada_para_aporte(entrada_id, aporte_id)
    print(f"  Entrada alocada para aporte #{aporte_id}")
    
    # 5. Atualizar saldo
    print("\n5. ATUALIZANDO SALDO")
    print("-" * 80)
    bd.atualizar_saldo_financiamento(fin_id, 13832.05)
    print(f"  Saldo atualizado para R$ 13.832,05")
    
    # 6. Gerar resumo
    print("\n6. RESUMO DO FINANCIAMENTO")
    print("-" * 80)
    resumo = bd.gerar_resumo_financiamento(fin_id)
    
    print(f"  Nome: {resumo['financiamento']['nome']}")
    print(f"  Saldo Inicial: R$ {resumo['financiamento']['saldo_inicial']:,.2f}")
    print(f"  Saldo Atual: R$ {resumo['financiamento']['saldo_atual']:,.2f}")
    print(f"  Parcelas Pagas: {resumo['parcelas_pagas']}")
    print(f"  Total Juros Pago: R$ {resumo['total_juros_pago']:,.2f}")
    print(f"  Total Aportes: R$ {resumo['total_aportes']:,.2f}")
    print(f"  Total Entradas Extras: R$ {resumo['total_entradas']:,.2f}")
    print(f"  Progresso: {resumo['progresso_percentual']:.2f}%")
    
    # 7. Listar aportes para cálculo
    print("\n7. APORTES PARA RECÁLCULO")
    print("-" * 80)
    aportes_dict = bd.obter_aportes_dict(fin_id)
    print(f"  Aportes (dicionário): {aportes_dict}")
    print(f"  Formato para CalculadoraAmortizacao: {aportes_dict}")


if __name__ == "__main__":
    exemplo_uso()
