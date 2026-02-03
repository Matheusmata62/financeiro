"""
Integração entre Cálculo de Amortização e Banco de Dados

Este módulo conecta o motor de cálculo (Fase 1) com o banco de dados (Fase 2),
permitindo calcular e salvar planos de amortização completos.
"""

from datetime import datetime
from typing import Tuple
from decimal import Decimal
from pathlib import Path

from amortizacao import CalculadoraAmortizacao, PlanoAmortizacao
from database import GerenciadorBancoDados


class SistemaFinanciamento:
    """Integra cálculo e banco de dados em um sistema coeso"""
    
    def __init__(self, db_path: Path = None):
        """Inicializa o sistema"""
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "financiamentos.db"
        self.bd = GerenciadorBancoDados(db_path)
    
    def criar_financiamento_completo(self, nome: str, saldo_inicial: float,
                                     taxa_mensal: float, parcela_fixa: float,
                                     descricao: str = None) -> int:
        """
        Cria um financiamento no banco de dados
        
        Returns:
            ID do financiamento
        """
        return self.bd.criar_financiamento(
            nome=nome,
            saldo_inicial=saldo_inicial,
            taxa_mensal=taxa_mensal,
            parcela_fixa=parcela_fixa,
            descricao=descricao
        )
    
    def adicionar_aporte(self, financiamento_id: int, numero_parcela: int,
                        valor_aporte: float, origem: str = "manual",
                        descricao: str = None) -> int:
        """Adiciona um aporte ao financiamento"""
        return self.bd.registrar_aporte(
            financiamento_id=financiamento_id,
            numero_parcela=numero_parcela,
            valor_aporte=valor_aporte,
            origem=origem,
            descricao=descricao
        )
    
    def simular_plano_com_aportes(self, financiamento_id: int) -> Tuple[PlanoAmortizacao, PlanoAmortizacao]:
        """
        Simula o plano de amortização com e sem aportes registrados
        
        Returns:
            (plano_sem_aportes, plano_com_aportes)
        """
        fin = self.bd.obter_financiamento(financiamento_id)
        
        calc = CalculadoraAmortizacao(
            saldo_devedor=fin['saldo_inicial'],
            taxa_mensal=fin['taxa_mensal'],
            parcela_mensal=fin['parcela_fixa']
        )
        
        # Plano original (sem aportes)
        plano_original = calc.gerar_plano_completo()
        
        # Plano com aportes registrados
        aportes = self.bd.obter_aportes_dict(financiamento_id)
        plano_acelerado = calc.gerar_plano_completo(aportes) if aportes else plano_original
        
        return plano_original, plano_acelerado
    
    def salvar_parcelas_do_plano(self, financiamento_id: int, 
                                plano: PlanoAmortizacao, 
                                marcar_como_pagas: bool = False):
        """
        Salva as parcelas do plano no banco de dados
        
        Args:
            financiamento_id: ID do financiamento
            plano: Plano de amortização a salvar
            marcar_como_pagas: Se True, marca as parcelas como já pagas
        """
        for parcela in plano.parcelas:
            self.bd.registrar_parcela_paga(
                financiamento_id=financiamento_id,
                numero_parcela=parcela.numero,
                valor_parcela=float(parcela.valor_parcela),
                juros=float(parcela.juros),
                principal=float(parcela.principal),
                saldo_anterior=float(parcela.saldo_anterior),
                saldo_posterior=float(parcela.saldo_posterior),
                data_pagamento=parcela.data if marcar_como_pagas else None
            )
    
    def simular_aporte_venda(self, financiamento_id: int, 
                           valor_venda: float, numero_parcela: int) -> Tuple[int, float]:
        """
        Simula o impacto de uma venda (aporte) em uma parcela específica
        
        Args:
            financiamento_id: ID do financiamento
            valor_venda: Valor da venda
            numero_parcela: Em qual parcela aplicar o aporte
        
        Returns:
            (meses_economizados, economia_em_juros)
        """
        fin = self.bd.obter_financiamento(financiamento_id)
        
        calc = CalculadoraAmortizacao(
            saldo_devedor=fin['saldo_inicial'],
            taxa_mensal=fin['taxa_mensal'],
            parcela_mensal=fin['parcela_fixa']
        )
        
        meses, economia = calc.simular_aporte(valor_venda, numero_parcela)
        
        return meses, economia
    
    def registrar_venda_e_aporte(self, financiamento_id: int,
                                valor_venda: float, numero_parcela: int,
                                descricao: str, produto_vendido: str = None) -> Tuple[int, int]:
        """
        Registra uma venda (entrada extra) e a converte em aporte automaticamente
        
        Returns:
            (entrada_id, aporte_id)
        """
        # Registra a venda como entrada extra
        entrada_id = self.bd.registrar_entrada_extra(
            financiamento_id=financiamento_id,
            valor=valor_venda,
            descricao=descricao,
            produto_vendido=produto_vendido
        )
        
        # Registra o aporte correspondente
        aporte_id = self.bd.registrar_aporte(
            financiamento_id=financiamento_id,
            numero_parcela=numero_parcela,
            valor_aporte=valor_venda,
            origem="revenda",
            descricao=f"Aporte de venda: {produto_vendido or descricao}"
        )
        
        # Aloca a entrada para o aporte
        self.bd.alocar_entrada_para_aporte(entrada_id, aporte_id)
        
        return entrada_id, aporte_id
    
    def obter_dashboard_dados(self, financiamento_id: int) -> dict:
        """Obtém todos os dados necessários para o dashboard"""
        
        plano_original, plano_com_aportes = self.simular_plano_com_aportes(
            financiamento_id
        )
        
        resumo = self.bd.gerar_resumo_financiamento(financiamento_id)
        
        return {
            'financiamento': resumo['financiamento'],
            'plano_original': {
                'parcelas': len(plano_original.parcelas),
                'total_juros': float(plano_original.total_juros_pago),
            },
            'plano_acelerado': {
                'parcelas': len(plano_com_aportes.parcelas),
                'total_juros': float(plano_com_aportes.total_juros_pago),
            },
            'economia': {
                'meses': len(plano_original.parcelas) - len(plano_com_aportes.parcelas),
                'juros': float(plano_original.total_juros_pago - plano_com_aportes.total_juros_pago),
            },
            'historico': {
                'parcelas_pagas': resumo['parcelas_pagas'],
                'total_juros_pago': resumo['total_juros_pago'],
                'total_principal_pago': resumo['total_principal_pago'],
                'aportes_realizados': resumo['aportes_realizados'],
                'total_aportes': resumo['total_aportes'],
                'entradas_extras': resumo['entradas_extras'],
                'total_entradas': resumo['total_entradas'],
                'progresso_percentual': resumo['progresso_percentual'],
            }
        }


