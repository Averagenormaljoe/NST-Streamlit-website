from PIL import Image
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import tensorflow_hub as hub
from helper.image_transfer import frame_to_image, get_result_image, resize_image
from helper.helper import open_styled_image
from helper.turn import get_ice_servers
from streamlit_session_memo import st_session_memo
from helper.johnson_helper import get_model_from_path, style_transfer


def webcam_input(style_model_name,style_image,webcam_stylization : bool = True, type: str = "main",width = 256):


    @st_session_memo
    def load_model(model_name, width):  # `width` is not used when loading the model, but is necessary as a cache key.
            model = get_model_from_path(model_name)
            return model


    model = load_model(style_model_name, width)
    style_image_list = [style_image] if not isinstance(style_image, list) else style_image  
    open_style_image = Image.open(style_image_list[0]) if style_image_list else None
    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        if (style_image is None and type != "johnson" ) or webcam_stylization is False:
            return frame

        image = frame_to_image(frame)

       
        if model is None:
            return image

        orig_h, orig_w = image.shape[0:2]

        # cv2.resize used in a forked thread may cause memory leaks
        input = resize_image(image, width, orig_h, orig_w)
        if type == "main":
            transferred = open_styled_image(input,open_style_image,model)
        elif type == "johnson":
            transferred = style_transfer(input, model)

    
        image = get_result_image(transferred, orig_w, orig_h)
        result = av.VideoFrame.from_ndarray(image, format="bgr24")
        return result

    ctx = webrtc_streamer(
        key="neural-style-transfer",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": get_ice_servers()},
        media_stream_constraints={"video": True, "audio": False},
    )
    if style_image is None and type != "johnson":
        st.error("Please upload a style image.")
