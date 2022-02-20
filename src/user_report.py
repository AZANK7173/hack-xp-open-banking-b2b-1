from api_communication import XpDataApi
import pandas as pd
import plotly.graph_objects as go
import numpy as np

class Report: 

    def __init__(self, api, client_name):
        self.api = api
        self.product_names = ['cdb', 'lci', 'lca', 'cri', 'cra', 'stocks', 'investmentFunds']
        self.client_name = client_name
        self.inv_user_df = self._create_user_investment_df()

    def _create_user_investment_df(self): 
        user_investments  = self.api.get_banking_user_investments(self.client_name)

        column_names = []
        for p in self.product_names: 
            columns = list(user_investments[p][0].keys())
            for c in columns: 
                if c not in column_names: column_names.append(c)

        inv_user_df = pd.DataFrame(columns=column_names)
        for p in self.product_names: 
            for inv in user_investments[p]:
                inv_user_df = inv_user_df.append(inv, ignore_index=True)

        inv_user_df['total_value'] = inv_user_df['value'] * inv_user_df['volumn']
        inv_user_df['client_name'] = self.client_name

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
        fig.update_layout(title=f"Investimentos do {self.client_name}")

        fig.show()

    def summary_user_invs(self): 
        summary_df = self.inv_user_df[['type', 'value', 'volumn', 'total_value', 'acquisitionDate', 'dueDate', 'risk']]

        summary_df = summary_df.rename(columns = {
            'type': 'Tipo', 
            'value': 'Valor',
            'volumn': 'Volume', 
            'total_value': 'Total Investido',
            'risk': 'Risco',
            'acquisitionDate': 'Data de Aquisição', 
            'dueDate' : 'Data de Expiração', 
        })

        return summary_df