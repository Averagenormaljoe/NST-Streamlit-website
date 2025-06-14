import streamlit as st
from PIL import Image
from typing import Optional
from UI_components import camera_component, method_slider, render_ui_sliders
from gatys import process_gatys, render_gatys_ui_sliders
from helper import display_instructions, generate_image_btn
from webcam_methods import process_webcam
from data import style_models_name
from streamlit.runtime.uploaded_file_manager import UploadedFile
from upload_types import content_types, video_types


if "webcam_stylization_enabled" not in st.session_state:
    st.session_state.webcam_stylization_enabled = False

def default_interface(method: str = "Image", content_image: Optional[UploadedFile] | None = None, style_image: Optional[UploadedFile] = None, picture: Optional[UploadedFile] = None):
    if st.button("Clear"):
        st.success("Cleared the images successfully!")
    print("Chosen method:",method)
    match method:
        case 'Image':
            st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
            print("Content Image: ", content_image)
            print("Style Image: ", style_image)
            generate_image_btn(content_image, style_image)
        case 'Video':
            pass
        case 'Camera':
            if picture is not None:
                generate_image_btn(picture, style_image)
        case 'Webcam':
            if st.button(f"Toggle Webcam Stylization (currently {'On' if st.session_state.webcam_stylization_enabled else 'Off'})"):
                st.session_state.webcam_stylization_enabled = not st.session_state.webcam_stylization_enabled
                if st.session_state.webcam_stylization_enabled:
                    st.success("Webcam stylization enabled.")
                else:
                    st.success("Webcam stylization disabled.")
            
        case _:
            st.error("Please select a valid method from the sidebar.")
def default_tab():
        # Upload Images

    content_image = None
    style_image = None
    picture = None
    method : str = method_slider(key="main_method")
    col1, col2 = st.columns(2)
    with col1:
       match method:
        case 'Image':
                content_image : UploadedFile | None = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=content_types, key="content_image_uploader")
        case 'Webcam':
            pass
        case 'Camera':
            picture = camera_component()
            
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=content_types)
    
    with col1:
        if method == "Webcam":
              process_webcam(style_image,st.session_state.webcam_stylization_enabled)
    
    st.sidebar.header('Options')
    
    default_interface(method=method, content_image=content_image, style_image=style_image, picture=picture)
    display_instructions()
