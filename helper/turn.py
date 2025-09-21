import logging
import os
import traceback
from typing import Dict, List

import streamlit as st
from twilio.rest import Client
# Code adapted from https://github.com/whitphx/style-transfer-web-app/blob/main/turn.py
# Website: GitHub
# Author: Yuichiro Tachibana (Tsuchiya)
# Date: Apr 27, 2023
# Date of access: 21/09/2025
logger = logging.getLogger(__name__)


@st.cache_data 
def get_ice_servers() -> List[Dict[str, List[str]]]:
    return [{"urls": ["stun:stun.l.google.com:19302"]}]
# end of code adaption