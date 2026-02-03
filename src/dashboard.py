"""
Fase 3: Dashboard Streamlit - Interface Visual

Sistema web interativo para gerenciar e visualizar amortização acelerada
Acesso: streamlit run src/dashboard.py
iPhone: Abra em navegador mobile (responde automaticamente)
"""

import streamlit as st
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent))

from integracao import SistemaFinanciamento
from amortizacao import CalculadoraAmortizacao

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================

st.set_page_config(
    page_title="Financiando - Moto Acelerada 🏍️",
    page_icon="🏍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhor visual no iPhone
st.markdown("""
    <style>
    /* Mobile responsivo */
    @media (max-width: 640px) {
        .block-container {
            padding: 1rem;
        }
    }
    
    /* Cores e temas */
    :root {
        --primary-color: #FF6B35;
        --secondary-color: #004E89;
        --success-color: #06A77D;
        --danger-color: #D62828;
    }
    
    /* Cards com sombra */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

sistema = SistemaFinanciamento()

# Sidebar para navegação
with st.sidebar:
    st.markdown("# 🏍️ Financiando")
    st.markdown("**Sistema de Amortização Acelerada**")
    st.markdown("---")
    
    pagina = st.radio(
        "Navegação:",
        ["📊 Dashboard", "➕ Novo Financiamento", "💰 Gerenciar Aportes", "📈 Simulador"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ℹ️ Sobre")
    st.markdown("""
    Sistema inteligente para acelerar 
    a quitação da sua moto através 
    de aportes estratégicos.
    
    **Desenvolvido para:** Matheus  
    **Data:** 3 de fevereiro de 2026
    """)

# ============================================================================
# PÁGINA: DASHBOARD PRINCIPAL
# ============================================================================

if pagina == "📊 Dashboard":
    st.title("📊 Dashboard Financeiro")
    
    # Obter financiamentos
    financiamentos = sistema.bd.listar_financiamentos(apenas_ativos=True)
    
    if not financiamentos:
        st.warning("⚠️ Nenhum financiamento cadastrado. Clique em '➕ Novo Financiamento' para começar!")
    else:
        # Seletor de financiamento
        nomes_fin = [f"{f['nome']}" for f in financiamentos]
        fin_selecionado = st.selectbox("Selecione seu financiamento:", nomes_fin)
        fin_id = next(f['id'] for f in financiamentos if f['nome'] == fin_selecionado)
        
        # Obter dados
        dados = sistema.obter_dashboard_dados(fin_id)
        fin_info = dados['financiamento']
        economia = dados['economia']
        historico = dados['historico']
        
        # ====== ROW 1: PRINCIPAIS MÉTRICAS ======
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 Saldo Atual",
                f"R$ {fin_info['saldo_atual']:,.2f}",
                f"{historico['progresso_percentual']:.1f}% quitado"
            )
        
        with col2:
            st.metric(
                "⏱️ Meses Economizados",
                f"{economia['meses']} meses",
                f"Da estimativa original"
            )
        
        with col3:
            st.metric(
                "💸 Juros Economizados",
                f"R$ {economia['juros']:,.2f}",
                "Em economia total"
            )
        
        with col4:
            st.metric(
                "📊 Aportes Realizados",
                f"{historico['aportes_realizados']}",
                f"R$ {historico['total_aportes']:,.2f} investido"
            )
        
        st.markdown("---")
        
        # ====== ROW 2: GRÁFICOS DE AMORTIZAÇÃO ======
        col_grafico1, col_grafico2 = st.columns(2)
        
        with col_grafico1:
            st.subheader("📈 Comparação de Prazo")
            
            fig_prazo = go.Figure()
            fig_prazo.add_trace(go.Bar(
                x=["Original", "Com Aportes"],
                y=[
                    dados['plano_original']['parcelas'],
                    dados['plano_acelerado']['parcelas']
                ],
                marker=dict(color=['#FF6B35', '#06A77D']),
                text=[
                    f"{dados['plano_original']['parcelas']} meses",
                    f"{dados['plano_acelerado']['parcelas']} meses"
                ],
                textposition='outside'
            ))
            fig_prazo.update_layout(
                showlegend=False,
                height=300,
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig_prazo, use_container_width=True)
        
        with col_grafico2:
            st.subheader("💸 Economia de Juros")
            
            fig_juros = go.Figure()
            fig_juros.add_trace(go.Bar(
                x=["Original", "Com Aportes"],
                y=[
                    dados['plano_original']['total_juros'],
                    dados['plano_acelerado']['total_juros']
                ],
                marker=dict(color=['#D62828', '#06A77D']),
                text=[
                    f"R$ {dados['plano_original']['total_juros']:,.0f}",
                    f"R$ {dados['plano_acelerado']['total_juros']:,.0f}"
                ],
                textposition='outside'
            ))
            fig_juros.update_layout(
                showlegend=False,
                height=300,
                margin=dict(t=20, b=20)
            )
            st.plotly_chart(fig_juros, use_container_width=True)
        
        st.markdown("---")
        
        # ====== WIDGET: ECONOMÍMETRO ======
        st.subheader("💰 ECONOMÍMETRO")
        
        # Barra de progresso visual
        economiza_por_mes = economia['juros'] / max(economia['meses'], 1)
        
        col_eco1, col_eco2 = st.columns([2, 1])
        with col_eco1:
            progress = min(economia['juros'] / (economia['juros'] + dados['plano_acelerado']['total_juros']), 1.0)
            st.progress(progress)
        
        with col_eco2:
            st.markdown(f"""
            ### R$ {economia['juros']:,.2f}
            **Juros poupados**
            """)
        
        st.info(f"""
        💡 **Você está economizando ~R$ {economiza_por_mes:,.2f} em juros a cada mês!**
        
        Se continuar com os aportes planejados, vai economizar **R$ {economia['juros']:,.2f}** 
        em juros e sair do financiamento **{economia['meses']} meses mais cedo**!
        """)
        
        st.markdown("---")
        
        # ====== HISTÓRICO DE APORTES ======
        st.subheader("📋 Histórico de Aportes")
        
        aportes = sistema.bd.obter_aportes(fin_id)
        
        if aportes:
            df_aportes = pd.DataFrame(aportes)
            df_aportes['data_aporte'] = pd.to_datetime(df_aportes['data_aporte']).dt.strftime('%d/%m/%Y')
            df_aportes = df_aportes[['numero_parcela', 'valor_aporte', 'origem', 'descricao', 'data_aporte']]
            df_aportes.columns = ['Parcela', 'Valor', 'Origem', 'Descrição', 'Data']
            
            st.dataframe(df_aportes, use_container_width=True)
        else:
            st.info("Nenhum aporte registrado ainda. Adicione aportes em '💰 Gerenciar Aportes'")
        
        st.markdown("---")
        
        # ====== ESTATÍSTICAS GERAIS ======
        st.subheader("📊 Estatísticas Gerais")
        
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Parcelas Pagas", f"{historico['parcelas_pagas']}")
            st.metric("Total Principal", f"R$ {historico['total_principal_pago']:,.2f}")
        
        with col_stat2:
            st.metric("Total Juros Pago", f"R$ {historico['total_juros_pago']:,.2f}")
            st.metric("Vendas Registradas", f"{historico['entradas_extras']}")
        
        with col_stat3:
            st.metric("Total de Vendas", f"R$ {historico['total_entradas']:,.2f}")
            st.metric("Progresso", f"{historico['progresso_percentual']:.1f}%")

# ============================================================================
# PÁGINA: NOVO FINANCIAMENTO
# ============================================================================

elif pagina == "➕ Novo Financiamento":
    st.title("➕ Novo Financiamento")
    
    with st.form("novo_financiamento"):
        st.markdown("### Informações do Financiamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Nome do Financiamento", "Moto Honda CG 160")
            saldo_inicial = st.number_input(
                "Saldo Inicial (R$)",
                min_value=1000.0,
                value=15000.0,
                step=100.0
            )
        
        with col2:
            descricao = st.text_input("Descrição", "Financiamento acelerado com aportes")
            parcela_fixa = st.number_input(
                "Parcela Mensal (R$)",
                min_value=100.0,
                value=400.0,
                step=50.0
            )
        
        st.markdown("### Taxas")
        
        col_taxa1, col_taxa2 = st.columns(2)
        
        with col_taxa1:
            taxa_percent = st.number_input(
                "Taxa de Juros (% ao mês)",
                min_value=0.1,
                value=1.2,
                step=0.1
            )
        
        with col_taxa2:
            taxa_decimal = taxa_percent / 100
            st.metric("Taxa decimal:", f"{taxa_decimal:.6f}")
        
        st.info("💡 Se sua taxa é 1.2% ao mês, insira 1.2")
        
        submitted = st.form_submit_button("✅ Criar Financiamento", use_container_width=True)
        
        if submitted:
            try:
                fin_id = sistema.criar_financiamento_completo(
                    nome=nome,
                    saldo_inicial=saldo_inicial,
                    taxa_mensal=taxa_decimal,
                    parcela_fixa=parcela_fixa,
                    descricao=descricao
                )
                st.success(f"✅ Financiamento criado com sucesso! (ID: {fin_id})")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Erro ao criar financiamento: {e}")

# ============================================================================
# PÁGINA: GERENCIAR APORTES
# ============================================================================

elif pagina == "💰 Gerenciar Aportes":
    st.title("💰 Gerenciar Aportes")
    
    financiamentos = sistema.bd.listar_financiamentos(apenas_ativos=True)
    
    if not financiamentos:
        st.warning("⚠️ Nenhum financiamento cadastrado!")
    else:
        nomes_fin = [f"{f['nome']}" for f in financiamentos]
        fin_selecionado = st.selectbox("Selecione o financiamento:", nomes_fin)
        fin_id = next(f['id'] for f in financiamentos if f['nome'] == fin_selecionado)
        
        st.markdown("---")
        
        # ====== ABAS ======
        tab1, tab2 = st.tabs(["➕ Novo Aporte", "📋 Ver Aportes"])
        
        with tab1:
            st.subheader("Adicionar Novo Aporte")
            
            with st.form("novo_aporte"):
                col1, col2 = st.columns(2)
                
                with col1:
                    numero_parcela = st.number_input(
                        "Número da Parcela",
                        min_value=1,
                        value=3,
                        step=1
                    )
                    valor_aporte = st.number_input(
                        "Valor do Aporte (R$)",
                        min_value=50.0,
                        value=500.0,
                        step=50.0
                    )
                
                with col2:
                    origem = st.selectbox(
                        "Origem do Aporte",
                        ["revenda", "salário", "bonus", "manual"]
                    )
                    descricao = st.text_input("Descrição", "Venda de acessórios")
                
                st.warning("""
                ⚠️ **Importante:** Quanto MAIS CEDO você fizer o aporte, 
                MAIS juros economiza! Aporte na parcela 3 economiza mais que na parcela 10.
                """)
                
                submitted = st.form_submit_button("✅ Adicionar Aporte", use_container_width=True)
                
                if submitted:
                    try:
                        aporte_id = sistema.adicionar_aporte(
                            fin_id,
                            numero_parcela=numero_parcela,
                            valor_aporte=valor_aporte,
                            origem=origem,
                            descricao=descricao
                        )
                        st.success(f"✅ Aporte adicionado! (ID: {aporte_id})")
                        
                        # Simular impacto
                        meses, economia = sistema.simular_aporte_venda(fin_id, valor_aporte, numero_parcela)
                        st.info(f"💰 Impacto: **{meses} mês(es)** economizados | **R$ {economia:.2f}** em juros")
                    except Exception as e:
                        st.error(f"❌ Erro: {e}")
        
        with tab2:
            st.subheader("Seus Aportes")
            
            aportes = sistema.bd.obter_aportes(fin_id)
            
            if aportes:
                df = pd.DataFrame(aportes)
                df['data_aporte'] = pd.to_datetime(df['data_aporte']).dt.strftime('%d/%m/%Y')
                df = df[['numero_parcela', 'valor_aporte', 'origem', 'descricao', 'data_aporte']]
                df.columns = ['Parcela', 'Valor (R$)', 'Origem', 'Descrição', 'Data']
                
                st.dataframe(df, use_container_width=True)
                
                total = sistema.bd.total_aportes(fin_id)
                st.success(f"💰 Total de Aportes: **R$ {total:,.2f}**")
            else:
                st.info("Nenhum aporte registrado ainda.")
        
        st.markdown("---")
        
        # ====== REGISTRAR VENDA ======
        st.subheader("🛍️ Registrar Venda (Rápido)")
        st.markdown("Vendeu algo? Registre aqui para criar um aporte automaticamente!")
        
        with st.form("registrar_venda"):
            col1, col2 = st.columns(2)
            
            with col1:
                valor_venda = st.number_input("Valor da Venda (R$)", min_value=50.0, value=300.0, step=50.0)
                numero_parcela_venda = st.number_input("Qual parcela amortizar?", min_value=1, value=5)
            
            with col2:
                produto = st.text_input("O que vendeu?", "Correia de transmissão")
                descricao_venda = st.text_input("Descrição adicional", "")
            
            submitted_venda = st.form_submit_button("🚀 Registrar Venda + Aporte", use_container_width=True)
            
            if submitted_venda:
                try:
                    entrada_id, aporte_id = sistema.registrar_venda_e_aporte(
                        fin_id,
                        valor_venda=valor_venda,
                        numero_parcela=numero_parcela_venda,
                        descricao=descricao_venda or produto,
                        produto_vendido=produto
                    )
                    
                    meses, economia_venda = sistema.simular_aporte_venda(fin_id, valor_venda, numero_parcela_venda)
                    
                    st.success(f"✅ Venda registrada e aporte criado!")
                    st.balloons()
                    st.info(f"""
                    📊 **Impacto desta venda:**
                    - **{meses} mês(es)** economizados
                    - **R$ {economia_venda:.2f}** em juros poupados
                    """)
                except Exception as e:
                    st.error(f"❌ Erro: {e}")

# ============================================================================
# PÁGINA: SIMULADOR
# ============================================================================

elif pagina == "📈 Simulador":
    st.title("📈 Simulador de Cenários")
    
    financiamentos = sistema.bd.listar_financiamentos(apenas_ativos=True)
    
    if not financiamentos:
        st.warning("⚠️ Nenhum financiamento cadastrado!")
    else:
        nomes_fin = [f"{f['nome']}" for f in financiamentos]
        fin_selecionado = st.selectbox("Selecione o financiamento:", nomes_fin)
        fin_id = next(f['id'] for f in financiamentos if f['nome'] == fin_selecionado)
        
        st.markdown("---")
        
        st.subheader("🎯 Simule Diferentes Cenários")
        
        col_sim1, col_sim2, col_sim3 = st.columns(3)
        
        with col_sim1:
            valor_simulado = st.slider(
                "Valor de Venda (R$)",
                min_value=50,
                max_value=2000,
                value=300,
                step=50
            )
        
        with col_sim2:
            parcela_simulada = st.slider(
                "Aplicar na Parcela",
                min_value=1,
                max_value=60,
                value=5,
                step=1
            )
        
        with col_sim3:
            st.empty()
        
        # Executar simulação
        try:
            meses_sim, economia_sim = sistema.simular_aporte_venda(fin_id, valor_simulado, parcela_simulada)
            
            # Resultados
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.metric(
                    "Meses Economizados",
                    f"{meses_sim} meses",
                    f"Com aporte de R$ {valor_simulado:.0f}"
                )
            
            with col_res2:
                st.metric(
                    "Juros Poupados",
                    f"R$ {economia_sim:,.2f}",
                    f"Economia total"
                )
            
            st.markdown("---")
            
            # Comparação com múltiplos valores
            st.subheader("📊 Comparar Múltiplos Cenários")
            
            valores_teste = [100, 200, 300, 500, 1000]
            resultados_sim = []
            
            for valor in valores_teste:
                m, e = sistema.simular_aporte_venda(fin_id, valor, parcela_simulada)
                resultados_sim.append({
                    'Valor de Venda': f"R$ {valor:.0f}",
                    'Meses Economizados': m,
                    'Juros Poupados': f"R$ {e:.2f}"
                })
            
            df_comparacao = pd.DataFrame(resultados_sim)
            st.dataframe(df_comparacao, use_container_width=True)
            
            # Gráfico comparativo
            fig_sim = px.bar(
                x=[v.replace('R$ ', '').replace('.0f', '') for v in df_comparacao['Valor de Venda']],
                y=df_comparacao['Meses Economizados'],
                labels={'x': 'Valor de Venda', 'y': 'Meses Economizados'},
                title="Impacto de Diferentes Valores"
            )
            st.plotly_chart(fig_sim, use_container_width=True)
            
        except Exception as e:
            st.error(f"❌ Erro na simulação: {e}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p style='color: #666;'>
        🏍️ <b>Financiando v1.0</b> | 
        Sistema de Amortização Acelerada para Moto
    </p>
    <p style='font-size: 12px; color: #999;'>
        Desenvolvido em 3 de fevereiro de 2026 | 
        <a href='#'>GitHub</a> | 
        <a href='#'>Suporte</a>
    </p>
</div>
""", unsafe_allow_html=True)
