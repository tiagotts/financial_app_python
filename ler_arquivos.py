import ofxparse
import io
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

def read_ofx_dataframe(fileOfx):
    resultado = pd.DataFrame()
    transaction_data = []
    # for extrato in os.listdir('./ofx'):
    # with open(fileOfx.read(), encoding='ascii', errors='ignore') as ofx_file:
    #     ofx = ofxparse.OfxParser.parse(ofx_file)
    content = fileOfx.read().decode('ascii', errors='ignore')
    ofx = ofxparse.OfxParser.parse(io.StringIO(content))

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

def read_csv_dataframe(fileCSV):
    resultado = pd.DataFrame()
    # with open(fileCSV, encoding='ascii', errors='ignore') as csv_file:

    df = pd.read_csv(fileCSV, delimiter=';')
    resultado['Data'] = pd.to_datetime(df["Data"]).dt.strftime('%d/%m/%Y')
    resultado['Descricao'] = df['Estabelecimento']
    resultado['Valor'] = df['Valor'].apply(parse_valor)
    return resultado
        
def get_csv():
    df_csv = read_csv_dataframe()
    df_ofx = read_ofx_dataframe()
    df_final = pd.concat([df_ofx, df_csv])
    df_final = df_final.reset_index(drop=True)
    # df_final.to_csv("./resultado/data_concat.csv", index=False)
    # df_final.to_excel("./resultado/data_concat.xlsx", index=False)
    return df_final

def convert_csv_ofx(file):
    resultado = pd.DataFrame()
    if file.name.endswith('.csv'):
        resultado = read_csv_dataframe(file)
    elif file.name.endswith('.ofx'):
        resultado = read_ofx_dataframe(file)

    return resultado