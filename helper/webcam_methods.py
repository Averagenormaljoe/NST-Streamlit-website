import streamlit as st
from helper.webcam import webcam_input


def process_webcam(model_path,style_image,stylization_enabled: bool = False) -> None:

    st.markdown('<h3 style="text-align:center;">Webcam Style Transfer</h3>', unsafe_allow_html=True)
    try:
        webcam_input(model_path,style_image,stylization_enabled)    
    except Exception as e:
        print(f"Error for 'process_webcam': {e}")  