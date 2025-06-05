import os
import tempfile
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from API import transfer_style
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from components import processing_btn
from helper import generate_styled_image

def video_transfer_style(input_video : UploadedFile | None,style_image , width : int =256,height : int =256,fps : int =30):

    is_processing = True
    if style_image is None:
        st.error("Could not read style image from {style_image_path}")
        return
    if input_video is None:
        st.error("Could not read video file {input_video_path}")
        return
    pil_style_image = np.array(style_image)
    
    col1, col2 = st.columns(2)
    is_processing = processing_btn(is_processing)
    
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, input_video.name)

    with open(temp_path, "wb") as f:
        f.write(input_video.read())

    st.video(temp_path)
    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        st.error("Could not open video file {input_video_path}")
        return
    fourcc = cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v')
    output_video_path = os.path.join(temp_dir, "NST_video.mp4")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    hub_module : str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    cap, out = process_frame(width, height, cap, pil_style_image, hub_module,out)
  
    print(f"Styled video saved to {output_video_path}")
    with open(output_video_path, "rb") as f:
        with col1:
            st.video(f.read(), format="video/mp4")
        with col2:
            is_processing = False
            st.markdown("</br>", unsafe_allow_html=True)
            st.markdown(
                        "<b> Your Stylized Video is Ready! Click below to download it. </b>", unsafe_allow_html=True)
            st.download_button("Download your video", f, file_name="output_video.mp4", mime="video/mp4")
        
        
        
def process_frame(width : int, height : int, cap, style_image, hub_module : str,out):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (width, height))
        content_image = frame.astype(np.float32)[np.newaxis, ...] / 255.
        stylized_image = generate_styled_image(content_image, style_image, hub_module)
        stylized_image = (stylized_image * 255).astype(np.uint8)
        out.write(stylized_image[0])
    cap.release()
    out.release()
    return cap, out