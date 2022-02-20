import os
import streamlit as st

from PIL import Image

from src.external_messages import ComunicationForAllUsersSt, get_users_name
from src.plataform import show_assessor_all, show_news
from src.st_app import AppClientData
from src.api_communication import XpDataApi

im = Image.open("favicon.png")
st.set_page_config(
    page_title="XP insights - Assessor",
    page_icon=im,
    layout="wide",
)

client_id = st.secrets["HACK_XP_CLIENT_ID"]
client_secret = st.secrets["HACK_XP_CLIENT_SECRET"]

api = XpDataApi(client_id=client_id, client_secret=client_secret)

users_list = get_users_name(api)

show_assessor_all(users_list)
show_news()
ComunicationForAllUsersSt(api, users_list).show()
