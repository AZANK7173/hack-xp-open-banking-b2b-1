from src.api_communication import XpDataApi
import pandas as pd
import plotly.graph_objects as go
import numpy as np

class Report: 

    def __init__(self, api, client_name, download_dataset=False):
        self.api = api
        self.product_names = ['cdb', 'lci', 'lca', 'cri', 'cra', 'stocks', 'investmentFunds']
        self.column_names = ['identity','bankId','description','type','value','dueDate','profitability','risk','acquisitionDate','volumn','ticker','name']
        self.client_name = client_name

        if download_dataset:
            self.inv_user_df = self._create_user_investment_df()
        else:
            df = pd.read_csv('src/data/dataset.csv', index_col = 1)
            self.inv_user_df = df.loc[df.client_name == self.client_name]

    def _create_user_investment_df(self): 
        user_investments = self.api.get_banking_user_investments(self.client_name)

        inv_user_df = pd.DataFrame(columns=self.column_names)
        for p in self.product_names: 
            for inv in user_investments[p]:
                inv_user_df = inv_user_df.append(inv, ignore_index=True)

        inv_user_df['total_value'] = inv_user_df['value'] * inv_user_df['volumn']
        inv_user_df['client_name'] = self.client_name

        for i in range(20):
            random_sample = inv_user_df.sample()
            inv_user_df = inv_user_df.drop(random_sample.index)

        inv_user_df['investment_name'] = inv_user_df.identity.apply(lambda x: '-'.join(x.split('-')[:3]))
        inv_user_df['inv_pct'] = inv_user_df.groupby('client_name').total_value.apply(lambda x: 100 * x / float(x.sum())).astype('float')  

        return inv_user_df

    def plot_donut_chart_user_investments(self):
        self.inv_user_df['type'] = self.inv_user_df['type'].replace({
                        'fii':'Fundo de Investimento', 
                        'multimercado':'Fundo de Investimento',
                        'renda-fixa':'Fundo de Investimento',
                        'renda-variável':'Fundo de Investimento',
                        np.nan: 'Ações'
                    })

        values = self.inv_user_df.groupby('type').total_value.sum()
        labels = values.index

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors = ['#800080', '#8b9bac' , '#1478a7' , '#a897f9' , '#19507b' , '#c7c96c' , '#bad1ce'])])
        fig.update_traces(hoverinfo='label+percent+name')
        fig.update_layout(title=f"Composição da carteira de {self.client_name}")

        return fig

    def summary_user_invs(self): 
        summary_df = self.inv_user_df[['investment_name', 'type', 'value', 'volumn', 'total_value', 'acquisitionDate', 'dueDate', 'risk']]

        summary_df = summary_df.rename(columns = {
            'type': 'Tipo', 
            'value': 'Valor',
            'volumn': 'Volume', 
            'total_value': 'Total Investido',
            'risk': 'Risco',
            'acquisitionDate': 'Data de Aquisição', 
            'dueDate' : 'Data de Expiração', 
        })

        summary_df = summary_df.set_index('investment_name')
        
        return summary_df