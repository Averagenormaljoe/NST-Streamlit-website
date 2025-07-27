from io import BufferedReader
import io
import os
import re
import tempfile
import cv2
from matplotlib.pylab import f
import numpy as np
from johnson_helper import style_transfer,get_model_from_path
import streamlit as st
import subprocess
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tensorflow as tf
from image_transfer import frame_to_image, get_result_image, resize_image
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
    temp_video  = 'temp_file_2.mp4'
    output_video_path = os.path.join(temp_dir, temp_video)
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
    cap, out, converted_video = process_frame(width, height, cap, pil_style_image, model_path, out)
    print("cap: ", cap, "out: ", out)
    finish_video(cap, out)

   
    if converted_video  and os.path.exists(converted_video):
        st.video(converted_video , format="video/mp4")
    else:
        st.error("Video file not found after processing.")
    
    is_processing = end_video(converted_video , is_processing)
   
  
def save_ffmpg(output_video_path : str):
    temp_dir = tempfile.mkdtemp()
    converted_video = "temp_video.mp4"
    path = os.path.join(temp_dir, converted_video)
    command = f"ffmpeg -y -i {output_video_path} -c:v libx264 {path}"
    subprocess.call(args=command.split(" "))
    return path

 
    
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
        
import av
def process_frame(width : int, height : int, cap : cv2.VideoCapture, style_image, model_path : str,out : cv2.VideoWriter):
    hub_model = get_model_from_path(model_path)
    print("Hub model: ", hub_model)
    start_time : float = time.time()
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Video Duration: ", cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
    output_memory_file = io.BytesIO()
    output = av.open(output_memory_file, 'w', format="mp4") 
    stream = output.add_stream('h264',fps)
    stream.width = width  
    stream.height = height  
    stream.pix_fmt = 'yuv420p' 
    stream.options
    try:
        while True:
            frame_start_time : float = time.time()
            ret, frame = cap.read()
            print(f"ret: {ret}")
            if not ret:
                print("Video has finished due to 'ret'. Exiting ...")
                break
   
            stylized_image = get_stylized_image(frame, style_image, hub_model,model_path,width)
            if stylized_image is None:
                print("Stylized frame is empty. Skipping frame...")
                continue
            out.write(stylized_image)
            stream_frame = av.VideoFrame.from_ndarray(stylized_image, format='bgr24')  
            packet = stream.encode(stream_frame )
            output.mux(packet)
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
    packet = stream.encode(None)
    output.mux(packet)
    output.close()

    output_memory_file.seek(0)
    return cap, out, output_memory_file


def get_stylized_image(frame, style_image, hub_model,model_path,width):
    orig_h, orig_w = frame.shape[0:2]
    input_frame = resize_image(frame, width, orig_h, orig_w)
    if model_path.endswith(".t7"):
        stylized_frame = style_transfer(input_frame,hub_model)
    else:
        stylized_frame = hub_model(tf.constant(input_frame), tf.constant(style_image))[0]
    stylized_image = get_result_image(stylized_frame, orig_w, orig_h)
    return stylized_image


def get_transformed_frame(width : int, height : int,frame, style_image, hub_module):
    resized_frame = cv2.resize(frame, (width, height))
    stylized_image = open_styled_image(resized_frame, style_image, hub_module)
    if stylized_image is None:
        st.error("Frame was not processed. Please try again.")
        return None
    stylized_resized_frame = (stylized_image * 255).astype(np.uint8)
    return stylized_resized_frame[0]