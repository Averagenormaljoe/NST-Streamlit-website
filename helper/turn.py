import logging
import os
import traceback

import streamlit as st
from twilio.rest import Client

logger = logging.getLogger(__name__)


@st.cache_data 
def get_ice_servers():

    try:
        account_sid : str = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token : str = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError as e:
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."  # noqa: E501
        )
        logger.error(f"Log error: {e}")
        traceback.print_exc()
        return [{"urls": ["stun:stun.l.google.com:19302"]}]
    try: 
        client = Client(account_sid, auth_token)

        token = client.tokens.create()
    except Exception as e:
        logger.error(f"Authentication error error: {e}")
        return [{"urls": ["stun:stun.l.google.com:19302"]}]
        
    return token.ice_servers