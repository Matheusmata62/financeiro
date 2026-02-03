"""
Testes para o gerenciador de banco de dados
"""

import sys
from pathlib import Path
import tempfile
from datetime import datetime

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database import GerenciadorBancoDados


def test_criar_financiamento():
    """Testa criação de financiamento"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test Moto",
            saldo_inicial=15000,
            taxa_mensal=0.012,
            parcela_fixa=400
        )
        
        assert fin_id > 0, "Financiamento não foi criado"
        
        fin = bd.obter_financiamento(fin_id)
        assert fin['saldo_inicial'] == 15000, "Saldo inicial incorreto"
        assert fin['ativo'] == 1, "Financiamento deve estar ativo"
        
        print("✓ Teste criar financiamento: PASSOU")


def test_registrar_parcela():
    """Testa registro de parcela paga"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test", saldo_inicial=10000, 
            taxa_mensal=0.01, parcela_fixa=300
        )
        
        bd.registrar_parcela_paga(
            fin_id, numero_parcela=1, valor_parcela=300,
            juros=100, principal=200,
            saldo_anterior=10000, saldo_posterior=9800
        )
        
        parcelas = bd.obter_parcelas_pagas(fin_id)
        assert len(parcelas) == 1, "Uma parcela deve estar registrada"
        assert parcelas[0]['juros'] == 100, "Juros incorreto"
        
        total_juros = bd.total_juros_pago(fin_id)
        assert total_juros == 100, f"Total de juros deve ser 100, obteve {total_juros}"
        
        print("✓ Teste registrar parcela: PASSOU")


def test_registrar_aporte():
    """Testa registro de aporte extra"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test", saldo_inicial=10000,
            taxa_mensal=0.01, parcela_fixa=300
        )
        
        aporte_id = bd.registrar_aporte(
            fin_id, numero_parcela=3, valor_aporte=500,
            origem="revenda", descricao="Venda de acessórios"
        )
        
        assert aporte_id > 0, "Aporte não foi criado"
        
        aportes = bd.obter_aportes(fin_id)
        assert len(aportes) == 1, "Um aporte deve estar registrado"
        assert aportes[0]['valor_aporte'] == 500, "Valor do aporte incorreto"
        
        total = bd.total_aportes(fin_id)
        assert total == 500, f"Total de aportes deve ser 500, obteve {total}"
        
        print("✓ Teste registrar aporte: PASSOU")


def test_registrar_entrada_extra():
    """Testa registro de entrada extra"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test", saldo_inicial=10000,
            taxa_mensal=0.01, parcela_fixa=300
        )
        
        entrada_id = bd.registrar_entrada_extra(
            fin_id, valor=300,
            descricao="Venda de correias",
            produto_vendido="Correias"
        )
        
        assert entrada_id > 0, "Entrada não foi criada"
        
        entradas = bd.obter_entradas_extras(fin_id)
        assert len(entradas) == 1, "Uma entrada deve estar registrada"
        assert entradas[0]['valor'] == 300, "Valor da entrada incorreto"
        
        total = bd.total_entradas_extras(fin_id)
        assert total == 300, f"Total de entradas deve ser 300, obteve {total}"
        
        print("✓ Teste registrar entrada extra: PASSOU")


def test_alocar_entrada_para_aporte():
    """Testa alocação de entrada para aporte"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test", saldo_inicial=10000,
            taxa_mensal=0.01, parcela_fixa=300
        )
        
        entrada_id = bd.registrar_entrada_extra(
            fin_id, valor=500, produto_vendido="Peça"
        )
        
        aporte_id = bd.registrar_aporte(
            fin_id, numero_parcela=3, valor_aporte=500,
            origem="revenda"
        )
        
        bd.alocar_entrada_para_aporte(entrada_id, aporte_id)
        
        entradas = bd.obter_entradas_extras(fin_id)
        assert entradas[0]['alocado_para_aporte'] == 1, "Entrada deve estar alocada"
        assert entradas[0]['aporte_id'] == aporte_id, "Aporte ID incorreto"
        
        print("✓ Teste alocar entrada para aporte: PASSOU")


def test_obter_aportes_dict():
    """Testa formato de aportes para cálculo"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test", saldo_inicial=10000,
            taxa_mensal=0.01, parcela_fixa=300
        )
        
        bd.registrar_aporte(fin_id, numero_parcela=3, valor_aporte=500)
        bd.registrar_aporte(fin_id, numero_parcela=7, valor_aporte=1000)
        
        aportes = bd.obter_aportes_dict(fin_id)
        
        assert aportes == {3: 500, 7: 1000}, "Dicionário de aportes incorreto"
        
        print("✓ Teste obter aportes dict: PASSOU")


def test_resumo_financiamento():
    """Testa geração de resumo completo"""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        bd = GerenciadorBancoDados(db_path)
        
        fin_id = bd.criar_financiamento(
            nome="Test", saldo_inicial=10000,
            taxa_mensal=0.01, parcela_fixa=300
        )
        
        bd.registrar_parcela_paga(
            fin_id, 1, 300, 100, 200, 10000, 9800
        )
        
        bd.registrar_aporte(fin_id, 3, 500, "revenda")
        bd.registrar_entrada_extra(fin_id, 300, "Venda")
        bd.atualizar_saldo_financiamento(fin_id, 9800)
        
        resumo = bd.gerar_resumo_financiamento(fin_id)
        
        assert resumo['parcelas_pagas'] == 1, "Deve ter 1 parcela paga"
        assert resumo['total_juros_pago'] == 100, "Juros incorreto"
        assert resumo['total_aportes'] == 500, "Total aportes incorreto"
        assert resumo['total_entradas'] == 300, "Total entradas incorreto"
        assert resumo['progresso_percentual'] == 2.0, "Progresso incorreto"
        
        print("✓ Teste resumo financiamento: PASSOU")


if __name__ == "__main__":
    print("Executando testes do Banco de Dados (Fase 2)...\n")
    
    test_criar_financiamento()
    test_registrar_parcela()
    test_registrar_aporte()
    test_registrar_entrada_extra()
    test_alocar_entrada_para_aporte()
    test_obter_aportes_dict()
    test_resumo_financiamento()
    
    print("\n✅ Todos os testes do banco de dados passaram!")
