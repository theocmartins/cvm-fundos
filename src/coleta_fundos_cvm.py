import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile
from tqdm import tqdm
import pandas as pd

url = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"


BASE_URL = "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/"

def baixar_cadastro_fundos():
    url = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
    df = pd.read_csv(url, sep=';', encoding='latin1', low_memory=False)
    df = df[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'CLASSE']]
    print(df.head())
    return df


def baixar_dados_mes(ano_mes):
    url_zip = f"{BASE_URL}/inf_diario_fi_{ano_mes}.zip"
    r = requests.get(url_zip)
    if r.status_code != 200:
        print(f"Dados não encontrados para {ano_mes}")
        return pd.DataFrame()

    with ZipFile(BytesIO(r.content)) as z:
        csv_name = [name for name in z.namelist() if name.endswith('.csv')][0]
        
        with z.open(csv_name) as f:
            df = pd.read_csv(f, sep=';', encoding='latin1', low_memory=False)
            print(f"Colunas disponíveis em {ano_mes}:")
            print(df.columns)
            print(f"Número de linhas em {ano_mes}: {len(df)}")





    df = df[['CNPJ_FUNDO_CLASSE', 'DT_COMPTC', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'CAPTC_DIA', 'RESG_DIA']]
    df.columns = ['cnpj', 'data', 'valor_cota', 'patrimonio', 'aportes', 'resgates']
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')
    return df

def coletar_dados_cvm(meses: list):
    print("Baixando cadastro de fundos...")
    df_cadastro = baixar_cadastro_fundos()

    print("Baixando dados mensais...")
    dados_todos = []
    for mes in tqdm(meses):
        print("Baixando dados para o mês:", mes)
        if len(mes) != 6 or not mes.isdigit() or mes < '202401':
            print(f"Mês inválido: {mes}. Deve ter o formato 'YYYYMM' e ser a partir de janeiro de 2024.")
            continue

        df_mes = baixar_dados_mes(mes)
        if not df_mes.empty:
            dados_todos.append(df_mes)

    if not dados_todos:
        print("Nenhum dado foi coletado.")
        return pd.DataFrame()

    df_total = pd.concat(dados_todos, ignore_index=True)
    print("Criando dataframe consolidado...")
    df_total = df_total.merge(df_cadastro, how='left', left_on='cnpj', right_on='CNPJ_FUNDO')
    df_total.drop(columns='CNPJ_FUNDO', inplace=True)

    return df_total[['data', 'cnpj', 'DENOM_SOCIAL', 'CLASSE', 'valor_cota', 'patrimonio', 'aportes', 'resgates']]

if __name__ == "__main__":
    meses = ['202404', '202405']
    df_fundos = coletar_dados_cvm(meses)
    
    import os

    # Cria o diretório 'dados' se ele não existir
    os.makedirs("dados", exist_ok=True)

    df_fundos.to_csv("dados/fundos_abril_maio_2024.csv", index=False)
    print(df_fundos.head())

