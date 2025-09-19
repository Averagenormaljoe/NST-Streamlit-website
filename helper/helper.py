import traceback
from helper.display_image_details import display_image_details
import streamlit as st
import numpy as np
from io import BytesIO
from PIL import Image
from helper.components import processing_btn
from helper.style_transfer import transfer_style
from helper.load_model import get_model_from_path
def generate_styled_image(content_image, style_image, model_path : str):
    try:
        print("model_path: ", model_path)

        style_model = get_model_from_path(model_path)
        generated_image = open_styled_image(content_image, style_image, style_model)
        return generated_image
    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'generate_styled_image': {e}"
        print(mes)  
        st.error(mes)
    
def open_styled_image(content_image, style_image, model,resize_style : bool= True) -> None:
    try:
        if content_image is None or style_image is None:
            st.error("Please upload both content and style images.")
            return None
        if model is None:
            st.error("Please select a valid model")
            return None
        # Convert PIL Image to numpy array
        pli_content_image = np.array(content_image)
        pli_style_image = np.array(style_image)
        # Load the pre-trained model

        # Transfer style
        styled_image = transfer_style(pli_content_image, pli_style_image, model,resize_style)
    except Exception as e:
        print(f"Error for 'process_webcam': {e}")  
        traceback.print_exc()
        return None
   
    return styled_image               

def display_styled_image(generated_image, is_processing: bool = False, show_balloons : bool = False) -> None:
    try:
        if generated_image is not None and show_balloons:
        # some balloons
            st.balloons()
        if generated_image is None:
            st.error("No image generated.")
            return

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
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'display_styled_image': {e}")  
 
        

def download_generated_image(generated_image) -> None:
    try:
        if generated_image is None:
            st.error("No image generated.")
            return
        # convert to pillow image
        img = Image.fromarray(generated_image)
        buffered : BytesIO = BytesIO()
        img.save(buffered, format="JPEG")
        display_image_details(img)
        st.download_button(
            label="Download image",
            data=buffered.getvalue(),
            file_name="output.png",
            mime="image/png"
            )
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'download_generated_image': {e}")  


    

def generate_image_btn(model_path,content_image,style_image) -> None:
    try:
        if content_image is not None and style_image is not None and model_path is not None:
            if st.button("Generate Styled Image", key="main_image_button"):
                with st.spinner("Styling Images...will take about 20-30 secs"):
                    is_processing : bool = True
                    # Convert the uploaded image to a PIL Image
                    open_content_image = Image.open(content_image)
                    open_style_image = Image.open(style_image)
            
                    # Path of the pre-trained TF model
                    generated_image = generate_styled_image(open_content_image, open_style_image, model_path)
                    is_processing = processing_btn(is_processing,"main")
                    display_styled_image(generated_image, is_processing)
                    return generated_image
    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'generate_image_btn': {e}"
        print(mes)  
        st.error(mes)        
def display_instructions() -> None:
    st.markdown("</br>", unsafe_allow_html=True)

    st.markdown(
        """
        <section style="background-color: black; padding: 10px; border-radius: 5px;">
            <h3>Instructions</h3>
            
      
           Welcome to StyleMotion!  
            Steps for using the application:  
           1. Select a mode from the dropdown: Image, Webcam, Camera, or Video.
           2. Upload a content image (or video) and a style image. Multi style images are supported.  
           3. Click on "Generate Styled Image" to apply the style transfer.  
           4. Wait for the processing to complete.
           5. The styled image will be displayed below, and you can download it.  
           6. You can also use the webcam feature for real-time style transfer.  
           7. For video style transfer, upload a video file and a style image.
           8  For camera input, allow camera access and click "Start Webcam", press take picture, which uses the camera as the content image.
           9. Use the sidebar to collect sample images and videos.  
        </section>
        """,
        unsafe_allow_html=True
    )

def instruction_warning() -> None:
    st.warning('NOTE : You need at least Intel i3 with 8GB memory for proper functioning of this application. ' \
                + ' Images greater then (2000x2000) are resized to (1000x1000).')
                 
        