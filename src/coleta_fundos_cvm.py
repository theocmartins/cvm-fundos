import pandas as pd
import requests
from io import BytesIO
from zipfile import ZipFile
from tqdm import tqdm

BASE_URL = "https://dados.cvm.gov.br/dados/FI/DOC/INF_DIARIO/DADOS/"

def baixar_cadastro_fundos():
    url = "https://dados.cvm.gov.br/dados/FI/CAD/DADOS/cad_fi.csv"
    df = pd.read_csv(url, sep=';', encoding='latin1')
    df = df[['CNPJ_FUNDO', 'DENOM_SOCIAL', 'CLASSE']]
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
            df = pd.read_csv(f, sep=';', encoding='latin1')

    df = df[['CNPJ_FUNDO', 'DT_COMPTC', 'VL_QUOTA', 'VL_PATRIM_LIQ', 'CAPTC_DIA', 'RESG_DIA']]
    df.columns = ['cnpj', 'data', 'valor_cota', 'patrimonio', 'aportes', 'resgates']
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')
    return df

def coletar_dados_cvm(meses: list):
    print("Baixando cadastro de fundos...")
    df_cadastro = baixar_cadastro_fundos()

    dados_todos = []
    for mes in tqdm(meses):
        df_mes = baixar_dados_mes(mes)
        if not df_mes.empty:
            dados_todos.append(df_mes)

    df_total = pd.concat(dados_todos, ignore_index=True)
    df_total = df_total.merge(df_cadastro, how='left', left_on='cnpj', right_on='CNPJ_FUNDO')
    df_total.drop(columns='CNPJ_FUNDO', inplace=True)

    return df_total[['data', 'cnpj', 'DENOM_SOCIAL', 'CLASSE', 'valor_cota', 'patrimonio', 'aportes', 'resgates']]

if __name__ == "__main__":
    meses = ['202404', '202405']
    df_fundos = coletar_dados_cvm(meses)
    df_fundos.to_csv("dados/fundos_abril_maio_2024.csv", index=False)
    print(df_fundos.head())
