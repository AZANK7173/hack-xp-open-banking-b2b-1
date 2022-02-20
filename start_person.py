import os
import streamlit as st

from src.external_messages import ComunicationUserSt
from src.st_app import AppClientData
from src.api_communication import XpDataApi

app_state = st.experimental_get_query_params()
app_state = {k: v[0] if isinstance(v, list) else v for k, v in app_state.items()}
user_name = app_state.get("user_name", "NAYLLA")

client_id = os.environ.get('HACK_XP_CLIENT_ID')
client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')

api = XpDataApi(client_id=client_id, client_secret=client_secret)
app = AppClientData(api, user_name)
app.create_user_page()

ComunicationUserSt(user_name, api).show()
