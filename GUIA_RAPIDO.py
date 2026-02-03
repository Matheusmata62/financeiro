"""
Guia Rápido - Financiando v1.0

Como usar o sistema de amortização acelerada
"""

# ============================================================================
# 1. SETUP INICIAL
# ============================================================================

# Na primeira vez:
# python -m venv venv
# venv\Scripts\activate
# pip install -r requirements.txt

# ============================================================================
# 2. CRIAR SEU FINANCIAMENTO
# ============================================================================

from src.integracao import SistemaFinanciamento

sistema = SistemaFinanciamento()

# Seus dados da moto
fin_id = sistema.criar_financiamento_completo(
    nome="Moto Honda CG 160",
    saldo_inicial=15000,      # Saldo que você deve
    taxa_mensal=0.012,        # 1.2% ao mês (0.012 em decimal)
    parcela_fixa=400          # Sua parcela mensal
)

# ============================================================================
# 3. ADICIONAR APORTES PLANEJADOS
# ============================================================================

# Se você planeja vender coisas para amortizar
sistema.adicionar_aporte(
    fin_id, 
    numero_parcela=3,         # Na 3ª parcela
    valor_aporte=500,         # +R$ 500
    origem="revenda",         # Venda de coisas
    descricao="Venda de acessórios"
)

sistema.adicionar_aporte(fin_id, 7, 1000, "revenda", "Venda maior")

# ============================================================================
# 4. VER O IMPACTO
# ============================================================================

plano_original, plano_acelerado = sistema.simular_plano_com_aportes(fin_id)

print(f"SEM aportes:   {len(plano_original.parcelas)} meses, R$ {plano_original.total_juros_pago:.2f} em juros")
print(f"COM aportes:   {len(plano_acelerado.parcelas)} meses, R$ {plano_acelerado.total_juros_pago:.2f} em juros")
print(f"ECONOMIA:      {len(plano_original.parcelas) - len(plano_acelerado.parcelas)} meses")

# ============================================================================
# 5. QUANDO VENDER ALGO (O MAIS IMPORTANTE!)
# ============================================================================

# Você vendeu uma correia de transmissão por R$ 300?
sistema.registrar_venda_e_aporte(
    fin_id,
    valor_venda=300,          # Quanto vendeu
    numero_parcela=5,         # Qual parcela você quer amortizar
    descricao="Venda rápida",
    produto_vendido="Correia de transmissão"
)

# Isso automaticamente:
# 1. Registra que você ganhou R$ 300
# 2. Cria um aporte de R$ 300
# 3. Aloca esse dinheiro para a parcela 5
# 4. Recalcula tudo

# ============================================================================
# 6. SIMULAR ANTES DE COMPROMETER
# ============================================================================

# "Se eu vender algo por R$ 250 agora, quanto economizo?"
meses, economia = sistema.simular_aporte_venda(fin_id, valor_venda=250, numero_parcela=5)

print(f"Vendendo R$ 250 na parcela 5:")
print(f"  - Economizo {meses} meses")
print(f"  - Poupo R$ {economia:.2f} em juros")

# ============================================================================
# 7. VER TUDO JUNTO (Dashboard)
# ============================================================================

dados = sistema.obter_dashboard_dados(fin_id)

print("\n📊 DASHBOARD")
print(f"Nome: {dados['financiamento']['nome']}")
print(f"\n💰 ECONOMIA POTENCIAL:")
print(f"   Meses: {dados['economia']['meses']}")
print(f"   Juros: R$ {dados['economia']['juros']:.2f}")
print(f"\n📈 HISTÓRICO:")
print(f"   Parcelas pagas: {dados['historico']['parcelas_pagas']}")
print(f"   Aportes: {dados['historico']['aportes_realizados']}")
print(f"   Total investido em aportes: R$ {dados['historico']['total_aportes']:.2f}")
print(f"   Vendas registradas: {dados['historico']['entradas_extras']}")
print(f"   Total de vendas: R$ {dados['historico']['total_entradas']:.2f}")
print(f"   Progresso: {dados['historico']['progresso_percentual']:.2f}%")

# ============================================================================
# 8. TESTES
# ============================================================================

# Para validar que tudo está funcionando:
# python tests/test_amortizacao.py
# python tests/test_database.py  
# python tests/test_e2e.py

# ============================================================================
# 9. ESTRUTURA DO BANCO DE DADOS
# ============================================================================

# Quando você executa o código, um arquivo é criado:
# data/financiamentos.db

# Ele tem essas tabelas:
# - financiamentos       (seus empréstimos)
# - parcelas_pagas       (histórico de pagamentos)
# - aportes_extras       (aportes que você fez)
# - entradas_extras      (vendas que você registrou)

# ============================================================================
# 10. PRÓXIMOS PASSOS
# ============================================================================

# Quando o Dashboard (Fase 3) ficar pronto:
# streamlit run src/dashboard.py
# 
# Aí você consegue:
# ✓ Ver gráficos lindos
# ✓ Simular vendas em tempo real
# ✓ Acompanhar do iPhone
# ✓ Receber notificações automáticas

# ============================================================================
# DICAS IMPORTANTES
# ============================================================================

# 1. TAXA DE JUROS: Se sua taxa é 1.2%, use 0.012 (não 1.2 ou 1,2)
# 
# 2. SALDO DEVEDOR: Use APENAS o valor que você ainda deve
#    (não o total que já pagou)
# 
# 3. APORTES: Quanto ANTES você aportar, MAIS juros economiza
#    (apporte na parcela 3 economiza mais que na parcela 10)
# 
# 4. SIMULAÇÃO: Sempre simule antes de registrar
#    (veja o impacto real de cada venda)
# 
# 5. HISTÓRICO: Seus dados são salvos no banco
#    (você pode fechar e abrir sem perder nada)

print("\n✅ Sistema pronto para usar!")
