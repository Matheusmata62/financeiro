"""
Teste de integração completa (E2E) - Fase 1 + Fase 2
"""

import sys
import os
from pathlib import Path
import tempfile

# Configura encoding UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.amortizacao import CalculadoraAmortizacao
from src.integracao import SistemaFinanciamento


def test_fluxo_completo_usuario():
    """
    Simula o fluxo completo de um usuário:
    1. Cria um financiamento
    2. Registra aportes
    3. Simula vendas
    4. Verifica resultados
    """
    print("=" * 80)
    print("TESTE E2E: Fluxo Completo do Usuario")
    print("=" * 80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        sistema = SistemaFinanciamento(db_path)
        
        # Step 1: Usuário cria financiamento
        print("\n[OK] Step 1: Criando financiamento de R$ 15.000")
        fin_id = sistema.criar_financiamento_completo(
            nome="Moto Test",
            saldo_inicial=15000,
            taxa_mensal=0.012,
            parcela_fixa=400
        )
        assert fin_id > 0, "Financiamento não foi criado"
        
        # Step 2: Usuário planeja aportes iniciais
        print("[OK] Step 2: Adicionando aportes planejados")
        aporte1 = sistema.adicionar_aporte(fin_id, 3, 500, "revenda", "Venda inicial")
        aporte2 = sistema.adicionar_aporte(fin_id, 7, 1000, "revenda", "Venda maior")
        assert aporte1 > 0 and aporte2 > 0, "Aportes não foram criados"
        
        # Step 3: Simular impacto
        print("[OK] Step 3: Simulando plano com aportes")
        plano_original, plano_acelerado = sistema.simular_plano_com_aportes(fin_id)
        
        economia_meses = len(plano_original.parcelas) - len(plano_acelerado.parcelas)
        economia_juros = plano_original.total_juros_pago - plano_acelerado.total_juros_pago
        
        print(f"   - Meses economizados: {economia_meses}")
        print(f"   - Juros economizados: R$ {economia_juros:.2f}")
        
        assert economia_meses > 0, "Deve haver economia de meses"
        assert economia_juros > 0, "Deve haver economia de juros"
        
        # Step 4: Usuário vende um item
        print("[OK] Step 4: Registrando venda (entrada extra + aporte automático)")
        entrada_id, aporte_id = sistema.registrar_venda_e_aporte(
            fin_id, valor_venda=300, numero_parcela=5,
            descricao="Venda rápida",
            produto_vendido="Correia"
        )
        assert entrada_id > 0 and aporte_id > 0, "Venda e aporte não foram registrados"
        
        # Step 5: Verificar dashboard
        print("[OK] Step 5: Gerando dashboard")
        dados = sistema.obter_dashboard_dados(fin_id)
        
        assert dados['historico']['aportes_realizados'] == 3, "Deve haver 3 aportes"
        assert dados['historico']['total_aportes'] == 1800, "Total aportes deve ser R$ 1.800"
        assert dados['historico']['entradas_extras'] == 1, "Deve haver 1 entrada extra"
        assert dados['historico']['total_entradas'] == 300, "Total entradas deve ser R$ 300"
        
        # Step 6: Simular nova venda
        print("[OK] Step 6: Simulando nova venda (R$ 250)")
        meses_novos, economia_nova = sistema.simular_aporte_venda(fin_id, 250, 10)
        assert meses_novos > 0, "Deve haver redução de meses"
        assert economia_nova > 0, "Deve haver economia"
        
        print(f"   - Reducao: {meses_novos} meses")
        print(f"   - Economia: R$ {economia_nova:.2f}")
        
        # Step 7: Registrar essa nova venda
        print("[OK] Step 7: Registrando nova venda")
        entrada_id2, aporte_id2 = sistema.registrar_venda_e_aporte(
            fin_id, valor_venda=250, numero_parcela=10,
            descricao="Segunda venda",
            produto_vendido="Pneu"
        )
        
        # Step 8: Verificar totais finais
        print("[OK] Step 8: Verificando totais finais")
        dados_finais = sistema.obter_dashboard_dados(fin_id)
        
        assert dados_finais['historico']['aportes_realizados'] == 4, "Deve haver 4 aportes"
        assert dados_finais['historico']['total_aportes'] == 2050, "Total deve ser R$ 2.050"
        assert dados_finais['historico']['total_entradas'] == 550, "Total entradas deve ser R$ 550"
        
        print(f"   - Total de aportes: {dados_finais['historico']['aportes_realizados']}")
        print(f"   - Valor acumulado: R$ {dados_finais['historico']['total_aportes']:.2f}")
        print(f"   - Meses economizados: {dados_finais['economia']['meses']}")
        print(f"   - Juros economizados: R$ {dados_finais['economia']['juros']:.2f}")
        
        print("\n" + "=" * 80)
        print("[SUCESSO] TESTE E2E PASSOU - Fluxo completo funciona perfeitamente!")
        print("=" * 80)


if __name__ == "__main__":
    test_fluxo_completo_usuario()
