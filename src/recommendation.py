from api_communication import XpDataApi
from user_report import Report

import pandas as pd
import scipy.sparse as sparse
from sklearn.preprocessing import LabelEncoder
import implicit

class InvestmentRecommender: 

    def __init__(self, api, download_datset=False): 

        self.api = api
        self.column_names = ['identity','bankId','description','type','value','dueDate','profitability','risk','acquisitionDate','volumn','ticker','name']
        
        if download_datset: 
            self.dataset = self._get_all_users_data()
        else: 
            self.dataset = pd.read_csv('data/dataset.csv')

        self.le_inv = LabelEncoder()
        self.dataset['investment_id'] = self.le_inv.fit_transform(self.dataset.investment_name).astype('int')

        self.le_client = LabelEncoder()
        self.dataset['client_id'] = self.le_client.fit_transform(self.dataset.client_name).astype('int')

        self.user_item_matrix = sparse.csr_matrix((self.dataset['inv_pct'], (self.dataset['client_id'], self.dataset['investment_id'])))

        self.model = self._fit()

    def _get_all_users_data(self): 
        data = self.api.get_openbanking_users_data()

        client_names = []
        for n in range(len(data)): 
            client_names.append(data[n]['name'])

        dataset_clients_investments = pd.DataFrame(columns=self.column_names)
        for client in client_names: 
            try:
                client_report = Report(self.api, client_name=client)
                dataset_clients_investments = dataset_clients_investments.append(client_report.inv_user_df, ignore_index=True)
            except:
                pass
        
        dataset_clients_investments['investment_name'] = dataset_clients_investments.identity.apply(lambda x: '-'.join(x.split('-')[:3]))
        dataset_clients_investments['inv_pct'] = dataset_clients_investments.groupby('client_name').total_value.apply(lambda x: 100 * x / float(x.sum())).astype('float')  

        return dataset_clients_investments

    def _fit(self): 
        model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=20)

        alpha_val = 2
        data_conf = (self.user_item_matrix * alpha_val).astype('double')

        model.fit(data_conf)

        return model

    def find_similar_investments(self, investment_id, n_similar = 10): 
        similar = self.model.similar_items(investment_id, n_similar)    
        investments = self.le_inv.inverse_transform(similar[0])    
        return investments

    def get_user_recommendations(self, client_id, n_similar = 10): 
        recommended = self.model.recommend(client_id, self.user_item_matrix[client_id], N = n_similar) 
        investments = self.le_inv.inverse_transform(recommended[0]) 
        return investments

