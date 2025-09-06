import logging
import os
import traceback

import streamlit as st
from twilio.rest import Client

logger = logging.getLogger(__name__)


@st.cache_data 
def get_ice_servers():

    return [{"urls": ["stun:stun.l.google.com:19302"]}]