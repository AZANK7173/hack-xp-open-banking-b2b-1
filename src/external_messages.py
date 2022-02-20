import streamlit as st

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


def create_for_user(user_name: Text):
    import os
    from src.api_communication import XpDataApi

    client_id = os.environ.get('HACK_XP_CLIENT_ID')
    client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')
    api = XpDataApi(client_id=client_id, client_secret=client_secret)
    data = api.get_broker_products()

    container = st.container()
    container.subheader(f'Enviar informações para {user_name}')

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