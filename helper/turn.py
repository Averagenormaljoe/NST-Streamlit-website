import logging
import os
import traceback
from typing import Dict, List

import streamlit as st
from twilio.rest import Client

logger = logging.getLogger(__name__)


@st.cache_data 
def get_ice_servers() -> List[Dict[str, List[str]]]:
    return [{"urls": ["stun:stun.l.google.com:19302"]}]
