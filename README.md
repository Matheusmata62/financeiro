# Financiando - Sistema Inteligente de Amortização Acelerada 🏍️

Um sistema completo para gerenciar e acelerar o pagamento de financiamentos (especialmente sua moto!) através de aportes inteligentes, com dashboard visual e sugestões de IA.

> **Status Atual:** Fases 1, 2 e 3 Completas ✅ | Próxima: IA e Automação (Fase 4)

## 📋 Fases de Desenvolvimento

### ✅ Fase 1: Core de Cálculo (O Motor Financeiro)
**Status:** Completa ✓

O coração do sistema - cálculos corretos de amortização brasileira:
- ✓ Cálculo de juros mensais sobre saldo devedor
- ✓ Lógica de aportes extras (redução de prazo)
- ✓ Simulação de impacto de aportes
- ✓ Economia de juros em tempo real

**Como usar:**
```python
from src.amortizacao import CalculadoraAmortizacao

# Configurar financiamento
calc = CalculadoraAmortizacao(
    saldo_devedor=15000,      # R$ 15.000
    taxa_mensal=0.012,        # 1.2% ao mês
    parcela_mensal=400        # R$ 400
)

# Gerar plano original
plano = calc.gerar_plano_completo()
print(f"Parcelas: {len(plano.parcelas)}")
print(f"Juros: R$ {plano.total_juros_pago:.2f}")

# Adicionar aportes
plano_acelerado = calc.gerar_plano_completo({
    3: 500,    # +R$500 na 3ª parcela
    7: 1000    # +R$1.000 na 7ª parcela
})

# Simular aporte individual
meses_poupados, economia = calc.simular_aporte(300, numero_parcela=5)
```

### ✅ Fase 2: Banco de Dados e Histórico
**Status:** Completa ✓

- ✓ SQLite com múltiplas tabelas
- ✓ Histórico de parcelas pagas
- ✓ Registro de aportes com data e origem
- ✓ Entradas extras (receitas de revenda)
- ✓ Alocação automática de vendas para aportes
- ✓ Integração com motor de cálculo

### 📊 Fase 3: Dashboard Streamlit
**Status:** Aguardando Fase 1

- Gráfico de tendência (original vs acelerada)
- Widget "Economímetro" com economia em juros
- Botão de simulação rápida
- Acesso via iPhone

### 🤖 Fase 4: Inteligência e Automação
**Status:** Aguardando Fase 1

- Notificações por WhatsApp/Agenda
- IA de decisão (onde cortar gastos)
- Integração com OpenAI/Ollama

## 🏗️ Estrutura do Projeto

```
financiando/
├── src/
│   ├── amortizacao.py       # Core de cálculo ✓
│   ├── database.py          # Banco de dados ✓
│   ├── integracao.py        # Integração C + BD ✓
│   ├── dashboard.py         # Dashboard Streamlit ✓
│   └── inteligencia.py      # IA (Fase 4)
├── data/
│   └── financiamentos.db    # Banco SQLite
├── tests/
│   ├── test_amortizacao.py  # Testes ✓
│   ├── test_database.py     # Testes BD ✓
│   └── test_e2e.py          # Testes E2E ✓
├── requirements.txt
├── run_dashboard.py         # Script para dashboard
└── README.md
```

## 🚀 Como Começar Rapidamente

```python
from src.integracao import SistemaFinanciamento

# 1. Criar financiamento
sistema = SistemaFinanciamento()
fin_id = sistema.criar_financiamento_completo(
    nome="Moto Honda CG 160",
    saldo_inicial=15000,
    taxa_mensal=0.012,
    parcela_fixa=400
)

# 2. Adicionar aportes planejados
sistema.adicionar_aporte(fin_id, 3, 500, "revenda", "Venda de acessórios")

# 3. Simular impacto
p_original, p_acelerado = sistema.simular_plano_com_aportes(fin_id)
print(f"Economia: {len(p_original.parcelas) - len(p_acelerado.parcelas)} meses")

# 4. Quando vender algo
sistema.registrar_venda_e_aporte(
    fin_id, valor_venda=300, numero_parcela=5,
    produto_vendido="Correia de transmissão"
)

# 5. Ver dashboard
dados = sistema.obter_dashboard_dados(fin_id)
print(f"Meses economizados: {dados['economia']['meses']}")
print(f"Juros economizados: R$ {dados['economia']['juros']:.2f}")
```

**Veja o arquivo [GUIA_RAPIDO.py](GUIA_RAPIDO.py) para mais exemplos detalhados!**

