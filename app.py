
from email.policy import default
from math import pi
import streamlit as st
from PIL import Image
import numpy as np
from typing import Any
import tensorflow_hub as hub
from API import transfer_style
from UI_components import render_ui_sliders, method_slider, camera_input
from johnson import johnson_header, johnson_video_input, johnson_image_input, johnson_webcam_input
from webcam import webcam_input
from components import processing_btn
from video_transfer import video_transfer_style
from gatys import render_gatys_ui_sliders
from helper import generate_image_btn, generate_styled_image, process_webcam
from data import style_models_name
st.set_page_config(page_title="Style motion - Style Transfer",
                   page_icon="./assets/favicon.png", layout="centered")

# Set the title and icon of the app

st.markdown("<hr>", unsafe_allow_html=True)
tab1, tab2, tab3,tab4,tab5 = st.tabs(["Image", "Video", "Johnson model","Gatys model", "Huang model"])

# -------------Header Section------------------------------------------------

title = '<p style="text-align: center;font-size: 50px;font-weight: 350;font-family:Cursive "> Style Motion </p>'
st.markdown(title, unsafe_allow_html=True)



# Example Image
st.image(image="./assets/nst.png")
st.markdown("</br>", unsafe_allow_html=True)


# -------------Sidebar Section------------------------------------------------


with st.sidebar:

    st.image(image="./assets/speed-brush.gif")
    st.markdown("</br>", unsafe_allow_html=True)

    st.markdown('<p style="font-size: 25px;font-weight: 550;">Some Inspiration 🎨</p>',
                unsafe_allow_html=True)
    st.markdown('Below are some of the art we created using Style Motion.',
                unsafe_allow_html=True)

    # ---------------------Example art images------------------------------

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content1.jpg")
    with col2:
        st.image(image="./assets/art1.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content2.jpg")
    with col2:
        st.image(image="./assets/art2.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content3.jpg")
    with col2:
        st.image(image="./assets/art3.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content4.jpg")
    with col2:
        st.image(image="./assets/art4.png")

 # ----------------------------------------------------------------------


# -------------Body Section------------------------------------------------
with tab1:


    # Upload Images
    col1, col2 = st.columns(3)
    content_image = None
    style_image = None
    method = method_slider()
    with col1:
        if method == 'Image':
            content_image = st.file_uploader(
                "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg'])
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=['png', 'jpg'])

    st.markdown("</br>", unsafe_allow_html=True)
    st.warning('NOTE : You need atleast Intel i3 with 8GB memory for proper functioning of this application. ' +
    ' Images greater then (2000x2000) are resized to (1000x1000).')
    st.sidebar.header('Options')
    
    if st.button("Clear"):
        st.success("Cleared the images successfully!")
        match method:
            case 'Image':
                st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
                print("Content Image: ", content_image)
                print("Style Image: ", style_image)
                generate_image_btn(content_image, style_image)
            case 'Webcam':
                process_webcam(style_image)
            case 'Camera':
                picture = camera_input()
                generate_image_btn(picture, style_image)




# -------------Video Style Transfer Section------------------------------------------------

with tab2:
    st.markdown('<h3 style="text-align:center;">Video Style Transfer</h3>', unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=['mp4','gif'], key="video_uploader"
    )

    style_images = st.file_uploader(
        "Upload Style Images (PNG & JPG, select multiple)", type=['png', 'jpg'], accept_multiple_files=True, key="style_images_uploader"
    )
    # resolution slider
    width_resolution, height_resolution, fps = render_ui_sliders()
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
        if st.button("Generate Styled Image"):
            with st.spinner("Stylizing video... This may take a few minutes."):
                is_processing = True
                # Read video bytes
                video_bytes = video_file.read()
                # Read style images as numpy arrays
                style_imgs = [np.array(Image.open(img)) for img in style_images]
                # Path of the pre-trained TF model
                model_path : str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
                hub_module = hub.load(model_path)
                # Stylize video (implement this function in your API)
                output_video_bytes = video_transfer_style(
                    video_bytes,  style_imgs[0], height_resolution, width_resolution,fps=fps
                )
                # Display result
                col1, col2 = st.columns(2)
                is_processing = processing_btn(is_processing)
                with col1:
                    st.video(output_video_bytes)
                with col2:
                    is_processing = False
                    st.markdown("</br>", unsafe_allow_html=True)
                    st.markdown(
                        "<b> Your Stylized Video is Ready ! Click below to download it. </b>", unsafe_allow_html=True)
                    st.download_button(
                        label="Download Stylized Video",
                        data=output_video_bytes,
                        file_name="stylized_output.mp4",
                        mime="video/mp4"
                    )
               
with tab3:
    johnson_header()
    select_model_name = st.sidebar.selectbox("Choose the style model: ", style_models_name)
    method = method_slider()

    if method == 'Image':
        content_image = st.file_uploader(
                "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg'])
        johnson_image_input(content_image, select_model_name)
        pass
    elif method == 'Webcam':
        johnson_webcam_input(select_model_name)
        pass
    elif method == 'Camera':
        enable = st.checkbox("Enable camera")
        picture = st.camera_input("Take a picture", disabled=not enable)
        johnson_image_input(picture, select_model_name)
        
        
with tab4:
    render_gatys_ui_sliders()
    
    
    
   
    
    


with tab5:
      st.markdown('<h3 style="text-align:center;">Huang Style Transfer</h3>', unsafe_allow_html=True)