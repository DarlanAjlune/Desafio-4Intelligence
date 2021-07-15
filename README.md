# Desafio-4Intelligence
 
Para explicar meu código irei separar em tópicos:

1. Importação das Bibliotecas:
    
    ```
    import requests
    from bs4 import BeautifulSoup
    import urllib
    import pandas as pd
    import datetime
    ```

    1. Biblioteca requests: utilizo o método get para pegar as informações contida na URL fornecida no PDF.
    
    1. Biblioteca BeautifulSoup: utilizo para conseguir extrair as informações coletadas do método get.

    1. Biblioteca urllib: utilizo para baixar o documento XLSX.

    1. Biblioteca pandas: utilizo para trabalhar com o DataFrame.

    1. Biblioteca datetime: utilizo para formatar a data.

2. Função formatando_data:

    ```
    def formatando_data(data):
        nova_data = datetime.date.fromisoformat(data)
        return nova_data.strftime("%d/%m/%Y")
    ```
    Esta função recebe uma string data no formato YYYY-MM-DD e retorna uma string no formato DD/MM/YYYY.

3. Acessar GitHub e buscar URL do Arquivo:

    ```
    url = 'https://github.com/owid/covid-19-data/tree/master/public/data'
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    url_dowload_xlsx = soup.find(class_='markdown-body entry-content container-lg').h3.findAll('a')[2]['href']
    ```
    Na variável resposta salvo as informações coletadas na url informada. Depois crio a variável soup, que irá auxiliar na busca da url capaz de baixar o arquivo .xlsx.  
    No processo de busca desta url, especifico o caminho todo, ou seja, primeiro acho a primeira classe que contém aquele nome, acesso a tag h3 contida nessa classe, busco todas as tags a, pego a terceira tag a encontrada e acesso o atributo href, onde se encontra a url desejada.

4. Baixar Arquivo e Criar DataFrame:

    ```
    urllib.request.urlretrieve(url_dowload_xlsx, 'owid-covid-data.xlsx')
    df_covid = pd.read_excel('owid-covid-data.xlsx')
    ```
    Para baixar o arquivo passo a url e o nome que este ficará salvo. Depois de baixar, crio o DataFrame lendo o arquivo baixado.

5. Filtrar Dados:

    ```
    df_covid_brasil = df_covid[df_covid.location == 'Brazil'][['date', 'total_deaths', 'new_deaths']]
    df_covid_brasil.reset_index(drop=True, inplace=True)
    ```
    Na variável df_covid_brasil estou salvando as colunas date, total_deaths e new_deaths em que a localização seja igual a Brazil. Depois reseto os index para ficar na ordem correta, ou seja, de 0 até n.

6. Renomear Colunas:

    ```
    df_covid_brasil.rename(columns={'date': 'Data', 'total_deaths': 'Total de Mortes', 'new_deaths': 'Novas Mortes no Dia'}, inplace=True)
    ```
    Renomeando nome das colunas do DataFrame.

7. Formatar Data:

    ```
    df_covid_brasil['Data'] = df_covid_brasil['Data'].apply(formatando_data)
    ```
    A função apply será responsável por percorrer meu DataFrame na coluna Data e para cada linha ela chama a função formatando_data.  
    Como esta função tem retorno, será alterado o formato antigo pelo novo.

8. Apagar Dados Faltantes:

    ```
    df_covid_brasil.dropna(inplace=True)
    df_covid_brasil.reset_index(drop=True, inplace=True)
    ```
    Apago todos os dados faltantes e reseto novamente os índices do DataFrame.

9. Salvar CSV:

    ```
    df_covid_brasil.to_csv('convid_brasil.csv', index=False)
    ```

10. Cálculo da Variação Anual:

    ```
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

    ```

    Inicialmente crio novas colunas do tipo float64 e vazias. Em seguida percorro meu DataFrame.  
    Para facilitar, em dado_ano_anterior salvo a linha que estou analisando naquele momento. Pego apenas o ano dessa data, acrescento 1 e depois crio minha data_atual. Depois disso, busco no DataFrame o índice desta nova data e salvo em indice_data_atual.
    > OBS.: indice_data_atual poderá ser vazio(caso não encontre no DataFrame) ou conter o índice da linha. Se houver, só terá apenas um índice, devido a construção do dataset fornecido no Github.

    Se encontrou uma data no DataFrame igual a data_atual, eu pego a linha correspondente, salvo em dado_ano_atual e logo em seguida realizo os cálculos para as respectivas colunas.
    > OBS.: Devido a construção do dataset, foi possível analisar que as datas estavam ordenadas. Portanto quando encontrar o índice da última linha do DataFrame, ele irá sair do for, a fim de otimizá-lo.

11. Salvar CSV

    ```
    df_covid_brasil.to_csv('convid_brasil_com_variacao_anual.csv', index=False)
    ```
    Salva outro CSV contendo as variações anuais.