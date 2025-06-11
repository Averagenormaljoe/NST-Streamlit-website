import streamlit as st
from PIL import Image
from typing import Optional
from UI_components import camera_component, method_slider, render_ui_sliders
from gatys import process_gatys, render_gatys_ui_sliders
from helper import display_instructions, generate_image_btn
from johnson import johnson_header, johnson_image_input, johnson_webcam_input
from video_transfer import video_transfer_style
from webcam_methods import process_webcam
from data import style_models_name
from streamlit.runtime.uploaded_file_manager import UploadedFile
content_types : list[str] = ["png", "jpg", "jpeg"]
video_types : list[str] = ["mp4", "gif"]

def default_interface(method: str = "Image", content_image: Optional[UploadedFile] | None = None, style_image: Optional[UploadedFile] = None, picture: Optional[UploadedFile] = None, webcam_stylization_enabled: bool = False):
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
            if st.button("Toggle Webcam Stylization" + " (currently " + ("On" if webcam_stylization_enabled else "Off") + ")"):
                webcam_stylization_enabled = not webcam_stylization_enabled
                if webcam_stylization_enabled:
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
    webcam_stylization_enabled : bool = False
    method : str = method_slider(key="main_method")
    col1, col2 = st.columns(2)
    with col1:
       match method:
        case 'Image':
                content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=content_types, key="content_image_uploader")
        case 'Webcam':
            process_webcam(style_image)
        case 'Camera':
            picture = camera_component()
            
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=content_types)

    
    st.sidebar.header('Options')
    
    default_interface(method=method, content_image=content_image, style_image=style_image, picture=picture, webcam_stylization_enabled=webcam_stylization_enabled)
    display_instructions()

def video_tab():
    st.markdown('<h3 style="text-align:center;">Video Style Transfer</h3>', unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=video_types, key="video_uploader"
    )

    style_images = st.file_uploader(
        "Upload Style Images (PNG & JPG, select multiple)", type=content_types, accept_multiple_files=True, key="style_images_uploader"
    )
    # resolution slider
    width_resolution, height_resolution,fps,content_weight, style_weight = render_ui_sliders()
    # style intensity slider
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;font-size: 20px;font-weight: 550;">Select Style Intensity</p>', unsafe_allow_html=True)
    style_intensity = st.slider(
        "Style Intensity",
        min_value=0.1, max_value=1.0, value=0.5, step=0.1,
        help="Adjust the intensity of the style transfer effect."
    )

    if video_file is not None and style_images and len(style_images) > 0:
        st.info(f"{len(style_images)} style image(s) selected.")
        if st.button("Generate Styled Video"):
            with st.spinner("Stylizing video... This may take a few minutes."):
                is_processing = True
                # Read style images as numpy arrays
                style_imgs = [Image.open(img) for img in style_images]
                # Stylize video (implement this function in your API)
                video_transfer_style(
                    video_file,  style_imgs[0], width_resolution,height_resolution,fps=fps
                )
    display_instructions()

def johnson_interface():
    select_model_name : str | None = st.sidebar.selectbox("Choose the style model: ", style_models_name, key="johnson_model_selector")
    method = method_slider(key="johnson_method")
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