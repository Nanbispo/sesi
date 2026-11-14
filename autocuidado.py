import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard - Saúde no Trabalho", layout="wide")
st.title("📊 Dashboard: Saúde e Autocuidado no Ambiente de Trabalho")
st.markdown("Visualização interativa das respostas da pesquisa.")

# 2. Carregamento dos Dados
nome_arquivo = "respostas.xlsx"

@st.cache_data
def carregar_dados(arquivo):
    return pd.read_excel(arquivo)

# Tenta carregar automaticamente se o arquivo estiver na mesma pasta, senão pede upload
if os.path.exists(nome_arquivo):
    df = carregar_dados(nome_arquivo)
else:
    uploaded_file = st.file_uploader("Planilha não encontrada. Faça o upload do arquivo Excel:", type=["xlsx"])
    if uploaded_file is not None:
        df = carregar_dados(uploaded_file)
    else:
        st.warning(f"Por favor, coloque o arquivo '{nome_arquivo}' na mesma pasta deste script ou faça o upload.")
        st.stop()

# 3. Barra Lateral (Filtros)
st.sidebar.header("Filtros Interativos")
col_setor = '1. Em qual setor da indústria você trabalha?'
setores = df[col_setor].dropna().unique().tolist()
setor_selecionado = st.sidebar.multiselect("Filtrar por Setor:", setores, default=setores)

# Aplicando o filtro na base de dados
df_filtrado = df[df[col_setor].isin(setor_selecionado)]

# 4. Indicadores Principais (KPIs)
st.subheader("Visão Geral")
col1, col2 = st.columns(2)
col1.metric("Total de Respostas", len(df_filtrado))
col2.metric("Setores Filtrados", len(setor_selecionado))

st.markdown("---")

# 5. Gráficos Interativos
colA, colB = st.columns(2)

# Gráfico 1: Turno de Trabalho
col_turno = '2. Qual é o seu turno de trabalho?'
fig_turno = px.pie(df_filtrado, names=col_turno, title="Distribuição por Turno de Trabalho", hole=0.4)
colA.plotly_chart(fig_turno, use_container_width=True)

# Gráfico 2: Frequência de Cuidado com a Saúde
col_freq = '4. Com que frequência você consegue dedicar tempo ao cuidado com sua saúde?'
freq_counts = df_filtrado[col_freq].value_counts().reset_index()
freq_counts.columns = [col_freq, 'Quantidade']
fig_freq = px.bar(freq_counts, x=col_freq, y='Quantidade', title="Frequência de Cuidado com a Saúde", text_auto=True)
colB.plotly_chart(fig_freq, use_container_width=True)

# Gráfico 3: Influência do Trabalho
st.markdown("---")
col_influencia = '8. Como o seu trabalho influencia sua capacidade de cuidar da saúde?'
fig_influencia = px.pie(df_filtrado, names=col_influencia, title="Impacto do Trabalho na Capacidade de Cuidado", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_influencia, use_container_width=True)

# 6. Visualização da Tabela de Dados
st.markdown("---")
st.subheader("Dados Detalhados")
with st.expander("Clique aqui para visualizar e exportar a planilha filtrada"):
    st.dataframe(df_filtrado)