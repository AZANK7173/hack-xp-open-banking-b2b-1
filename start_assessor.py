import os
import streamlit as st

from src.external_messages import ComunicationForAllUsersSt, get_users_name
from src.plataform import show_assessor_all, show_news
from src.st_app import AppClientData
from src.api_communication import XpDataApi


client_id = os.environ.get('HACK_XP_CLIENT_ID')
client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')

api = XpDataApi(client_id=client_id, client_secret=client_secret)

users_list = get_users_name(api)

show_assessor_all(users_list)
show_news()
ComunicationForAllUsersSt(api, users_list).show()
