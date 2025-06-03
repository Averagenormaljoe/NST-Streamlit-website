import imutils
import cv2
import numpy as np
import streamlit as st
def johnson_header():
    st.sidebar.title('Fast neural style transfer (Johnson)')
    st.sidebar.header('Options')
    

def get_model_from_path(style_model_path):
    model = cv2.dnn.readNetFromTorch(style_model_path)
    return model

def style_transfer(image, model):
    if model is None:
        st.error("Model not loaded. Please select a valid model.")
        return None
    (h, w) = image.shape[:2]
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR) #PIL Jpeg to Opencv image

    blob = cv2.dnn.blobFromImage(image, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
    model.setInput(blob)
    output = model.forward()

    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    output /= 255.0
    output = output.transpose(1, 2, 0)
    output = np.clip(output, 0.0, 1.0)
    output = imutils.resize(output, width=500)
    return output

def johnson_image_input(content_image, select_model_name: str | None) :
    if content_image is None:
        st.error("Please upload both content and style images.")
        return None


    pli_content_image = np.array(content_image)

    model = get_model_from_path(select_model_name)

    # Transfer style
    generated_image = style_transfer(pli_content_image, model)
    
    return generated_image

def johnson_webcam_input(select_model_name: str | None ):
    return select_model_name

def johnson_video_input(select_model_name: str | None, style_image, width=500):
    return select_model_name, style_image, width

