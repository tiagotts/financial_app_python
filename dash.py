import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os
from financial_app import executar_ia

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)

mes = "Selecione..."
meses = ['Selecione...','Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
st.title("Dashboard de Finanças Pessoais")
c1, c2 = st.columns([0.65, 0.35])
df = pd.DataFrame()

def atualizar_tabela_grafico(df, mes):
    selected_categories = st.session_state.get("multiselect_categorias", df["Categoria"].unique().tolist())
    df["Valor"] = np.where(df["Valor"].astype(float) > 0, df["Valor"].astype(float), df["Valor"].astype(float)*-1)
    def filter_data(df, mes, selected_categories):
        df_filtered = df[df['Mês'] == mes]
        if selected_categories:
            df_filtered = df_filtered[df_filtered['Categoria'].isin(selected_categories)]
        return df_filtered

    df_filtered = filter_data(df, mes, selected_categories)
    total = df_filtered["Valor"].sum()
    total_row = pd.DataFrame({
        "Categoria": ["TOTAL"],
        "Valor": [total]
    })
    df_final = pd.concat([df_filtered, total_row], ignore_index=True)
    if 'table_placeholder' not in st.session_state:
        st.session_state['table_placeholder'] = c1.empty()
    st.session_state['table_placeholder'].dataframe(df_final)

    category_distribution = df_filtered.groupby("Categoria")["Valor"].sum().reset_index()
    category_distribution["CategoriaValor"] = category_distribution.apply(
        lambda row: f"{row['Categoria']} (R$ {row['Valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + ")", axis=1)
    fig = px.pie(
        category_distribution,
        values='Valor',
        names='CategoriaValor',  
        title='Distribuição por Categoria',
        hole=0.3
    )
    if 'chart_placeholder' not in st.session_state:
        st.session_state['chart_placeholder'] = c2.empty()
    st.session_state['chart_placeholder'].plotly_chart(fig, use_container_width=True)

    if 'total_placeholder' not in st.session_state:
        st.session_state['total_placeholder'] = st.empty()
    st.session_state['total_placeholder'].write(f"Total de Gastos: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

def montarTela():
    df["Mês"] = mes
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df["Data"] = df["Data"].apply(lambda x: x.date())
    df["Valor"] = np.where(df["Valor"].astype(float) > 0, df["Valor"].astype(float), df["Valor"].astype(float)*-1)

    st.sidebar.header("Filtros")
    categories = df["Categoria"].unique().tolist()
    st.sidebar.multiselect(
        "Filtrar por Categorias",
        categories,
        default=categories,
        key=f"multiselect_categorias"
    )
    atualizar_tabela_grafico(df, mes)

with st.sidebar:
    mes = st.sidebar.selectbox("Mês de referência para avaliar", meses, key="mes_selecionado", accept_new_options=False)
    uploaded_files = st.file_uploader(
        "Faça upload de um ou mais arquivos CSV ou OFX", 
        accept_multiple_files=True
    )
    process_files = st.button("Enviar arquivos")


def selecionar_arquivo_existente():
    arquivo = st.session_state["arquivo_selecionado"]
    st.session_state["df"] = pd.read_csv(f'./arquivos/{arquivo}')
    
arquivos_csv = []
for item in os.listdir('./arquivos'):
    if item.lower().endswith('.csv'):
        arquivos_csv.append(item)

arquivo_gerado = st.sidebar.selectbox("Arquivos", arquivos_csv, key='arquivo_selecionado', on_change=selecionar_arquivo_existente)

if arquivos_csv:
    df = pd.read_csv(f'./arquivos/{arquivo_gerado}')
    mes = arquivo_gerado.replace("data_", "").replace(".csv", "")
    montarTela()

if (process_files and uploaded_files and mes):
    if mes == "Selecione...":
        st.warning("Por favor, selecione um mês de referência para continuar.")
    else:
        df = pd.DataFrame()
        df = executar_ia(uploaded_files, mes)
        atualizar_tabela_grafico(df, mes)
    if not uploaded_files:
        st.info("Por favor, selecione pelo menos um arquivo para enviar.")



