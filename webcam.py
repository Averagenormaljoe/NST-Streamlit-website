from PIL import Image
from matplotlib import style
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import tensorflow_hub as hub
import av
from helper import get_model_path, open_styled_image
from turn import get_ice_servers
from streamlit_session_memo import st_session_memo
def get_model_from_path(style_model_path):
    model = cv2.dnn.readNetFromTorch(style_model_path)
    return model

def webcam_input(style_model_name,style_image,webcam_stylization : bool = True, type: str = "main"):
    WIDTH = st.sidebar.select_slider('QUALITY (May reduce the speed)', list(range(150, 501, 50)))
    width = WIDTH

    @st_session_memo
    def load_model(model_name, width):  # `width` is not used when loading the model, but is necessary as a cache key.
        if type == "main":
            hub_module = hub.load(model_name)
            return hub_module

    model_path: str = get_model_path(True)
    model = load_model(model_path, width)
    style_image_list = [style_image] if isinstance(style_image, str) else style_image  
    open_style_image = Image.open(style_image_list[0]) if style_image_list else None
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        if style_image is None or webcam_stylization is False:
            return frame

        image = frame.to_ndarray(format="bgr24")

       
        if model is None:
            return image

        orig_h, orig_w = image.shape[0:2]

        # cv2.resize used in a forked thread may cause memory leaks
        input = np.asarray(Image.fromarray(image).resize((width, int(width * orig_h / orig_w))))

        #transferred = style_transfer(input, model)
        
        transferred = open_styled_image(input,open_style_image,model)
        result = Image.fromarray((transferred * 255).astype(np.uint8))
        image = np.asarray(result.resize((orig_w, orig_h)))
        return av.VideoFrame.from_ndarray(image, format="bgr24")

    ctx = webrtc_streamer(
        key="neural-style-transfer",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": get_ice_servers()},
        media_stream_constraints={"video": True, "audio": False},
    )
    if style_image is None:
        st.error("Please upload a style image.")
