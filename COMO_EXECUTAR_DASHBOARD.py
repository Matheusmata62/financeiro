"""
🚀 Como Executar o Dashboard Streamlit

Três formas de executar:
"""

# ============================================================================
# FORMA 1: Usar o script Python
# ============================================================================

# Terminal / PowerShell:
# cd c:\Users\mathe\Desktop\financiando
# python run_dashboard.py

# ============================================================================
# FORMA 2: Comando direto com Streamlit
# ============================================================================

# Terminal / PowerShell:
# cd c:\Users\mathe\Desktop\financiando
# venv\Scripts\activate  # Ativar ambiente virtual (Windows)
# streamlit run src/dashboard.py

# ============================================================================
# FORMA 3: Python direto com venv
# ============================================================================

# Terminal / PowerShell:
# cd c:\Users\mathe\Desktop\financiando
# venv\Scripts\python.exe -m streamlit run src/dashboard.py

# ============================================================================
# ACESSAR O DASHBOARD
# ============================================================================

"""
Após executar qualquer um dos comandos acima:

1. No PC:
   - Abra seu navegador
   - Acesse: http://localhost:8501
   - Ou: http://127.0.0.1:8501

2. No iPhone:
   - No PC, execute: ipconfig
   - Anote o IPv4 Address (ex: 192.168.1.100)
   - No iPhone Safari, digite: http://192.168.1.100:8501
   - Abre perfeitamente responsivo!

3. Em outro PC na rede:
   - Use o IP obtido em ipconfig
   - Acesse: http://SEU_IP:8501
"""

# ============================================================================
# PRIMEIRO USO - Passo a Passo
# ============================================================================

"""
1. Criar o ambiente virtual (primeira vez)
   ╔════════════════════════════════════════════╗
   ║ cd c:\Users\mathe\Desktop\financiando     ║
   ║ python -m venv venv                        ║
   ╚════════════════════════════════════════════╝

2. Instalar dependências (primeira vez)
   ╔════════════════════════════════════════════╗
   ║ venv\Scripts\pip install -r requirements   ║
   ╚════════════════════════════════════════════╝

3. Executar o dashboard
   ╔════════════════════════════════════════════╗
   ║ venv\Scripts\activate                      ║
   ║ streamlit run src/dashboard.py             ║
   ╚════════════════════════════════════════════╝

4. Browser abre automaticamente em http://localhost:8501

5. PRONTO! Comece a usar:
   ➕ Criar novo financiamento
   💰 Adicionar aportes
   📊 Ver dashboard
   📈 Simular cenários
"""

# ============================================================================
# DICAS IMPORTANTES
# ============================================================================

"""
📱 No iPhone:
   - Dashboard funciona 100% responsivo
   - Gráficos se adaptam ao tamanho
   - Formulários são touch-friendly
   - Performance é rápida mesmo em 4G

🔄 Recarregar:
   - F5 para recarregar página
   - Ctrl+Shift+R para recarregar completo
   - Dados sempre salvos no BD

💾 Dados:
   - Tudo é salvo em: data/financiamentos.db
   - Banco SQLite persiste mesmo fechando
   - Você não perde nenhum dado

⚡ Performance:
   - Dashboard é bem rápido
   - Gráficos carregam em menos de 1s
   - Ideal para iPhone 4G/5G

🔒 Segurança:
   - Dados salvos localmente
   - Não precisa internet (apenas para Streamlit)
   - Nenhum dado enviado para servidor
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
❌ Problema: "Port 8501 is already in use"
   ✅ Solução: 
      - Feche outras instâncias de Streamlit
      - Ou use: streamlit run src/dashboard.py --server.port 8502

❌ Problema: "ModuleNotFoundError: No module named 'streamlit'"
   ✅ Solução:
      - Ative venv: venv\Scripts\activate
      - Ou instale: venv\Scripts\pip install streamlit

❌ Problema: "Connection refused" no iPhone
   ✅ Solução:
      - Certifique-se que PC e iPhone estão na mesma rede
      - Use IP correto (ipconfig no PC)
      - Permita firewall (Windows pode bloquear)

❌ Problema: Dashboard lento
   ✅ Solução:
      - Feche outras abas
      - Atualize Python para 3.11+
      - Verifique conexão de rede
      - Limpe cache: Ctrl+Shift+Del

❌ Problema: Gráficos não aparecem
   ✅ Solução:
      - Recarregue página (F5)
      - Atualize Plotly: pip install --upgrade plotly
      - Verifique console do navegador (F12)
"""

# ============================================================================
# FUNCIONALIDADES DISPONÍVEIS
# ============================================================================

"""
No Dashboard você pode:

1. 📊 Dashboard Principal
   - Ver todas suas métricas
   - Gráficos comparativos
   - Widget economímetro
   - Histórico de aportes

2. ➕ Novo Financiamento
   - Criar novo financiamento
   - Definir taxa de juros
   - Parcela mensal
   - Descrição

3. 💰 Gerenciar Aportes
   - Adicionar aportes
   - Registrar vendas rapidamente
   - Ver histórico
   - Simular impacto

4. 📈 Simulador
   - Testar diferentes valores
   - Comparar cenários
   - Gráficos de impacto
"""

# ============================================================================
# PRÓXIMOS PASSOS
# ============================================================================

"""
Agora que o Dashboard está rodando:

1. Crie seu primeiro financiamento
   - Clique em "➕ Novo Financiamento"
   - Preencha seus dados reais
   
2. Adicione aportes planejados
   - Acesse "💰 Gerenciar Aportes"
   - Adicione seus planos
   
3. Registre suas vendas
   - Quando vender algo, use "Registrar Venda"
   - Sistema cria aporte automaticamente
   
4. Acompanhe o progresso
   - Dashboard se atualiza em tempo real
   - Veja economia crescendo

5. Simule cenários
   - Use o Simulador para testar
   - Veja impacto antes de se comprometer

Fase 4 (Próxima) adicionará:
🤖 IA para análise de gastos
🔔 Notificações WhatsApp
📅 Integração Google Calendar
"""

# ============================================================================
# ATUALIZAR REQUIREMENTS
# ============================================================================

"""
Se precisar instalar novamente:

venv\Scripts\pip install -r requirements.txt

Ou instalar individuais:

venv\Scripts\pip install streamlit==1.28.1
venv\Scripts\pip install plotly==5.17.0
venv\Scripts\pip install pandas==2.0.3
venv\Scripts\pip install sqlalchemy==2.0.21
"""

print(__doc__)
