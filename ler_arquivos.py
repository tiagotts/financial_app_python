import ofxparse
import os 
import pandas as pd

def parse_valor(valor):
    # Remove espaços e "R$"
    valor = valor.replace("R$", "").replace(" ", "")
    # Captura o sinal negativo em qualquer posição
    negativo = '-' in valor
    valor = valor.replace("-", "")
    # Remove pontos e troca vírgula por ponto
    valor = valor.replace(".", "").replace(",", ".")
    valor_float = float(valor)
    return -valor_float if negativo else valor_float

def get_ofx_dataframe():
    resultado = pd.DataFrame()
    transaction_data = []
    for extrato in os.listdir('./ofx'):
        with open(f'ofx/{extrato}', encoding='ascii', errors='ignore') as ofx_file:
            ofx = ofxparse.OfxParser.parse(ofx_file)

        for account in ofx.accounts:
            for transaction in account.statement.transactions:
                transaction_data.append({
                    "Data": transaction.date,
                    "Descricao": transaction.memo,
                    "Valor": transaction.amount,
                })

    resultado = pd.concat([resultado, pd.DataFrame(transaction_data)])
    resultado["Valor"] = resultado["Valor"].astype(float)
    resultado["Descricao"] = resultado["Descricao"]
    resultado["Data"] = pd.to_datetime(resultado["Data"], format='%Y-%m-%d').dt.strftime('%d/%m/%Y')
    return resultado

def read_csv_dataframe():
    resultado = pd.DataFrame()
    for extrato in os.listdir('./csv'):
        with open(f'csv/{extrato}', encoding='ascii', errors='ignore') as csv_file:
            df = pd.read_csv(csv_file, delimiter=';')
            resultado['Data'] = pd.to_datetime(df["Data"]).dt.strftime('%d/%m/%Y')
            resultado['Descricao'] = df['Estabelecimento']
            resultado['Valor'] = df['Valor'].apply(parse_valor)
            return resultado
        
def get_csv():
    df_csv = read_csv_dataframe()
    df_ofx = get_ofx_dataframe()
    df_final = pd.concat([df_ofx, df_csv])
    df_final = df_final.reset_index(drop=True)
    # df_final.to_csv("./resultado/data_concat.csv", index=False)
    # df_final.to_excel("./resultado/data_concat.xlsx", index=False)
    return df_final

get_csv()
