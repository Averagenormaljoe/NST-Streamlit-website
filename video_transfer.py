from io import BufferedReader
import os
import tempfile
import cv2
from matplotlib.pylab import f
import numpy as np
from johnson_helper import style_transfer,get_model_from_path
import streamlit as st
import subprocess
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tensorflow as tf
from components import processing_btn
from helper import  open_styled_image
from video_helper import tensor_toimage, image_read
from cv2.typing import MatLike

def video_validation(input_video: UploadedFile | None,style_image,model_path) -> bool:
    if style_image is None and not model_path.endswith(".t7"):
        st.error(f"Could not read style image from {style_image}")
        return False
    if input_video is None:
        st.error(f"Could not read video file {input_video}")
        return False

    return True

def generate_temp_paths(video_name : str = "input_video.mp4") -> tuple[str, str]:
    temp_dir : str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, video_name)
    return temp_dir, temp_path

from typing import Optional
import time

def video_setup(name : str, width: int, height: int, fps: int = 30) -> tuple[Optional[cv2.VideoCapture], Optional[cv2.VideoWriter], Optional[str]]:
    if not os.path.exists(name):
        st.error(f"Video file {name} does not exist.")
        return None, None, None
    cap = cv2.VideoCapture(name)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    video_seconds = cap.get(cv2.CAP_PROP_FRAME_COUNT) / video_fps
    print(f"Video_FPS: {video_fps}, Video_Seconds: {video_seconds:.2f}")
    if not cap.isOpened():
        st.error(f"Could not open video file {name} for cap.")
        return None, None, None
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_dir = tempfile.mkdtemp()
    
    output_video_path = os.path.join(temp_dir, name)
    out = cv2.VideoWriter(output_video_path, fourcc, video_fps, (width, height))
    
    return cap, out, output_video_path

def get_temp_video(input_video):
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(input_video.read())
    return tfile.name

def prepare_directory(input_video,name):


    name = get_temp_video(input_video)
    if not os.path.exists(name):
        st.error(f"Could not save video file to {name}.")
        return False, name
    print(f"Video file saved to {name}")
    return True,name

def valid_video_setup(cap,out, output_video_path):
    if cap is None or out is None or output_video_path is None:
        st.error("Could not open video file.")
        return False
    return True

def finish_video(cap: cv2.VideoCapture, out: cv2.VideoWriter):
    cap.release()
    out.release()
   
def end_video(output_video_path: str, is_processing: bool = False):
    print(f"Styled video saved to {output_video_path}")
    is_processing = display_styled_video(output_video_path,is_processing)
    return is_processing
    

def video_transfer_style(input_video : UploadedFile | None,style_image , width : int =256,height : int =256,fps : int =30, model_path : str = ""):
    is_processing : bool = True
    if not video_validation(input_video, style_image,model_path):
        return
    print("Model path: ", model_path)
    if model_path.endswith(".t7"):
        pil_style_image = None
    else:
        pil_style_image = image_read(style_image)

    is_processing = processing_btn(is_processing)
    print("input_video: ", input_video)
    name = input_video.name if input_video else ""
    print(f"Input video name: {name}")
    state,name = prepare_directory(input_video,name)
    if not state:
        return
    cap, out, output_video_path = video_setup(name,width,height,fps)
    if not valid_video_setup(cap, out, output_video_path):
        return
    cap, out, frames = process_frame(width, height, cap, pil_style_image, model_path, out)
    print("cap: ", cap, "out: ", out)
    finish_video(cap, out)

   
    if frames:
        st.video(frames, format="video/mp4")
    
    #is_processing = end_video(output_video_path, is_processing)
   
  
def save_ffmpg(output_video_path : str):
    converted_video = "./testh264.mp4"
    command = f"ffmpeg -y -i {output_video_path} -c:v libx264 {converted_video}"
    subprocess.call(args=command.split(" "))

 
    
def display_styled_video(output_video_path : str, is_processing : bool = False):
    if output_video_path is None:
        st.error("No video generated.")
        return
    col1, col2 = st.columns(2)
    with col1:
        video_format = "video/mp4"
        with open(output_video_path, "rb") as f:
            st.video(f, format= video_format)
    with col2:
        is_processing = False
        video_ready_st(output_video_path)
    return is_processing     

def video_ready_st(f : str):
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("<b> Your Stylized Video is Ready! Click below to download it. </b>", unsafe_allow_html=True)
    st.download_button("Download your video", f, file_name="output_video.mp4", mime="video/mp4")   
        
        
def process_frame(width : int, height : int, cap : cv2.VideoCapture, style_image, model_path : str,out : cv2.VideoWriter):
    hub_model = get_model_from_path(model_path)
    print("Hub model: ", hub_model)
    start_time : float = time.time()
    frames : list = []
    print("Video Duration: ", cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS))
    try:
        while True:
            frame_start_time : float = time.time()
            ret, frame = cap.read()
            print(f"ret: {ret}")
            if not ret:
                print("Video has finished due to 'ret'. Exiting ...")
                break
            resized_frame : MatLike = cv2.resize(frame, (width, height))
            stylized_image = get_stylized_image(resized_frame, style_image, hub_model,model_path)
            frames.append(stylized_image)
            if stylized_image is None:
                print("Stylized frame is empty. Skipping frame...")
                continue
            out.write(stylized_image)
            frame_end_time : float = time.time()
            print(f"Processed frame in {frame_end_time - frame_start_time:.2f} seconds")
    except cv2.error as e:
        print(f"OpenCV error: {e}")
    except Exception as e:
        print(f"Error during video stylization: {e}")
    finally:
        finish_video(cap, out)
        end_time : float = time.time()
        print(f"Video style transfer processing time: {end_time - start_time:.2f} seconds")
    return cap, out,frames


def get_stylized_image(frame, style_image, hub_model,model_path):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = image_read(frame)
    if model_path.endswith(".t7"):
        stylized_frame = style_transfer(frame,hub_model)
    else:
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