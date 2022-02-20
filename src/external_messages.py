import streamlit as st
import time
import os

from src.api_communication import XpDataApi
from typing import List, Text, Dict, Any


class CreateMessages:
    def __init__(self):
        pass

    def get_modification_in_portfolio_message(
            self, user_name: Text, products_recommendation: Dict[Text, List[Text]]
    ) -> Text:
        main_text = f"""Ola {user_name},\n\nObservando o cenário econômico atual, observamos alguns ativos que possam ser de seu interesse para compor sua carteira:"""
        for prod_type, prod_list_name in products_recommendation.items():
            if prod_type != "name":
                main_text = main_text + f"{prod_type}: " + ", ".join([prod["identity"] for prod in prod_list_name])
            main_text = main_text + "\n"

        main_text = main_text + "\nPara conhecer esses e outros produtos, acesse https://conteudos.xpi.com.br/"

        return main_text

    def get_relatorio_carteira_message(
            self, user_name: Text, time_range: Text, portfolio_var: float, ibov_var: float, highlights: Dict[Text, float]
    ):
        main_text = f"""Ola {user_name},\n\nNo periodo de {time_range} sua carteira variou {portfolio_var}%, enquanto o Ibov variou {ibov_var}%.\n  Destaques:\n"""

        for prod_name, prod_var in dict(sorted(highlights.items(), key=lambda item: item[1], reverse=True)).items():
            main_text = main_text + f"  - {prod_name}: {prod_var}\n"

        return main_text

    def get_new_product_message(
            self, user_name: Text, product_data: Dict[Text, Any]
    ) -> Text:
        main_text = f"""Ola {user_name},\n\nHá um novo produto disponível para investimento. Corra para conhecer.\n"""
        for d_type, d_value in product_data.items():
            main_text = main_text + f"  - {d_type}: {d_value}\n"

        main_text = main_text + "\nPara conhecer esse e outros produtos, acesse https://conteudos.xpi.com.br/"

        return main_text


class ComunicationUserSt:
    def __init__(self, user_name: Text):
        self.user_name = user_name
        client_id = os.environ.get('HACK_XP_CLIENT_ID')
        client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
        self.api = XpDataApi(client_id=client_id, client_secret=client_secret)
        self.data = self.api.get_broker_products()
        self.user_data_inv = self.api.get_banking_user_investments(self.user_name)

    def _email_fn(self, expander, txt):
        time.sleep(2)
        expander.success(f'Enviado para {self.user_name} por e-mail')

    def _whats_fn(self, expander, txt):
        time.sleep(2)
        expander.success(f'Enviado para {self.user_name} por whatsapp')

    def create_relatorios(self):
        expander = st.expander("Enviar relatórios da carteira")
        col1_d, col2_d = expander.columns(2)
        date_s = col1_d.date_input("Data de inicio do relatório")
        date_e = col2_d.date_input("Data de fim do relatório")

        period = date_s.strftime("%d/%m/%Y") +" - "+ date_e.strftime("%d/%m/%Y")

        id_period = id(period)
        var = (id_period / 10 ** len(str(id_period)))*3

        list_product = []
        for inv_type, list_inv_product in self.user_data_inv.items():
            list_product.extend(list_inv_product)
        data_product = {}
        for product in list_product:
            if 'ticker' in product:
                data_product[product['ticker']] = product.get('profitability', 0)
            else:
                data_product[product['identity']] = product.get('profitability', 0)

        text = CreateMessages().get_relatorio_carteira_message(self.user_name, period, 0, round(var, 3), data_product)
        txt = expander.text_area('Mensagem:', text)
        col1, col2, col3 = expander.columns(3)
        col2.button('1- Enviar por e-mail', on_click=lambda: self._email_fn(expander, txt))
        col3.button('1- Enviar por whatsapp', on_click=lambda: self._whats_fn(expander, txt))

    def create_modification(self):
        expander = st.expander("Enviar recomendação de modificação da carteira")
        text = CreateMessages().get_modification_in_portfolio_message(self.user_name, self.data)
        txt = expander.text_area('Mensagem:', text)
        col1, col2, col3 = expander.columns(3)
        col2.button('2- Enviar por e-mail', on_click=lambda: self._email_fn(expander, txt))
        col3.button('2- Enviar por whatsapp', on_click=lambda: self._whats_fn(expander, txt))

    def create_new_product(self):
        import random
        expander = st.expander("Enviar recomendação de novo produto")
        product_options = []
        for k, v in self.data.items():
            if k != "name":
                product_options.extend([x for x in v])

        id_name = id(self.user_name)
        options_for_product = [x['identity'] for x in product_options]
        random.shuffle(options_for_product, lambda: id_name/10**len(str(id_name)))
        option = expander.selectbox(
            f'Escolha um produto (os primeiros são os mais recomendados para o {self.user_name})',
            options_for_product
        )
        expander.checkbox("Enviar prospecto em anexo")
        expander.checkbox("Enviar relatório em anexo")
        text = CreateMessages().get_new_product_message(self.user_name,
                                                        next((x for x in product_options if x['identity'] == option),
                                                             {}))
        txt = expander.text_area('Mensagem:', text)
        col1, col2, col3 = expander.columns(3)
        col2.button('3- Enviar por e-mail', on_click=lambda: self._email_fn(expander, txt))
        col3.button('3- Enviar por whatsapp', on_click=lambda: self._whats_fn(expander, txt))

    def show(self):
        container = st.container()
        container.subheader(f'Enviar informações para {self.user_name}')

        app_state = st.experimental_get_query_params()
        app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()}
        st.write(f"{app_state}")
        self.create_relatorios()
        self.create_modification()
        self.create_new_product()


