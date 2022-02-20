import os
import streamlit as st

from src.external_messages import ComunicationForAllUsersSt, get_users_name
from src.st_app import AppClientData
from src.api_communication import XpDataApi


client_id = os.environ.get('HACK_XP_CLIENT_ID')
client_secret = os.environ.get('HACK_XP_CLIENT_SECRET')

api = XpDataApi(client_id=client_id, client_secret=client_secret)


ComunicationForAllUsersSt(api, get_users_name(api)).show()
