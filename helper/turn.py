import logging
import os

import streamlit as st
from twilio.rest import Client

logger = logging.getLogger(__name__)


@st.cache_data 
def get_ice_servers():

    try:
        account_sid : str = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token : str = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    try:
        client = Client(account_sid, auth_token)

        token = client.tokens.create()
    except Exception as e:
        print(f"Error while getting credentials: {e}") 
    return token.ice_servers