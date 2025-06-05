import streamlit as st
import numpy as np
import tensorflow_hub as hub
from io import BytesIO
from API import transfer_style
from PIL import Image

from components import processing_btn
from webcam import webcam_input


def generate_styled_image(content_image, style_image, model_path : str):
    hub_module = hub.load(model_path)
    print("model_path: ", model_path)
    generated_image = open_styled_image(content_image, style_image, hub_module)
    return generated_image
    
    
    
    
def open_styled_image(content_image, style_image, hub_module):
  
    if content_image is None or style_image is None:
        st.error("Please upload both content and style images.")
        return None

    # Convert PIL Image to numpy array
    pli_content_image = np.array(content_image)
    pli_style_image = np.array(style_image)
    # Load the pre-trained model

    # Transfer style
    styled_image = transfer_style(pli_content_image, pli_style_image, hub_module)
    
    return styled_image              

def display_styled_image(generated_image, is_processing: bool):
    if generated_image is not None:
        # some baloons
        st.balloons()

    col1, col2 = st.columns(2)
    with col1:
        # Display the output
        st.image(generated_image)
    with col2:
        is_processing = False
        st.markdown("</br>", unsafe_allow_html=True)
        st.markdown(
            "<b> Your Image is Ready ! Click below to download it. </b>", unsafe_allow_html=True)
        # de-normalize the image
        generated_image = (generated_image * 255).astype(np.uint8)
        download_generated_image(generated_image)
        

def download_generated_image(generated_image):
    if generated_image is None:
        st.error("No image generated.")
        return
    # convert to pillow image
    img = Image.fromarray(generated_image)
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    st.download_button(
        label="Download image",
        data=buffered.getvalue(),
        file_name="output.png",
        mime="image/png")

def process_webcam(style_image):
    if style_image is None:
        st.error("Please upload a style image.")
        return
    st.markdown('<h3 style="text-align:center;">Webcam Style Transfer</h3>', unsafe_allow_html=True)
    model_path: str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    webcam_input(model_path,style_image)      
    
def generate_image_btn(content_image,style_image):
    if content_image is not None and style_image is not None:
        if st.button("Generate Styled Image"):
            with st.spinner("Styling Images...will take about 20-30 secs"):
                is_processing : bool = True
                # Convert the uploaded image to a PIL Image
                open_content_image = Image.open(content_image)
                open_style_image = Image.open(style_image)
                # Path of the pre-trained TF model
                model_path: str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
                generated_image = generate_styled_image(open_content_image, open_style_image, model_path)
                is_processing = processing_btn(is_processing)
                display_styled_image(generated_image, is_processing)
                download_generated_image(generated_image)
                return generated_image
                