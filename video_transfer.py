from encodings.punycode import T
from io import BufferedReader
import os
import tempfile
import cv2
import numpy as np
import tensorflow_hub as hub
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tensorflow as tf
from components import processing_btn
from helper import open_styled_image
from video_helper import tensor_toimage, image_read
from cv2.typing import MatLike

def video_validation(input_video: UploadedFile | None,style_image) -> bool:
    if style_image is None:
        st.error("Could not read style image from {style_image_path}")
        return False
    if input_video is None:
        st.error("Could not read video file {input_video_path}")
        return False

    return True

def generate_temp_paths(video_name : str = "input_video.mp4") -> tuple[str, str]:
    temp_dir : str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, video_name)
    return temp_dir, temp_path

from typing import Optional
import time

def video_setup(temp_path: str, temp_dir: str, width: int, height: int, fps: int = 30) -> tuple[Optional[cv2.VideoCapture], Optional[cv2.VideoWriter], Optional[str]]:
    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        st.error("Could not open video file {input_video_path}")
        return None, None, None
    fourcc = cv2.VideoWriter_fourcc(*'m', 'p', '4', 'v')
    output_video_path = os.path.join(temp_dir, "NST_video.mp4")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    return cap, out, output_video_path

def read_temp_video(input_video, temp_path : str):
    with open(temp_path, "wb") as f:
        if input_video is None:
            st.error("No video file uploaded.")
            return
        f.write(input_video.read())
 

def video_transfer_style(input_video : UploadedFile | None,style_image , width : int =256,height : int =256,fps : int =30):

    is_processing : bool = True
    if not video_validation(input_video, style_image):
        return
    pil_style_image = image_read(style_image)
    
    
    is_processing = processing_btn(is_processing)
    
    temp_dir, temp_path = generate_temp_paths()

    read_temp_video(input_video, temp_path)
    if not os.path.exists(temp_path):
        st.error(f"Could not save video file to {temp_path}.")
        return
    print(f"Video file saved to {temp_path}")

    
    model_path : str = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    cap, out, output_video_path = video_setup(temp_path,temp_dir,width,height,fps)
    if cap is None or out is None or output_video_path is None:
        st.error(f"Could not open video file {temp_path}.")
        return
    cap, out = process_frame(width, height, cap, pil_style_image, model_path, out)
  
  
    print(f"Styled video saved to {output_video_path}")
    is_processing = display_styled_video(output_video_path,is_processing)
    
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
        video_ready_st(f)
    return is_processing     

def video_ready_st(f : BufferedReader):
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("<b> Your Stylized Video is Ready! Click below to download it. </b>", unsafe_allow_html=True)
    st.download_button("Download your video", f, file_name="output_video.mp4", mime="video/mp4")   
        
        
def process_frame(width : int, height : int, cap : cv2.VideoCapture, style_image, model_path : str,out : cv2.VideoWriter):
    hub_model = hub.load(model_path)
    start_time : float = time.time()
    while True:
        frame_start_time : float = time.time()
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame : MatLike = cv2.resize(frame, (width, height))
        stylized_image = get_stylized_image(resized_frame, style_image, hub_model)
        out.write(stylized_image)
        frame_end_time : float = time.time()
        print(f"Processed frame in {frame_end_time - frame_start_time:.2f} seconds")
    cap.release()
    out.release()
    end_time : float = time.time()
    print(f"Video style transfer processing time: {end_time - start_time:.2f} seconds")
    return cap, out


def get_stylized_image(frame, style_image, hub_model):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = image_read(frame)
    stylized_frame = hub_model(tf.constant(frame), tf.constant(style_image))[0]
    stylized_image = tensor_toimage(stylized_frame)
    return stylized_image


def get_transformed_frame(width : int, height : int,frame, style_image, hub_module):
    resized_frame = cv2.resize(frame, (width, height))
    stylized_image = open_styled_image(resized_frame, style_image, hub_module)
    if stylized_image is None:
        st.error("Frame was not processed. Please try again.")
        return None
    stylized_resized_frame = (stylized_image * 255).astype(np.uint8)
    return stylized_resized_frame[0]