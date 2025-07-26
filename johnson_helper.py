from operator import contains
import imutils
import cv2
import numpy as np
import streamlit as st
from cv2.typing import MatLike
import tensorflow_hub as hub

def get_model_from_path(style_model_path):
    if style_model_path.endswith('.t7'):
        model = cv2.dnn.readNetFromTorch(style_model_path)
    elif style_model_path.endswith('.pth'):
        model = cv2.dnn.readNetFromTensorflow(style_model_path)
    elif style_model_path.contains('tfhub'):
        model = hub.load(style_model_path)
    else:
        st.error(f"This model path is invalid: {style_model_path}")
        return None
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