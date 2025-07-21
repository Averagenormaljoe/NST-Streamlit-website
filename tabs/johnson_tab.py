from UI_components import method_slider
from helper import display_instructions
from upload_types import content_types
import streamlit as st
from UI_components import camera_component
from johnson import johnson_header, johnson_image_input, johnson_webcam_input
from data import style_models_name

def johnson_interface():
    select_model_name : str | None = st.selectbox("Choose the style model: ", style_models_name, key="johnson_model_selector")
    method = method_slider("johnson_method")
    match method:
        case 'Image':
            content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=content_types, key="johnson_content_image_uploader")
            johnson_image_input(content_image, select_model_name)
        case 'Webcam':
            johnson_webcam_input(select_model_name)
        case'Camera':
            picture = camera_component()
            johnson_image_input(picture, select_model_name)
        case "video":
            pass

def johnson_tab():
    johnson_header()
    johnson_interface()
    display_instructions()