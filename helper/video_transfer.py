#from AdaIN.AdaIN_functions.image import tensor_toimage
from helper.model_validation import is_AdaIN, is_forward_feed, variables_dir_exists
from helper.style_transfer import convert_to_numpy_image, transfer_style
from video_methods.video_stream import prepare_stream, save_packet, close_stream
from video_methods.video_interface import display_styled_video
import os
import tempfile
import cv2
import numpy as np
from helper.load_model import get_model_from_path
from helper.johnson_helper import style_transfer
import streamlit as st
import av
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile
import tensorflow as tf
from helper.image_transfer import get_result_image, resize_image
from helper.components import processing_btn
from helper.helper import  open_styled_image
from helper.video_helper import image_read
import traceback
from typing import Optional
import time
def video_validation(input_video: UploadedFile | None,style_image,model_path) -> bool:
    try:
        if style_image is None and (not model_path.endswith(".t7") and not variables_dir_exists(model_path)):
            st.error(f"Error: Could not read style image from {style_image}")
            return False
        if input_video is None:
            st.error(f"Error: Could not read video file {input_video}")
            return False

        return True
    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'video_validation': {e}"
        print(mes)  
        st.error(mes)
    return False

def generate_temp_paths(video_name : str = "input_video.mp4") -> tuple[str, str]:
    temp_dir : str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, video_name)
    return temp_dir, temp_path


def video_setup(name : str, width: int, height: int, fps: int = 30) -> Optional[cv2.VideoCapture] | None:
    try: 
        if not os.path.exists(name):
            st.error(f"Video file {name} does not exist.")
            return None, None, None
        cap = cv2.VideoCapture(name)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        video_seconds = cap.get(cv2.CAP_PROP_FRAME_COUNT) / video_fps
        print(f"Video_FPS: {video_fps}, Video_Seconds: {video_seconds:.2f}")
        if not cap.isOpened():
            st.error(f"Could not open video file {name} for cap.")
            return None
        return cap
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'process_webcam': {e}")  
    return None
def get_temp_video(input_video) -> str:
    try:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(input_video.read())
        return tfile.name
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'get_temp_video': {e}") 
        return ""

def prepare_directory(input_video,name):
    try:
        name = get_temp_video(input_video)
        if not os.path.exists(name):
            st.error(f"Could not save video file to {name}.")
            return False, name
        print(f"Video file saved to {name}")
        return True,name

    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'prepare_directory': {e}"
        print(mes)  
        st.error(mes)
    return False, name
def valid_video_setup(cap):
    if cap is None:
        st.error("Could not open video file.")
        return False
    return True

def finish_video(cap: cv2.VideoCapture):
    cap.release()

def end_video(output_video_path: str, is_processing: bool = False):
    print(f"Styled video saved to {output_video_path}")
    is_processing = display_styled_video(output_video_path,is_processing)
    return is_processing
    

def video_transfer_style(input_video : UploadedFile | None,style_image : UploadedFile | None , width : int =256,height : int =256,fps : int =30, model_path : str = ""):
    if input_video is None or model_path is None or (style_image is None and not variables_dir_exists(model_path)):
        return
    try:
        is_processing : bool = True
        if not video_validation(input_video, style_image,model_path):
            return
        print("Model path: ", model_path)
        if ((model_path.endswith(".t7") or variables_dir_exists(model_path))) and not is_AdaIN(model_path):
            pil_style_image = None
        else:
            
            pil_style_image = np.array(style_image)

        is_processing = processing_btn(is_processing,f"video_{model_path}")
        print("input_video: ", input_video)
        name = input_video.name if input_video else ""
        print(f"Input video name: {name}")
        state,name = prepare_directory(input_video,name)
        if not state:
            return
        cap = video_setup(name,width,height,fps)
        if not valid_video_setup(cap):
            return
        start_time = time.time()
        cap,converted_video = process_frame(width, height,fps, cap, pil_style_image, model_path)
        end_time = (time.time() - start_time)
        print(f"Video Mode for model ({model_path}) in {end_time} seconds.")
        print("cap: ", cap)
        if cap is None:
            st.error("Could not process video frames.")
            return
        is_processing = end_video(converted_video , is_processing)
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'video_transfer_style': {e}")  
    
 


    
def process_frame(width : int, height : int,fps, cap : cv2.VideoCapture, style_image, model_path : str):
    hub_model = get_model_from_path(model_path)
    print("Hub model: ", hub_model)
    start_time : float = time.time()
    if fps is None:
        fps = cap.get(cv2.CAP_PROP_FPS)
    print("Video Duration: ", cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps)
    output, stream, output_memory_file = prepare_stream(width, height,fps)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_text = "Stylization time. Please wait."
    video_bar = st.progress(0, text=progress_text)
    try:
        while True:
            frame_start_time : float = time.time()
            pos = (int(cap.get(cv2.CAP_PROP_POS_FRAMES)) + 1)
            progress = min(pos / total_frames, 1.0)
            video_bar.progress(progress, text=progress_text)
            ret, frame = cap.read()
            print(f"ret: {ret}")
            if not ret:
                print("Video has finished due to 'ret'. Exiting ...")
                break
   
            stylized_image = get_stylized_image(frame, style_image, hub_model,model_path,width)
            if stylized_image is None:
                print("Stylized frame is empty. Skipping frame...")
                continue
            stream_frame = av.VideoFrame.from_ndarray(stylized_image, format='bgr24')  
            save_packet(stream, output, stream_frame)
            frame_end_time : float = time.time()
            print(f"Processed frame in {frame_end_time - frame_start_time:.2f} seconds")
    except cv2.error as e:
        print(f"OpenCV error during video stylization: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"Error during video stylization: {e}")
        traceback.print_exc()
    finally:
        finish_video(cap)
        end_time : float = time.time()
        duration = end_time - start_time
        print(f"Video style transfer processing time: {duration} seconds")
        
    close_stream(stream, output, output_memory_file)
    return cap, output_memory_file

def tensor_toimage(tensor : tf.Tensor):
  tensor =tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0]==1
    tensor=tensor[0]
  return tensor

def get_stylized_image(frame, style_image, hub_model,model_path : str,width : int):
    orig_h, orig_w = frame.shape[0:2]
    input_frame = resize_image(frame, width, orig_h, orig_w)
    try:
        if is_forward_feed(model_path):
            print("Feedforward mode")
            stylized_frame = style_transfer(input_frame,hub_model)
        else:
            print("AdaIN mode")
            stylized_frame = get_transformed_frame(frame, style_image,hub_model)
    except Exception as e:
        print(f"Error:: get_stylized_image: {e}")
        traceback.print_exc()
        st.error("An error occurred during style transfer.")
        return None
    stylized_image = get_result_image(stylized_frame, orig_w, orig_h)
    return stylized_image


def get_transformed_frame(frame, style_image, hub_module):
    try:
        stylized_image = open_styled_image(frame, style_image, hub_module,False)
        if stylized_image is None:
            st.error("Frame was not processed. Please try again.")
            return None
        return stylized_image
    except Exception as e:
        traceback.print_exc()
        mes = f"Error for 'get_transformed_frame': {e}"
        print(mes)  
        st.error(mes)
    return None