import streamlit as st
import pandas as pd
import plotly.express as px

# ========================
# Configuração inicial
# ========================
st.set_page_config(page_title="Contratos Financeiros", layout="wide")

# ========================
# Carregar dados
# ========================
clientes = pd.read_csv("data/clientes.csv")
contratos = pd.read_csv("data/contratos.csv")
pagamentos = pd.read_csv("data/pagamentos.csv")

# Juntar dados principais
df = contratos.merge(clientes, on="cliente_id")
df_pag = pagamentos.merge(df, on="id_contrato")

# ========================
# Layout
# ========================
st.title("📊 Dashboard de Contratos e Pagamentos - Piauí")
st.divider()

# ========================
# Filtros
# ========================
st.sidebar.header("Filtros")
cidade_filtro = st.sidebar.multiselect("Selecione a cidade", sorted(df['cidade'].unique()))
setor_filtro = st.sidebar.multiselect("Selecione o setor", sorted(df['setor'].unique()))
status_filtro = st.sidebar.multiselect("Selecione o status do contrato", sorted(df['status'].unique()))

df_filtrado = df_pag.copy()
if cidade_filtro:
    df_filtrado = df_filtrado[df_filtrado['cidade'].isin(cidade_filtro)]
if setor_filtro:
    df_filtrado = df_filtrado[df_filtrado['setor'].isin(setor_filtro)]
if status_filtro:
    df_filtrado = df_filtrado[df_filtrado['status'].isin(status_filtro)]

# Caso não haja dados após filtro
if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# ========================
# KPIs
# ========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Receita Total", f"R$ {df_filtrado['valor_pago'].sum():,.2f}", border=True)
col2.metric("Ticket Médio", f"R$ {df_filtrado['valor_pago'].mean():,.2f}", border=True)
col3.metric("Contratos Ativos", df_filtrado[df_filtrado['status']== 'Ativo']['id_contrato'].nunique(), border=True)

inad_pct = (len(df_filtrado[df_filtrado['status_pagamento']=='Atrasado']) / len(df_filtrado)) * 100
col4.metric("Inadimplência", f"{inad_pct:.1f}%", border=True)

st.divider()

# ========================
# Gráficos Interativos
# ========================

# Função para mostrar números completos com R$
def plotly_reais(fig, eixo_x=True, eixo_y=True):
    layout_update = {}
    if eixo_x:
        layout_update['xaxis'] = dict(tickprefix="R$ ", separatethousands=True)
    if eixo_y:
        layout_update['yaxis'] = dict(tickprefix="R$ ", separatethousands=True)
    fig.update_layout(**layout_update)
    return fig

# Linha 1: Receita por cidade e Receita por setor
st.subheader("📍 Receita por Cidade x Receita por Setor")
col1, col2 = st.columns(2)

with col1:
    receita_cidade = (
        df_filtrado.groupby("cidade")["valor_pago"]
        .sum()
        .reset_index()
        .sort_values(by="valor_pago", ascending=False)
        .head(10)
    )
    fig1 = px.bar(
        receita_cidade,
        x="valor_pago",
        y="cidade",
        orientation="h",
        text=receita_cidade["valor_pago"]  # aqui passamos explicitamente os valores
    )
    fig1 = plotly_reais(fig1, eixo_x=True, eixo_y=False)
    fig1.update_traces(texttemplate="R$ %{text:,.2f}")  # agora funciona corretamente
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    receita_setor = df_filtrado.groupby("setor")["valor_pago"].sum().reset_index()
    fig2 = px.bar(
        receita_setor,
        x="setor",
        y="valor_pago",
        text=receita_setor["valor_pago"]  # explicitamente
    )
    fig2 = plotly_reais(fig2)
    fig2.update_traces(texttemplate="R$ %{text:,.2f}")
    st.plotly_chart(fig2, use_container_width=True)

# Linha 2: Formas de pagamento e Evolução temporal
st.subheader("💳 Formas de Pagamento x Evolução Temporal")
col3, col4 = st.columns(2)

with col3:
    formas = df_filtrado["forma_pagamento"].value_counts().reset_index()
    formas.columns = ["forma_pagamento", "qtd"]
    fig3 = px.pie(
        formas,
        names="forma_pagamento",
        values="qtd",
        title="Formas de Pagamento"
    )
    fig3.update_traces(texttemplate="%{label}: R$ %{value:,.2f}")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    df_filtrado["data_pagamento"] = pd.to_datetime(df_filtrado["data_pagamento"])
    pag_tempo = (
        df_filtrado.groupby(df_filtrado["data_pagamento"].dt.to_period("M"))["valor_pago"]
        .sum()
        .reset_index()
    )
    pag_tempo["data_pagamento"] = pag_tempo["data_pagamento"].astype(str)
    fig4 = px.line(
        pag_tempo,
        x="data_pagamento",
        y="valor_pago",
        markers=True,
        text=pag_tempo["valor_pago"],  # passar explicitamente
        title="Evolução da Receita Mensal"
    )
    fig4 = plotly_reais(fig4, eixo_y=True, eixo_x=False)
    fig4.update_traces(texttemplate="R$ %{text:,.2f}")
    st.plotly_chart(fig4, use_container_width=True)


