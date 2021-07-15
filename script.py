import requests
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import datetime


def formatando_data(data):
    nova_data = datetime.date.fromisoformat(data)
    return nova_data.strftime("%d/%m/%Y")


url = 'https://github.com/owid/covid-19-data/tree/master/public/data'
resposta = requests.get(url)
soup = BeautifulSoup(resposta.text, 'html.parser')
url_dowload_xlsx = soup.find(class_='markdown-body entry-content container-lg').h3.findAll('a')[2]['href']

urllib.request.urlretrieve(url_dowload_xlsx, 'owid-covid-data.xlsx')
df_covid = pd.read_excel('owid-covid-data.xlsx')

df_covid_brasil = df_covid[df_covid.location == 'Brazil'][['date', 'total_deaths', 'new_deaths']]
df_covid_brasil.reset_index(drop=True, inplace=True)

df_covid_brasil.rename(columns={'date': 'Data', 'total_deaths': 'Total de Mortes', 'new_deaths': 'Novas Mortes no Dia'}, inplace=True)

df_covid_brasil['Data'] = df_covid_brasil['Data'].apply(formatando_data)

df_covid_brasil.dropna(inplace=True)
df_covid_brasil.reset_index(drop=True, inplace=True)

df_covid_brasil.to_csv('convid_brasil.csv', index=False)

df_covid_brasil['Variacao Anual Total de Mortes'] = pd.Series(dtype='float64')
df_covid_brasil['Variacao Anual Novas Mortes'] = pd.Series(dtype='float64')

for aux in df_covid_brasil.itertuples():
    dado_ano_anterior = df_covid_brasil.loc[aux.Index]
    ano_atual = str(int(dado_ano_anterior['Data'][-4:]) + 1)
    data_atual = dado_ano_anterior['Data'][:-4] + ano_atual

    indice_data_atual = df_covid_brasil.index[df_covid_brasil['Data'].str.find(data_atual) != -1].tolist()

    if len(indice_data_atual) == 1:
        dado_ano_atual = df_covid_brasil.loc[indice_data_atual[0]]
        df_covid_brasil.loc[indice_data_atual[0], 'Variacao Anual Total de Mortes'] = ((dado_ano_atual['Total de Mortes'] / dado_ano_anterior['Total de Mortes']) - 1) * 100
        df_covid_brasil.loc[indice_data_atual[0], 'Variacao Anual Novas Mortes'] = ((dado_ano_atual['Novas Mortes no Dia'] / dado_ano_anterior['Novas Mortes no Dia']) - 1) * 100
        if indice_data_atual[0] == (len(df_covid_brasil) - 1):
            break

df_covid_brasil.to_csv('convid_brasil_com_variacao_anual.csv', index=False)
