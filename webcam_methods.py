import streamlit as st
from webcam import webcam_input


def process_webcam(style_image):

    st.markdown('<h3 style="text-align:center;">Webcam Style Transfer</h3>', unsafe_allow_html=True)
    model_path: str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    webcam_input(model_path,style_image)      