class ComunicationForAllUsersSt:
    def __init__(self):
        self.user_name = "<Nome-Do-Usuario>"
        client_id = os.environ.get('HACK_XP_CLIENT_ID')
        client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
        self.api = XpDataApi(client_id=client_id, client_secret=client_secret)
        self.data = self.api.get_broker_products()
        self.users_to_send = self._get_users_name()
        self.user_data_inv = {"Stock": [
            {"identity": "EX 1", 'profitability': 1.2},
            {"identity": "EX 2", 'profitability': -1.3},
            {"identity": "EX 3", 'profitability': 15.2}
        ]}

    @st.cache
    def _get_users_name(self):
        return [x["name"] for x in self.api.get_openbanking_users_data()]

    def _email_fn(self, expander, txt):
        time.sleep(2)
        expander.success(f'Enviado para {self.user_name} por e-mail')

    def _whats_fn(self, expander, txt):
        time.sleep(2)
        expander.success(f'Enviado para {self.user_name} por whatsapp')

    def create_relatorios(self):
        expander = st.expander("Enviar relatórios da carteira")
        col1_d, col2_d = expander.columns(2)
        date_s = col1_d.date_input("Data de inicio dos relatórios")
        date_e = col2_d.date_input("Data de fim dos relatórios")

        period = date_s.strftime("%d/%m/%Y") +" - "+ date_e.strftime("%d/%m/%Y")

        id_period = id(period)
        var = (id_period / 10 ** len(str(id_period)))*3

        list_product = []
        for inv_type, list_inv_product in self.user_data_inv.items():
            list_product.extend(list_inv_product)
        data_product = {}
        for product in list_product:
            if 'ticker' in product:
                data_product[product['ticker']] = product.get('profitability', 0)
            else:
                data_product[product['identity']] = product.get('profitability', 0)

        text = CreateMessages().get_relatorio_carteira_message(self.user_name, period, 8, round(var, 3), data_product)
        txt = expander.text_area('Exemplo do corpo da mensagem:', text)
        col1, col2, col3 = expander.columns(3)
        col2.button('1- Enviar a todos por e-mail', on_click=lambda: self._email_fn(expander, txt))
        col3.button('1- Enviar a todos por whatsapp', on_click=lambda: self._whats_fn(expander, txt))

    def create_modification(self):
        expander = st.expander("Enviar recomendação de modificação da carteira")
        text = CreateMessages().get_modification_in_portfolio_message(self.user_name, self.data)
        txt = expander.text_area('Exemplo do corpo da mensagem:', text)
        col1, col2, col3 = expander.columns(3)
        col2.button('2- Enviar a todos por e-mail', on_click=lambda: self._email_fn(expander, txt))
        col3.button('2- Enviar a todos por whatsapp', on_click=lambda: self._whats_fn(expander, txt))

    def create_new_product(self):
        import random
        expander = st.expander("Enviar recomendação de novo produto")
        product_options = []
        for k, v in self.data.items():
            if k != "name":
                product_options.extend([x for x in v])

        id_name = id(self.user_name)
        options_for_product = [x['identity'] for x in product_options]
        random.shuffle(options_for_product, lambda: id_name/10**len(str(id_name)))
        option = expander.selectbox(
            f'Escolha um produto',
            options_for_product
        )

        options_people = expander.multiselect(
            'Para quem enviar (os clientes recomendados já estão pré-selecionados)',
            self.users_to_send,
            random.sample(self.users_to_send, 3))

        expander.checkbox("Enviar prospecto a todos em anexo")
        expander.checkbox("Enviar relatório a todos em anexo")
        text = CreateMessages().get_new_product_message(self.user_name,
                                                        next((x for x in product_options if x['identity'] == option),
                                                             {}))
        txt = expander.text_area('Exemplo do corpo da mensagem:', text)
        col1, col2, col3 = expander.columns(3)
        col2.button('3- Enviar a todos por e-mail', on_click=lambda: self._email_fn(expander, txt))
        col3.button('3- Enviar a todos por whatsapp', on_click=lambda: self._whats_fn(expander, txt))

    def show(self):
        container = st.container()
        container.subheader(f'Enviar informações para {self.user_name}')

        app_state = st.experimental_get_query_params()
        app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()}
        st.write(f"{app_state}")
        self.create_relatorios()
        self.create_modification()
        self.create_new_product()


