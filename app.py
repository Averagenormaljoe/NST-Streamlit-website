
import streamlit as st
from PIL import Image
import numpy as np
from typing import Any
import tensorflow_hub as hub
from UI_components import example_images, render_ui_sliders, method_slider, camera_component
from johnson import johnson_header, johnson_video_input, johnson_image_input, johnson_webcam_input
from components import processing_btn
from video_transfer import video_transfer_style
from gatys import render_gatys_ui_sliders
from helper import generate_image_btn, generate_styled_image, process_webcam
from data import style_models_name
st.set_page_config(page_title="Style motion - Style Transfer",
                   page_icon="./assets/favicon.png", layout="centered")

# title 

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

    # ---------------------Example art images------------------------------

    example_images()

 # ----------------------------------------------------------------------


# -------------Body Section------------------------------------------------
with tab1:


    # Upload Images
    col1, col2 = st.columns(2)
    content_image = None
    style_image = None
    method = method_slider(key="main_method")
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
    print("Chosen method:",method)
    match method:
        case 'Image':
            st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
            print("Content Image: ", content_image)
            print("Style Image: ", style_image)
            generate_image_btn(content_image, style_image)
        case 'Webcam':
            process_webcam(style_image)
        case 'Camera':
            picture = camera_component()
            generate_image_btn(picture, style_image)
        case 'Video':
            pass
        case _:
            st.error("Please select a valid method from the sidebar.")




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
        if st.button("Generate Styled Video"):
            with st.spinner("Stylizing video... This may take a few minutes."):
                is_processing = True
                # Read style images as numpy arrays
                style_imgs = [Image.open(img) for img in style_images]
                # Stylize video (implement this function in your API)
                video_transfer_style(
                    video_file,  style_imgs[0], width_resolution,height_resolution,fps=fps
                )
              
  # -------------Johnson Model Section------------------------------------------------             
with tab3:
    johnson_header()
    select_model_name = st.sidebar.selectbox("Choose the style model: ", style_models_name)
    method = method_slider(key="johnson_method")

    match method:
        case 'Image':
            content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg'])
            johnson_image_input(content_image, select_model_name)
        case 'Webcam':
            johnson_webcam_input(select_model_name)
        case'Camera':
            picture = camera_component()
            johnson_image_input(picture, select_model_name)
        case "video":
            pass
# -------------Gatys Model Section------------------------------------------------        
with tab4:
    render_gatys_ui_sliders()

    
    
    
   
# -------------Huang Model Section------------------------------------------------    
    

with tab5:
      st.markdown('<h3 style="text-align:center;">Huang Style Transfer</h3>', unsafe_allow_html=True)