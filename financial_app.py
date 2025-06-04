
from ler_arquivos import get_csv
import datetime
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv, find_dotenv

df = get_csv()

# LLM
_ = load_dotenv(find_dotenv())

template = """
Você é um analista de dados, trabalhando em um projeto de limpeza de dados.
Seu trabalho é escolher uma categoria adequada para cada lançamento financeiro
que vou te enviar.

Todos são transações financeiras de uma pessoa física.

Ignorar as transações de pagamento e nao incluir em nenhuma categoria: por exemplo, PAGAMENTO, PGTO e etc

Escolha uma dentre as seguintes categorias:
- Assinaturas: por exemplo de netflix, MAX, premiere, prime, AWS, GCP, AZURE, etc
- Alimentação
- Saúde
- Mercado: por exemplo, supermercado, DONA DE CASA, BigBox, Oba, Atacadao e etc
- Saúde
- Educação: Por exemplo KIWIFY, universidade, curso Alure, Azimov, Udemy e etc
- Compras: Por exemplo DUTY, ZP, RICHESSE, TRACKFIELD, MULTI NEG, TECNOPAN
_ Roupas: por exemplo, calçados, roupas, calçados, etc
- Farmacia: por exemplo drogarias, farmacia, medicamentos, etc
- Lazer: Musculação, volei, tenis, futebol, ALLPARK, CPQ BRASIL , POMERODE, etc
- Transporte
- Loterica: por exemplo mega sena, lotofácil, quina, LOTERIASONLINETPG
- Investimento
- Transferências para terceiros: exmplo transferencia para o banco
- Telefone
- Moradia
- Saidas Restaurante e Bares: Por exemplo, NAZO, restaurante, bar, DONA JU, SANDO, caminito, churrascaria, TERRASERVA, PAYGO, JARAGUA e etc
- Viagem: por exemplo LATAN, AZUL, GOL, VOE
- Suplementos: por exemplo UNDERLABZ, DUX, creatina, Gorwth, etc
- Zuma: por exemplo relacionado a cachorro, ANIMALE
- Ignoradas
- Taxas: Por exemplo: ANUIDADE 

Escola a categoria deste item:
{text}

Responda apenas com a categoria.
"""
prompt = PromptTemplate.from_template(template=template)
chat = ChatOpenAI(model="gpt-4o-mini")

category = []

chain = prompt | chat | StrOutputParser()
category = chain.batch(list(df["Descricao"].values))
df["Categoria"] = category
df.to_csv("data_completo.csv")
df = df[df['Categoria'] != 'Ignoradas'] 
mes_atual = datetime.datetime.now().strftime("%B")
df.to_csv(f"data_{mes_atual}.csv", index=False)
