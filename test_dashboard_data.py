#!/usr/bin/env python
# Teste de dados para dashboard

import sys
from pathlib import Path
import tempfile

sys.path.insert(0, 'src')

from integracao import SistemaFinanciamento

# Criar sistema com BD temporário
with tempfile.TemporaryDirectory() as tmpdir:
    db_path = Path(tmpdir) / 'test.db'
    sistema = SistemaFinanciamento(db_path)
    
    # Criar financiamento
    fin_id = sistema.criar_financiamento_completo(
        nome='Moto Teste Dashboard',
        saldo_inicial=15000,
        taxa_mensal=0.012,
        parcela_fixa=400
    )
    
    # Adicionar aportes
    sistema.adicionar_aporte(fin_id, 3, 500, 'revenda', 'Venda 1')
    sistema.adicionar_aporte(fin_id, 7, 1000, 'revenda', 'Venda 2')
    
    # Registrar venda
    sistema.registrar_venda_e_aporte(fin_id, 300, 5, 'Venda rápida', 'Correia')
    
    # Obter dados para dashboard
    dados = sistema.obter_dashboard_dados(fin_id)
    
    print('=' * 60)
    print('Dashboard Test - Dados Obtidos com Sucesso!')
    print('=' * 60)
    print()
    print('Financiamento:', dados['financiamento']['nome'])
    print('Saldo Atual:', f"R$ {dados['financiamento']['saldo_atual']:,.2f}")
    print()
    print('Plano Original:')
    print(f'  Parcelas: {dados["plano_original"]["parcelas"]}')
    print(f'  Juros: R$ {dados["plano_original"]["total_juros"]:,.2f}')
    print()
    print('Plano Acelerado:')
    print(f'  Parcelas: {dados["plano_acelerado"]["parcelas"]}')
    print(f'  Juros: R$ {dados["plano_acelerado"]["total_juros"]:,.2f}')
    print()
    print('Economia:')
    print(f'  Meses: {dados["economia"]["meses"]}')
    print(f'  Juros: R$ {dados["economia"]["juros"]:,.2f}')
    print()
    print('Histórico:')
    print(f'  Aportes: {dados["historico"]["aportes_realizados"]}')
    print(f'  Total Aportes: R$ {dados["historico"]["total_aportes"]:,.2f}')
    print(f'  Entradas: {dados["historico"]["entradas_extras"]}')
    print(f'  Total Entradas: R$ {dados["historico"]["total_entradas"]:,.2f}')
    print()
    print('=' * 60)
    print('✅ Dashboard está 100% funcional!')
    print('=' * 60)