def exemplo_uso():
    """Exemplo de uso integrado"""
    print("=" * 80)
    print("EXEMPLO: Sistema Integrado de Financiamento")
    print("=" * 80)
    
    sistema = SistemaFinanciamento()
    
    # 1. Criar financiamento
    print("\n1. CRIANDO FINANCIAMENTO")
    print("-" * 80)
    fin_id = sistema.criar_financiamento_completo(
        nome="Moto Honda CG 160",
        saldo_inicial=15000,
        taxa_mensal=0.012,
        parcela_fixa=400,
        descricao="Financiamento 2026 - Acelerado com aportes"
    )
    print(f"  ✓ Financiamento criado (ID: {fin_id})")
    
    # 2. Adicionar aportes
    print("\n2. ADICIONANDO APORTES")
    print("-" * 80)
    aporte1 = sistema.adicionar_aporte(
        fin_id, numero_parcela=3,
        valor_aporte=500,
        origem="revenda",
        descricao="Venda de acessórios"
    )
    print(f"  ✓ Aporte 1: R$ 500 na parcela 3")
    
    aporte2 = sistema.adicionar_aporte(
        fin_id, numero_parcela=7,
        valor_aporte=1000,
        origem="revenda",
        descricao="Venda de peças usadas"
    )
    print(f"  ✓ Aporte 2: R$ 1.000 na parcela 7")
    
    # 3. Simular planos
    print("\n3. SIMULANDO PLANOS DE AMORTIZAÇÃO")
    print("-" * 80)
    plano_original, plano_acelerado = sistema.simular_plano_com_aportes(fin_id)
    
    print(f"  PLANO ORIGINAL:")
    print(f"    Parcelas: {len(plano_original.parcelas)}")
    print(f"    Juros: R$ {plano_original.total_juros_pago:,.2f}")
    
    print(f"\n  PLANO ACELERADO:")
    print(f"    Parcelas: {len(plano_acelerado.parcelas)}")
    print(f"    Juros: R$ {plano_acelerado.total_juros_pago:,.2f}")
    
    print(f"\n  ECONOMIA:")
    print(f"    Meses: {len(plano_original.parcelas) - len(plano_acelerado.parcelas)}")
    print(f"    Juros: R$ {plano_original.total_juros_pago - plano_acelerado.total_juros_pago:,.2f}")
    
    # 4. Simular venda
    print("\n4. SIMULANDO VENDA (E se vender algo por R$ 300 na parcela 5?)")
    print("-" * 80)
    meses, economia = sistema.simular_aporte_venda(fin_id, 300, 5)
    print(f"  Meses economizados: {meses}")
    print(f"  Economia em juros: R$ {economia:,.2f}")
    
    # 5. Registrar venda e aporte
    print("\n5. REGISTRANDO VENDA E APORTE AUTOMÁTICO")
    print("-" * 80)
    entrada_id, aporte_id = sistema.registrar_venda_e_aporte(
        fin_id, valor_venda=300, numero_parcela=5,
        descricao="Venda rápida",
        produto_vendido="Correia de transmissão"
    )
    print(f"  ✓ Venda registrada (Entrada ID: {entrada_id})")
    print(f"  ✓ Aporte criado automaticamente (Aporte ID: {aporte_id})")
    
    # 6. Dashboard
    print("\n6. DADOS DO DASHBOARD")
    print("-" * 80)
    dados = sistema.obter_dashboard_dados(fin_id)
    
    print(f"  Financiamento: {dados['financiamento']['nome']}")
    print(f"  Economia Potencial: {dados['economia']['meses']} meses")
    print(f"  Economia em Juros: R$ {dados['economia']['juros']:,.2f}")
    print(f"  Aportes Realizados: {dados['historico']['aportes_realizados']}")
    print(f"  Total Aportes: R$ {dados['historico']['total_aportes']:,.2f}")
    print(f"  Entradas Extras: {dados['historico']['entradas_extras']}")
    print(f"  Total Entradas: R$ {dados['historico']['total_entradas']:,.2f}")


if __name__ == "__main__":
    exemplo_uso()