def create_for_user(user_name: Text):
    import os
    from src.api_communication import XpDataApi

    client_id = os.environ.get('HACK_XP_CLIENT_ID')
    client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
    api = XpDataApi(client_id=client_id, client_secret=client_secret)
    data = api.get_broker_products()

    container = st.container()
    container.subheader(f'Enviar informações para {user_name}')

    app_state = st.experimental_get_query_params()
    app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()}
    st.write(f"{app_state}")

    # Relatório
    with container.container():
        expander_1 = st.expander("Enviar relatórios da carteira")
        text = CreateMessages().get_relatorio_carteira_message(user_name, "Dez-Nov", 50.1, 35.1, {"CIEL3": 10, "CASH3": -10, "PETR4": 54.3})
        txt = expander_1.text_area('Mensagem:', text)
        col1, col2, col3 = expander_1.columns(3)
        col2.button('1- Enviar por e-mail', on_click=lambda: expander_1.success(f'Enviado para {user_name} por e-mail'))
        col3.button('1- Enviar por whatsapp', on_click=lambda: expander_1.success(f'Enviado para {user_name} por whatsapp'))

    # Recomendação de modificação no portfólio
    with container.container():
        expander_2 = st.expander("Enviar recomendação de modificação da carteira")
        text = CreateMessages().get_modification_in_portfolio_message(user_name, data)
        txt = expander_2.text_area('Mensagem:', text)
        col1, col2, col3 = expander_2.columns(3)
        col2.button('2- Enviar por e-mail', on_click=lambda: expander_2.success(f'Enviado para {user_name} por e-mail'))
        col3.button('2- Enviar por whatsapp', on_click=lambda: expander_2.success(f'Enviado para {user_name} por whatsapp'))

    # Recomendação de novo produto
    with container.container():
        expander_3 = st.expander("Enviar recomendação de novo produto")
        product_options = []
        for k, v in data.items():
            if k != "name":
                product_options.extend([x for x in v])
        option = expander_3.selectbox(
            f'Escolha um produto (os primeiros são os mais recomendados para o {user_name})',
            sorted([x['identity'] for x in product_options])
        )
        text = CreateMessages().get_new_product_message(user_name, next((x for x in product_options if x['identity'] == option), {}))
        txt = expander_3.text_area('Mensagem:', text)
        col1, col2, col3 = expander_3.columns(3)
        col2.button('3- Enviar por e-mail',
                    on_click=lambda: expander_3.success(f'Enviado para {user_name} por e-mail'))
        col3.button('3- Enviar por whatsapp',
                    on_click=lambda: expander_3.success(f'Enviado para {user_name} por whatsapp'))


"""if __name__ == '__main__':
    import os
    from src.api_communication import XpDataApi

    client_id = os.environ.get('HACK_XP_CLIENT_ID')
    client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
    api = XpDataApi(client_id=client_id, client_secret=client_secret)

    data = api.get_broker_products()

    #text = CreateMessages().get_modification_in_portfolio_message("Zezinho", data)
    #text = CreateMessages().get_relatorio_carteira_message("Zezinho", "Dez-Nov", 50.1, 35.1, {"CIEL3": 10, "CASH3": -10, "PETR4": 54.3})
    text = CreateMessages().get_new_product_message("Zezinho", data["cdb"][0])
    create_for_user()
    print(text)"""