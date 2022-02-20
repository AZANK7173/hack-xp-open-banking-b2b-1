import pandas as pd
import warnings
warnings.filterwarnings("ignore")

#Tabela Investimento
def time_process(date):
    return date.strftime("%D")

data = pd.read_csv('src/data/all_users_and_products.csv')
clients = ['JOSE', 'JOAO', 'FRANCISCO', 'CARLOS','SARA','MARTA', 'JULIANA', 'MARCIA']
client_data = data[data['client_name'].isin(clients)]
client_data['acquisitionDate'] = pd.to_datetime(client_data['acquisitionDate']).copy()
client_data = client_data.sort_values(by="acquisitionDate", ascending=False)
st_table = client_data.drop(columns=['bankId','profitability','ticker','Unnamed: 0','investment_id', 'dueDate', 'risk',
    'value','name','description', 'client_id', 'type', 'volumn']).iloc[1:9]
st_table = st_table.iloc[1:, :]
st_table.set_index('identity', inplace=True)
st_table.reset_index(drop=True, inplace=True)
st_table['acquisitionDate'] = st_table['acquisitionDate'].apply(time_process)
st_table.columns = ['Data da Aquisição','Volume Compra','Cliente','Investimento','Porcentagem']


#Tabela Conta Corrente
from src.api_communication import XpDataApi
import os
import pandas as pd

#client_id = os.environ.get('HACK_XP_CLIENT_ID')
client_id = 'XUShAWJwg3hGSuu86xvT0fFv0DAWdRkAWXvsvE5YLN9v1aG2'
#client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
client_secret = 'oOHtUfak8mQPpyA07taGGvNbRwujxlqLlFBamb0bvOwSSLDn1yrGlI7T3rzJXskB'
clients = ['JOSE', 'JOAO', 'FRANCISCO', 'CARLOS','SARA','MARTA', 'JULIANA', 'MARCIA']
api = XpDataApi(client_id=client_id, client_secret=client_secret)

def get_mov_cc(clients):
    data = []
    for name in clients:
        dic = api.get_banking_user_account(name)
        for tras in dic:
            tras['description']=name
            data.append(tras)

    df = pd.DataFrame(data)
    df = df.sort_values(by='date',ascending=False)
    df.columns = ['Tipo de Transação','Cliente','Volume','Data da Transação']

    return df.head(8)

st_table_cc = get_mov_cc(clients)
st_table_cc['Data da Transação'] = pd.to_datetime(st_table_cc['Data da Transação'])
st_table_cc['Data da Transação'] = st_table_cc['Data da Transação'].apply(time_process)
st_table_cc = st_table_cc[['Data da Transação','Volume','Cliente','Tipo de Transação']]


#Balanço
import os
clients = ['JOSE', 'JOAO','SARA', 'JULIANA']

lista = []
for client in clients:
    balance = api.get_banking_user_account_balance(client)
    lista.append((client,balance))
