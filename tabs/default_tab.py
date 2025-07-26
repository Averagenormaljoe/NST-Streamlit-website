from requests import get
import streamlit as st
from PIL import Image
from typing import Optional
from UI_components import camera_component, method_slider
from gatys import process_gatys, render_gatys_ui_sliders
from ui_video import get_ui_video_sliders
from ui_video import get_video_uploader
from helper import display_instructions, generate_image_btn
from webcam_methods import process_webcam
from data import style_models_name
from streamlit.runtime.uploaded_file_manager import UploadedFile
from upload_types import content_types, video_types
from ui_video import get_video_uploader
from video_transfer import video_transfer_style

def video_process(video_file,style_images,width_resolution : int,height_resolution : int,fps : int):
    style_images = [style_images] if isinstance(style_images, str) else style_images 
    if video_file is not None and style_images and len(style_images) > 0:
        st.info(f"{len(style_images)} style image(s) selected.")
        if st.button("Generate Styled Video"):
            with st.spinner("Stylizing video... This may take a few minutes."):
                # Read style images as numpy arrays
                style_imgs = [Image.open(img) for img in style_images]
                # Stylize video (implement this function in your API)
                video_transfer_style(
                    video_file,  style_imgs[0], width_resolution,height_resolution,fps=fps
                    )

if "webcam_stylization_enabled" not in st.session_state:
    st.session_state.webcam_stylization_enabled = False

def default_interface(method: str = "Image", content_image: Optional[UploadedFile] | None = None, style_image: Optional[UploadedFile] = None, picture: Optional[UploadedFile] = None, video_uploader: Optional[UploadedFile] = None):
 
    print("Chosen method:",method)
    match method:
        case 'Image':
            st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
            print("Content Image: ", content_image)
            print("Style Image: ", style_image)
            generate_image_btn(content_image, style_image)
        case 'Video':
            width_resolution, height_resolution,fps,content_weight, style_weight = get_ui_video_sliders()
            video_process(video_uploader, style_image, width_resolution, height_resolution, fps)
        case 'Camera':
            if picture is not None:
                generate_image_btn(picture, style_image)
        case 'Webcam':
            pass
            
        case _:
            st.error("Please select a valid method from the sidebar.")
def default_tab():
        # Upload Images

    content_image = None
    style_image = None
    picture = None
    video_uploader = None
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
        case 'Video':
            video_uploader = get_video_uploader(video_types=video_types, key="video_uploader")
          
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=content_types)
    
    with col1:
        if method == "Webcam":
              process_webcam(style_image,True)
    
    
    
    default_interface(method=method, content_image=content_image, style_image=style_image, picture=picture,video_uploader=video_uploader)
    display_instructions()
