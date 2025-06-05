import os
import tempfile
import cv2
import numpy as np
import tensorflow_hub as hub
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile

from components import processing_btn
from helper import open_styled_image

def video_transfer_style(input_video : UploadedFile | None,style_image , width : int =256,height : int =256,fps : int =30):

    is_processing = True
    if style_image is None:
        st.error("Could not read style image from {style_image_path}")
        return
    if input_video is None:
        st.error("Could not read video file {input_video_path}")
        return
    pil_style_image = np.array(style_image)
    
    
    is_processing = processing_btn(is_processing)
    
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, input_video.name)

    with open(temp_path, "wb") as f:
        f.write(input_video.read())
    print(f"Video file saved to {temp_path}")
    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        st.error("Could not open video file {input_video_path}")
        return
    fourcc = cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v')
    output_video_path = os.path.join(temp_dir, "NST_video.mp4")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    model_path : str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    cap, out = process_frame(width, height, cap, pil_style_image, model_path, out)
  
  
    print(f"Styled video saved to {output_video_path}")
    display_styled_video(output_video_path)
    
def display_styled_video(output_video_path : str, is_processing : bool = False):
    if output_video_path is None:
        st.error("No video generated.")
        return
    col1, col2 = st.columns(2)
    with open(output_video_path, "rb") as f:
        with col1:
            st.video(f.read(), format="video/mp4")
    with col2:
        is_processing = False
        st.markdown("</br>", unsafe_allow_html=True)
        st.markdown(
            "<b> Your Stylized Video is Ready! Click below to download it. </b>", unsafe_allow_html=True)
        st.download_button("Download your video", f, file_name="output_video.mp4", mime="video/mp4")        
        
        
def process_frame(width : int, height : int, cap, style_image, model_path : str,out):
    hub_module = hub.load(model_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        stylized_image = get_transformed_frame(width, height, frame, style_image, hub_module)
        out.write(stylized_image)
    cap.release()
    out.release()
    return cap, out


def get_transformed_frame(width : int, height : int,frame, style_image, hub_module):
    resized_frame = cv2.resize(frame, (width, height))
    stylized_image = open_styled_image(resized_frame, style_image, hub_module)
    stylized_resized_frame = (stylized_image * 255).astype(np.uint8)
    return stylized_resized_frame[0]