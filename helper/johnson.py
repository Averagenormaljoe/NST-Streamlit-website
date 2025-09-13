import traceback
import numpy as np
import streamlit as st
from PIL import Image
from helper.helper import display_styled_image
from helper.johnson_helper import style_transfer
from helper.load_model import get_model_from_path
from helper.webcam import webcam_input
def johnson_header() -> None:
    st.title('Fast neural style transfer (Johnson)')




def johnson_image_input(content_image, style_model_path: str | None) -> None:

    if content_image is None:
        st.error("Please upload the content image.")
        return 
    if style_model_path is None:
        st.error("Please select a style model.")
        return 
    if st.button("Generate Style Image"):
        with st.spinner("Stylizing Image... This may take a few minutes."):
            open_content_image = Image.open(content_image)
            pli_content_image = np.array(open_content_image)
            if pli_content_image is None:
                st.error("Failed to load content image.")
                return
                
            size : tuple[int,int] = open_content_image.size
            
            model = get_model_from_path(style_model_path,size)
            if model is None:
                st.error("Failed to load the style model.")
                return

            # Transfer style
            generated_image = style_transfer(pli_content_image, model)
            display_styled_image(generated_image)

def johnson_webcam_input(style_model_path: str | None ) -> None:
    try:
        if style_model_path is None:
            st.error("Please select a style model.")
            return
        webcam_input(style_model_path, None, webcam_stylization=True, type="johnson")
    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'johnson_webcam_input': {e}"
        print(mes)  
        st.error(mes)