## 📊 Exemplo de Saída

```
Parcela 001 | Data: 03/02/2026 | Saldo: R$ 15.000,00 | Juros: R$ 180,00 | Principal: R$ 220,00 | Novo Saldo: R$ 14.780,00
Parcela 002 | Data: 05/03/2026 | Saldo: R$ 14.780,00 | Juros: R$ 177,36 | Principal: R$ 222,64 | Novo Saldo: R$ 14.557,36
Parcela 003 | Data: 04/04/2026 | Saldo: R$ 14.557,36 | Juros: R$ 174,69 | Principal: R$ 225,31 | Novo Saldo: R$ 13.832,05 ← APORTE R$500
...

RESUMO ORIGINAL:
- Total de parcelas: 51
- Total de juros: R$ 5.047,45

COM APORTES (R$1.500 total):
- Total de parcelas: 44
- Total de juros: R$ 4.075,83
- Economia: 7 meses + R$ 971,62 em juros
```

## 🗄️ Banco de Dados (Fase 2)

Estrutura SQLite com 4 tabelas:

1. **financiamentos** - Registro dos empréstimos
2. **parcelas_pagas** - Histórico de pagamentos
3. **aportes_extras** - Aportes de amortização acelerada
4. **entradas_extras** - Receitas de revenda

### Exemplo de Uso:

```python
from src.integracao import SistemaFinanciamento

sistema = SistemaFinanciamento()

# Criar financiamento
fin_id = sistema.criar_financiamento_completo(
    nome="Moto Honda CG 160",
    saldo_inicial=15000,
    taxa_mensal=0.012,
    parcela_fixa=400
)

# Adicionar aportes
sistema.adicionar_aporte(fin_id, numero_parcela=3, valor_aporte=500)
sistema.adicionar_aporte(fin_id, numero_parcela=7, valor_aporte=1000)

# Simular impacto
plano_original, plano_acelerado = sistema.simular_plano_com_aportes(fin_id)

# Registrar venda (e gerar aporte automaticamente)
entrada_id, aporte_id = sistema.registrar_venda_e_aporte(
    fin_id, valor_venda=300, numero_parcela=5,
    produto_vendido="Correia de transmissão"
)

# Obter dados do dashboard
dados = sistema.obter_dashboard_dados(fin_id)
print(f"Economia: {dados['economia']['meses']} meses")
print(f"Economia em juros: R$ {dados['economia']['juros']:.2f}")
```

## 📊 Dashboard Streamlit (Fase 3)

Interface web responsiva com 4 seções principais:

### 1. **📊 Dashboard**
- Métricas em tempo real (saldo, economia, aportes)
- Gráficos comparativos (original vs acelerado)
- Widget "Economímetro" destacando juros economizados
- Histórico visual de aportes

### 2. **➕ Novo Financiamento**
- Formulário intuitivo para criar financiamentos
- Validação de taxas e valores
- Feedback imediato de sucesso

### 3. **💰 Gerenciar Aportes**
- Adicionar aportes com origem rastreada
- Visualizar histórico completo
- Registrar vendas rapidamente (cria aporte automático)
- Simulação instantânea de impacto

### 4. **📈 Simulador de Cenários**
- Sliders para simular diferentes valores
- Comparação lado a lado de múltiplos cenários
- Gráficos de impacto em tempo real

### Como Executar

```bash
# Opção 1: Script direto
python run_dashboard.py

# Opção 2: Comando Streamlit
streamlit run src/dashboard.py

# Opção 3: Com ambiente virtual
venv\Scripts\activate
streamlit run src/dashboard.py
```

### Acessar

- **PC:** http://localhost:8501
- **iPhone:** http://SEU_IP:8501 (descobrir IP com `ipconfig`)
- **Rede:** Use o IP da máquina onde está rodando

**O dashboard é 100% responsivo para iPhone!** ✅

## 🎯 Objetivo Final

Transformar você em um "gerenciador de moto acelerado" que:
1. ✓ Sabe EXATAMENTE o impacto financeiro de cada venda
2. 💡 Recebe sugestões de IA sobre melhor estratégia
3. 📱 Acompanha tudo do iPhone via Streamlit
4. 🔔 Fica informado sobre dias estratégicos de pagamento
5. 📈 Vê claramente a progressão rumo à quitação

---

**Desenvolvido para:** Matheus  
**Objetivo:** Acelerar a quitação da moto através de aportes inteligentes 🏍️  
**Status:** Fases 1, 2 e 3 Completas | Próxima: IA e Automação (Fase 4)
