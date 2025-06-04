import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from financial_app import executar_ia

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)
c1, c2 = st.columns([0.6, 0.4])
st.title("Dashboard de Finanças Pessoais")

with st.sidebar:
    uploaded_files = st.file_uploader(
        "Faça upload de um ou mais arquivos CSV ou OFX", 
        accept_multiple_files=True
    )
    process_files = st.button("Enviar arquivos")

if process_files and uploaded_files:
    df = executar_ia(uploaded_files)
    # df = pd.concat(dfs, ignore_index=True)

    df["Mês"] = "Maio"
    df["Data"] = pd.to_datetime(df["Data"], dayfirst=True)
    df["Data"] = df["Data"].apply(lambda x: x.date())
    df["Valor"] = np.where(df["Valor"].astype(float) > 0, df["Valor"].astype(float), df["Valor"].astype(float)*-1)

    st.sidebar.header("Filtros")
    mes = st.sidebar.selectbox("Mês", df["Mês"].unique())
    categories = df["Categoria"].unique().tolist()
    selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

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
    st.write(f"Total de Gastos: R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    c1.dataframe(df_final)

    st.write("")
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
    c2.plotly_chart(fig, use_container_width=True, key='pie_chart')

elif not uploaded_files:
    st.info("Por favor, selecione pelo menos um arquivo para enviar.")
else:
    st.info("Clique em 'Enviar arquivos' para processar os arquivos selecionados.")