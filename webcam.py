from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import tensorflow_hub as hub
import av
from helper import open_styled_image
from turn import get_ice_servers
from streamlit_session_memo import st_session_memo
def get_model_from_path(style_model_path):
    model = cv2.dnn.readNetFromTorch(style_model_path)
    return model

def webcam_input(style_model_name,style_image, type: str = "main"):
    st.header("Webcam Live Feed")
    WIDTH = st.sidebar.select_slider('QUALITY (May reduce the speed)', list(range(150, 501, 50)))
    width = WIDTH

    @st_session_memo
    def load_model(model_name, width):  # `width` is not used when loading the model, but is necessary as a cache key.
        if type == "main":
            hub_module = hub.load(model_name)
            return hub_module

    model_path: str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    model = load_model(model_path, width)
    
    open_style_image = Image.open(style_image) if style_image is not None else None
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        if style_image is None:
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
