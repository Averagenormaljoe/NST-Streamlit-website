
from email.policy import default
import streamlit as st
from PIL import Image
import numpy as np
from typing import Any
from numpy.typing import NDArray
from io import BytesIO
import tensorflow_hub as hub
from API import transfer_style
from webcam import webcam_input
from components import processingBtn
from video_transfer import video_transfer_style
from data import style_models_name
# Set page configs. Get emoji names from WebFx
st.set_page_config(page_title="PixelMix - Style Transfer",
                   page_icon="./assets/favicon.png", layout="centered")

# Set the title and icon of the app

st.markdown("<hr>", unsafe_allow_html=True)
tab1, tab2, tab3,tab4,tab5 = st.tabs(["Image", "Video", "Johnson model","Gatys model", "Huang model"])

# -------------Header Section------------------------------------------------

title = '<p style="text-align: center;font-size: 50px;font-weight: 350;font-family:Cursive "> PixelMix </p>'
st.markdown(title, unsafe_allow_html=True)


st.markdown(
    "<b> <i> Create Digital Art using Machine Learning ! </i> </b>  &nbsp; We takes 2 images — Content Image & Style Image — and blends "
    "them together so that the resulting output image retains the core elements of the content image, but appears to "
    "be “painted” in the style of the style reference image.", unsafe_allow_html=True
)


# Example Image
st.image(image="./assets/nst.png")
st.markdown("</br>", unsafe_allow_html=True)


# -------------Sidebar Section------------------------------------------------


with st.sidebar:

    st.image(image="./assets/speed-brush.gif")
    st.markdown("</br>", unsafe_allow_html=True)

    st.markdown('<p style="font-size: 25px;font-weight: 550;">Some Inspiration 🎨</p>',
                unsafe_allow_html=True)
    st.markdown('Below are some of the art we created using PixelMix.',
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
    col1, col2, col3 = st.columns(3)
    content_image = None
    style_image = None
    method = st.sidebar.radio('Go To ->', options=['Webcam', 'Image'], key="method_selector")
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
    

    
    if (content_image is not None or method == "Webcam") and style_image is not None:
        if st.button("Clear"):
            st.success("Cleared the images successfully!")
            
        
  
        if method == 'Image':
            st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
            if st.button("Generate Styled Image"):
                with st.spinner("Styling Images...will take about 20-30 secs"):
                    is_processing : bool = True
                    
                    content_image = Image.open(content_image)
                    style_image = Image.open(style_image)

                    # Convert PIL Image to numpy array
                    content_image = np.array(content_image)
                    style_image = np.array(style_image)

                    # Path of the pre-trained TF model
                    model_path: str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
                    hub_module = hub.load(model_path)
                    # output image
                    styled_image = transfer_style(content_image, style_image, hub_module)
                    is_processing = processingBtn(is_processing)
                        
                    if style_image is not None:
                        # some baloons
                        st.balloons()

                    col1, col2 = st.columns(2)
                    with col1:
                        # Display the output
                        st.image(styled_image)
                    with col2:
                        is_processing = False
                        st.markdown("</br>", unsafe_allow_html=True)
                        st.markdown(
                            "<b> Your Image is Ready ! Click below to download it. </b>", unsafe_allow_html=True)

                        # de-normalize the image
                        styled_image = (styled_image * 255).astype(np.uint8)
                        # convert to pillow image
                        img = Image.fromarray(styled_image)
                        buffered = BytesIO()
                        img.save(buffered, format="JPEG")
                        st.download_button(
                            label="Download image",
                            data=buffered.getvalue(),
                            file_name="output.png",
                            mime="image/png")
        elif method == 'Webcam':
            st.markdown('<h3 style="text-align:center;">Webcam Style Transfer</h3>', unsafe_allow_html=True)
            model_path: str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
            webcam_input(model_path,style_image)        
                        
                    
               
                    


# -------------Video Style Transfer Section------------------------------------------------

with tab2:
    st.markdown('<h3 style="text-align:center;">Video Style Transfer</h3>', unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=['mp4','gif'], key="video_uploader"
    )

    style_images = st.file_uploader(
        "Upload Style Images (PNG & JPG, select multiple)", type=['png', 'jpg'], accept_multiple_files=True, key="style_images_uploader"
    )
    # Resolution slider
    # width
    width_resolution = st.slider(
        "Select Output Resolution (Width)", 
        min_value=256, max_value=1080, value=512, step=64, 
        help="Set the width (in pixels) for the output video. Height will be scaled proportionally."
    )
    # height
    height_resolution = st.slider(
        "Select Output Resolution (WHeight)", 
        min_value=256, max_value=1080, value=512, step=64, 
        help="Set the Height(in pixels) for the output video."
    )
    # FPS slider
    fps = st.slider(
        "Select Output FPS (Frames Per Second)", 
        min_value=1, max_value=30, value=30, step=1, 
        help="Set the frames per second for the output video."
    )
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
                is_processing = processingBtn(is_processing)
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
    st.sidebar.title('Fast neural style transfer (Johnson)')
    st.sidebar.header('Options')

    select_model_name = st.sidebar.selectbox("Choose the style model: ", style_models_name)


    #if method == 'Image':
        # image_input(select_model_name)
    #else:
        # webcam_input(select_model_name)
        
        
with tab4:
      st.markdown('<h3 style="text-align:center;">Gatys model</h3>', unsafe_allow_html=True)
      st.markdown('<h4 style="text-align:center;">Provides the highest style quality at the cost of speed (will take around 5 minutes)</h4>', unsafe_allow_html=True)
      epoch_slider = st.slider(
          "Select Epochs",
          min_value=1, max_value=1000, value=10, step=1,
          help="Set the number of epochs for the style transfer. More epochs may yield better results but will take longer."
      )
    
    


with tab5:
      st.markdown('<h3 style="text-align:center;">Huang Style Transfer</h3>', unsafe_allow_html=True)