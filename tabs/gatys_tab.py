from UI_components import method_slider
from gatys import process_gatys, render_gatys_ui_sliders
from helper import display_instructions
from upload_types import content_types
import streamlit as st
from UI_components import camera_component
from data import style_models_name
from streamlit.runtime.uploaded_file_manager import UploadedFile


def gatys_interface():
    style_image = None
    col1, col2 = st.columns(2)
    with col1:
        epoch_slider, style_intensity = render_gatys_ui_sliders()
        select_model_name : str | None = st.sidebar.selectbox("Choose the style model: ", style_models_name, key="gatys_model_selector")
        method = method_slider(key="gatys_method")
        match method:
            case 'Image':
                content_image = st.file_uploader(
                        "Upload Content Image (PNG & JPG images only)", type=content_types, key="gatys_content_image_uploader")
                process_gatys(content_image, style_image,epoch_slider, style_intensity)
            case'Camera':
                picture : UploadedFile | None = camera_component()
                process_gatys(picture, style_image,epoch_slider, style_intensity)
            case 'Webcam':
                pass
                
            case 'Video':
        
                pass
            case _:
                st.error("Please select a valid method from the sidebar.")
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=content_types, key="gatys_style_image_uploader")

            

def gatys_tab():
    
    gatys_interface()
    display_instructions()
def huang_tab():
    st.markdown('<h3 style="text-align:center;">Huang Model</h3>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;font-size: 20px;font-weight: 550;">This model is not implemented yet.</p>', unsafe_allow_html=True)
    display_instructions()