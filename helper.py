from turtle import mode
import requests
import streamlit as st
import numpy as np
import keras
import tensorflow_hub as hub
from io import BytesIO
from PIL import Image
import tensorflow as tf
from components import processing_btn
from API import transfer_style
import os
from keras.layers import TFSMLayer
def is_pb_model(file_name : str) -> bool:
    return file_name.lower().endswith(".pb")

def is_keras_model(file_name : str) -> bool:
    return file_name.lower().endswith(".keras")


def contains_pb_model(dir_path: str) -> bool:
    if not os.path.isdir(dir_path):
        return False
    return any(file.lower().endswith(".pb") for file in os.listdir(dir_path))


def load_model(model_path : str):
    if is_keras_model(model_path):
        model = tf.keras.models.load_model(model_path)
        return model
    elif contains_pb_model(model_path):
        print(model_path)
        loaded = tf.saved_model.load(model_path)
        print("Signature:",loaded.signatures["serving_default"].structured_input_signature)
        model = TFSMLayer(model_path, call_endpoint="serving_default")
        return model

    hub_module = hub.load(model_path)
    return hub_module

def generate_styled_image(content_image, style_image, model_path : str):
    print("model_path: ", model_path)
    

    hub_module = load_model(model_path)
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

def display_styled_image(generated_image, is_processing: bool = False, show_balloons : bool = False):
    
    if generated_image is not None and show_balloons:
        # some balloons
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
        denormalize_generated_image = (generated_image * 255).astype(np.uint8)
        download_generated_image(denormalize_generated_image)
        

def download_generated_image(generated_image):
    if generated_image is None:
        st.error("No image generated.")
        return
    # convert to pillow image
    img = Image.fromarray(generated_image)
    buffered : BytesIO = BytesIO()
    img.save(buffered, format="JPEG")

    st.download_button(
        label="Download image",
        data=buffered.getvalue(),
        file_name="output.png",
        mime="image/png"
        )


    
    
    
def get_model_path(use_main : bool = False) -> str:
    main_model_path : str = "exported_model"
    magenta_model_path : str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    # Path of the pre-trained TF model
    model_path: str =  magenta_model_path   
    return model_path
def generate_image_btn(content_image,style_image):
    if content_image is not None and style_image is not None:
        if st.button("Generate Styled Image"):
            with st.spinner("Styling Images...will take about 20-30 secs"):
                is_processing : bool = True
                # Convert the uploaded image to a PIL Image
                open_content_image = Image.open(content_image)
                open_style_image = Image.open(style_image)
           
                # Path of the pre-trained TF model
                model_path: str = get_model_path(True)
                generated_image = generate_styled_image(open_content_image, open_style_image, model_path)
                is_processing = processing_btn(is_processing)
                display_styled_image(generated_image, is_processing)
                return generated_image
            
def display_instructions():
    st.markdown("</br>", unsafe_allow_html=True)

    st.markdown(
        """
        <section style="background-color: black; padding: 10px; border-radius: 5px;">
            <h3>Instructions</h3>
            
      
           Welcome to StyleMotion!  
            Steps for using the application:  
           1. Upload a content image and a style image.  
           2. Click on "Generate Styled Image" to apply the style transfer.  
           3. The styled image will be displayed below, and you can download it.  
           4. You can also use the webcam feature for real-time style transfer.  
           5. For video style transfer, upload a video file and a style image.  
           6. Use the sidebar to navigate through these modes.  
           7. Enjoy creating art with StyleMotion!  
        </section>
        """,
        unsafe_allow_html=True
    )

def instruction_warning():
    st.warning('NOTE : You need at least Intel i3 with 8GB memory for proper functioning of this application. ' \
                + ' Images greater then (2000x2000) are resized to (1000x1000).')
                 
                
def load_image_by_url(url : str):
    try:
        image = Image.open(BytesIO(requests.get(url).content))
        return image
    except Exception as e:
        st.error(f"Error loading image from URL: {e}")
        return None
    

def get_url_image():
    url : str = st.sidebar.text_input('URL for the content image.')
    assigned_name : str = 'content.jpg'
    if st.sidebar.button('Load Image'):
        try:
            content_path : str = keras.utils.get_file(os.path.join(os.getcwd(), assigned_name), url)
            content_image_file = Image.open(content_path)
            return content_image_file
        except:
            st.error("Invalid URL. Please enter a valid image URL.")
            return None
      