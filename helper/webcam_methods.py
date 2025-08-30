import streamlit as st
from helper.webcam import webcam_input


def process_webcam(model_path,style_image,stylization_enabled: bool = False):

    st.markdown('<h3 style="text-align:center;">Webcam Style Transfer</h3>', unsafe_allow_html=True)

    webcam_input(model_path,style_image,stylization_enabled)      