import imutils
import cv2
import numpy as np
import streamlit as st
from PIL import Image
from data import style_models_dict
from helper import display_styled_image
from cv2.typing import MatLike
import webcam
def johnson_header():
    st.title('Fast neural style transfer (Johnson)')

def get_model_from_path(style_model_path):
    model = cv2.dnn.readNetFromTorch(style_model_path)
    return model

def style_transfer(image, model):
    if model is None:
        st.error("Model not loaded. Please select a valid model.")
        return None
    (h, w)  = image.shape[:2]
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) #PIL Jpeg to Opencv image

    mean : tuple[float,float,float] = (103.939, 116.779, 123.680)
    blob : MatLike = cv2.dnn.blobFromImage(image, 1.0, (w, h), mean, swapRB=False, crop=False)
    model.setInput(blob)
    output = model.forward()

    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += mean[0]
    output[1] += mean[1]
    output[2] += mean[2]
    output /= 255.0
    output = output.transpose(1, 2, 0)
    output = np.clip(output, 0.0, 1.0)
    width : int = 500
    output = imutils.resize(output, width=width)
    return output

def johnson_image_input(content_image, select_model_name: str | None) :
    if content_image is None:
        st.error("Please upload the content image.")
        return None
    if st.button("Generate Style Image"):
        with st.spinner("Stylizing video... This may take a few minutes."):
            open_content_image = Image.open(content_image)
            pli_content_image = np.array(open_content_image)
            if select_model_name is None:
                st.error("Please provide a style model.")
                return None
            style_model_path = style_models_dict[select_model_name]
            model = get_model_from_path(style_model_path)

            # Transfer style
            generated_image = style_transfer(pli_content_image, model)
            display_styled_image(generated_image)

def johnson_webcam_input(select_model_name: str | None ):
    if select_model_name is None:
        st.error("Please select a style model.")
        return None
    return select_model_name

def johnson_video_input(select_model_name: str | None, style_image, width=500):
    return select_model_name, style_image, width

