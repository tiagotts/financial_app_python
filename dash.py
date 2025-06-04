import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import numpy as np

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)
mes_atual = datetime.datetime.now().strftime("%B")
df = pd.read_csv(f"./data_{mes_atual}.csv")
# df["Mês"] = df["Data"].apply(lambda x: "-".join(x.split("-")[:-1]))
# df["Mês"] =datetime.now().strftime('%m')  # '06'
df["Mês"] = "Maio"
df["Data"] = pd.to_datetime(df["Data"])
df["Data"] = df["Data"].apply(lambda x: x.date())
df["Valor"] = np.where(df["Valor"].astype(float) > 0, df["Valor"].astype(float), df["Valor"].astype(float)*-1)

def filter_data(df, mes, selected_categories):
    df_filtered = df[df['Mês'] == mes]
    if selected_categories:
        df_filtered = df_filtered[df_filtered['Categoria'].isin(selected_categories)]
    return df_filtered

# Título do Dashboard
st.title("Dashboard de Finanças Pessoais")

# Filtros de data
st.sidebar.header("Filtros")

# Definir intervalo de data
mes = st.sidebar.selectbox("Mês", df["Mês"].unique())

# Filtro de categoria
categories = df["Categoria"].unique().tolist()
selected_categories = st.sidebar.multiselect("Filtrar por Categorias", categories, default=categories)

df_filtered = filter_data(df, mes, selected_categories)
total = df_filtered["Valor"].sum()
total_row = pd.DataFrame({
    "Categoria": ["TOTAL"],
    "Valor": [total]
})

# ====================
c1, c2 = st.columns([0.6, 0.4])
df_final = pd.concat([df_filtered, total_row], ignore_index=True)
c1.dataframe(df_final)

st.write("")  # Optional: add a header or space
category_distribution = df_filtered.groupby("Categoria")["Valor"].sum().reset_index()
fig = px.pie(category_distribution, values='Valor', names='Categoria', 
            title='Distribuição por Categoria', hole=0.3)

c2.plotly_chart(fig, use_container_width=True, key='pie_chart')

df_filtered = filter_data(df, mes, selected_categories)