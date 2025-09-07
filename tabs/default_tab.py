from helper.model_dirs import get_model_dirs
import streamlit as st
from PIL import Image
from typing import Optional
from helper.UI_components import camera_component, method_slider
from helper.ui_video import get_ui_video_sliders, get_video_uploader
from helper.helper import display_instructions, generate_image_btn
from helper.webcam_methods import process_webcam
from streamlit.runtime.uploaded_file_manager import UploadedFile
from helper.upload_types import content_types, video_types
from helper.video_transfer import video_transfer_style

def video_process(video_file,style_images,width_resolution : int,height_resolution : int,fps : int,model_path):
    if fps is None or height_resolution is None or width_resolution is None:
        st.error("The provided height, fps or width resolution is invalid")
        return
    style_images = [style_images] if type(style_images) is UploadedFile else style_images
    if video_file is not None and style_images is not None and model_path is not None :
        print(style_images)
        open_style_imgs = [Image.open(img) for img in style_images]
        st.info(f"{len(open_style_imgs)} style image(s) selected.")
        if st.button("Generate Styled Video"):
            with st.spinner("Stylizing video... This may take a few minutes."):
                video_transfer_style(
                    video_file,  open_style_imgs[0], width_resolution,height_resolution,fps=fps,model_path=model_path
                    )

if "webcam_stylization_enabled" not in st.session_state:
    st.session_state.webcam_stylization_enabled = False

def default_interface(model_path : str,method: str = "Image", content_image: Optional[UploadedFile] | None = None, style_image: Optional[UploadedFile] = None, picture: Optional[UploadedFile] = None, video_uploader: Optional[UploadedFile] = None):

    print("Chosen method:",method)
    match method:
        case 'Image':
            st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
            print("Content Image: ", content_image)
            print("Style Image: ", style_image)
            generate_image_btn(model_path,content_image, style_image)
        case 'Video':
            width_resolution, height_resolution,fps = get_ui_video_sliders()
            video_process(video_uploader, style_image, width_resolution, height_resolution, fps,model_path)
        case 'Camera':
            if picture is not None:
                generate_image_btn(model_path,picture, style_image)
        case 'Webcam':
            print("In webcam mode")
        case _:
            st.error("Please select a valid method from the sidebar.")
def default_tab():
        # Upload Images
    dir_path = "main_model"
    model_dirs,style_models_dict = get_model_dirs(dir_path)
    select_model_name : str | None = st.selectbox("Choose the style model: ", model_dirs, key="style_motion_model_selector")
    if select_model_name is None:
        st.error("Please select a style model.")
    model_path = style_models_dict[select_model_name]
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
            camera_key = "main_model"
            picture = camera_component(camera_key)
        case 'Video':
            video_uploader = get_video_uploader(video_types=video_types, key="video_uploader")
          
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=content_types, key="default loader" )
    
    with col1:
        if method == "Webcam":
              process_webcam(model_path,style_image,True)
    
    
    
    default_interface(model_path,method=method, content_image=content_image, style_image=style_image, picture=picture,video_uploader=video_uploader)
    display_instructions()
