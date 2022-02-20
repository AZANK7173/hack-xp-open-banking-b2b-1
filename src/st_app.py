from recommendation import InvestmentRecommender
from user_report import Report
from api_communication import XpDataApi

import streamlit as st
import pandas as pd

class AppClientData: 

    def __init__(self, api, client_name, client_id):

        self.api = api
        self.client_id = client_id
        self.client_name = client_name

        self.report = Report(self.api, self.client_name)

        self.model = InvestmentRecommender(api, download_datset=False)
        self.client_recommendations = self.model.get_user_recommendations(client_id=self.client_id, n_similar = 50)

        self.renda_variavel = ['stocks', 'investfund']
        self.renda_fixa = ['cdb', 'lci', 'lca', 'cri', 'cra']

        recommended_renda_fixa = [item for item in self.client_recommendations if self.get_product_type(item) in self.renda_fixa]
        recommended_renda_variavel = [item for item in self.client_recommendations if self.get_product_type(item) in self.renda_variavel]

        self.recommended_renda_fixa = pd.DataFrame(recommended_renda_fixa, columns = ['Produtos'])
        self.recommended_renda_variavel = pd.DataFrame(recommended_renda_variavel, columns = ['Produtos'])

    def create_user_page(self): 
        
        st.title(f'Investimentos de {self.client_name}')
        sidebar = st.sidebar.title(f'Dados de {self.client_name}')
        user_data = self.api.get_openbanking_user_data(self.client_name)
    
        st.sidebar.subheader('Informações')
        st.sidebar.markdown(f"**Nome Completo**: {user_data['name']}")
        st.sidebar.markdown(f"**CPF**: {user_data['cpf']}")
        st.sidebar.markdown(f"**Data de nascimento**: {user_data['bornDate']}")
        
        st.sidebar.subheader('Instituições')
        st.sidebar.markdown(f"**Instituição**: {user_data['banks'][0]['institution']['bankName']}")
        st.sidebar.markdown(f"**Cliente desde**: {user_data['banks'][0]['startDate']}")
        st.sidebar.markdown(f"**Agência**: {user_data['banks'][0]['institution']['agency']}")
        st.sidebar.markdown(f"**Número da conta**: {user_data['banks'][0]['institution']['number']}")
        
        with st.container():
            st.subheader(f'Relatórios e desempenho da carteira de {self.client_name}')

            st.plotly_chart(self.report.plot_donut_chart_user_investments())

            st.dataframe(self.report.summary_user_invs())

        with st.container():
            st.write('\n\n\n')
            ibov, carteira = st.columns(2)
            ibov.metric('Ibovespa ', "110.879,85", "-1,2%")
            valor_investido = str(self.report.inv_user_df['total_value'].sum())
            valor_investido = f"{valor_investido[:2]}.{valor_investido[3:6]}.{valor_investido[6:]},00"
            carteira.metric('Total Investido', f"{valor_investido}", "+0,5%")
        
        st.write('\n\n\n')
        with st.container(): 
            st.subheader(f'Outros produtos que {self.client_name} pode gostar')

            rf, rv = st.columns(2)
            with rf:
                st.markdown('**Renda Fixa**')
                st.dataframe(self.recommended_renda_fixa)
            with rv: 
                st.markdown('**Renda Variável**')
                st.dataframe(self.recommended_renda_variavel)
    
    
    def get_product_type(self, product_str): 
        return (product_str.split('-')[1:2])[0].lower()



if __name__ == '__main__':
    import os
    client_id = os.environ.get('HACK_XP_CLIENT_ID')
    client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
    api = XpDataApi(client_id=client_id, client_secret=client_secret)
    app = AppClientData(api, 'NAYLLA', 148)
    app.create_user_page()
