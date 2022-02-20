from matplotlib.pyplot import title
import streamlit as st 
from src.news import get_news
from src.create_tables import st_table,st_table_cc, lista

def show_assessor_all(users_list):
    st.title('Central do Assessor')
    st.subheader('Últimas Movimentações de Investimento de seus Clientes')
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    st.dataframe(st_table)

    st.subheader('Dados Open Finance: Últimos Lancamentos Conta Corrente - Clientes')
    st.dataframe(st_table_cc)

    st.subheader('Dados Open Finance: Balanço dos Clientes (oportunidades de novas vendas)')
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"{lista[0][0]}", f"R$ {int(lista[0][1])}", "R$ 5000")
    col2.metric(f"{lista[1][0]}", f"R$ {int(lista[1][1])}", "- R$ 12780")
    col3.metric(f"{lista[2][0]}", f"R$ {int(lista[2][1])}", "- R$ 200")
    col4.metric(f"{lista[3][0]}", f"R$ {int(lista[3][1])}", "R$ 4500")

    st.subheader('Acessar dados de cliente')
    option = st.selectbox(
        f'Escolha um produto',
        users_list
    )
    _, _, _, col4_1 = st.columns(4)
    link = f'[[Acessar Cliente]](http://192.168.0.2:8501/?user_name={option})'
    col4_1.markdown(link, unsafe_allow_html=True)


def show_news():
    st.sidebar.subheader('Últimas Notícias')
    link = 'https://www.infomoney.com.br/feed/'
    titles, links = get_news(link)
    st.sidebar.info(f"""
        - [{titles[0]}]({links[0]})
        - [{titles[1]}]({links[1]})
        - [{titles[2]}]({links[2]})
    """)

if __name__ == "__main__":
    show_assessor_all()
    show_news()