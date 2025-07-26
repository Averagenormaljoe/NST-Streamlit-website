from UI_components import method_slider
from helper import display_instructions
from upload_types import content_types
import streamlit as st
from UI_components import camera_component
from johnson import johnson_header, johnson_image_input, johnson_webcam_input
from data import style_models_name,style_models_dict

def johnson_interface():
    select_model_name : str | None = st.selectbox("Choose the style model: ", style_models_name, key="johnson_model_selector")
    if select_model_name is None:
        st.error("Please select a style model.")
    model_path = style_models_dict[select_model_name]
    method = method_slider("johnson_method")
    match method:
        
        case 'Image':
            content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=content_types, key="johnson_content_image_uploader")
            johnson_image_input(content_image, model_path)
        case 'Webcam':
            johnson_webcam_input(model_path)
        case'Camera':
            picture = camera_component()
            johnson_image_input(picture, model_path)
        case "video":
            video

def johnson_tab():
    johnson_header()
    johnson_interface()
    display_instructions()