from gatys_functions import get_model
from gatys_functions.get_layers import get_layers
import streamlit as st
from gatys_functions.LoopManager import LoopManager
from shared_utils.file_nav import get_base_name
def render_gatys_ui_sliders() -> tuple[int, float]:
    # Style intensity slider
    style_intensity : float = st.slider(
        "Select Style Intensity", 
        min_value=0.1, max_value=1.0, value=0.5, step=0.1, 
        help="Adjust the intensity of the style transfer effect."
    )
    content_intensity : float = st.slider(
        "Select Content Intensity", 
        min_value=0.1, max_value=1.0, value=0.5, step=0.1, 
        help="Adjust the content intensity of the style transfer effect."
    )
    hardware_options : list[str] = ["CPU", "GPU"]
    st.markdown('<h3 style="text-align:center;">Gatys model</h3>', unsafe_allow_html=True)
    st.radio("CPU or GPU?", options=hardware_options, index=0, key="gatys_device_choice",
             help="Select the device to run the Gatys model. GPU is recommended for faster processing.")
    st.markdown('<h4 style="text-align:center;">Provides the highest style quality at the cost of speed (will take around 5 minutes or hour on cpu devices)</h4>', unsafe_allow_html=True)
    epoch_slider : int = st.slider(
          "Select Epochs",
          min_value=1, max_value=1000, value=10, step=1,
          help="Set the number of epochs for the style transfer. More epochs may yield better results but will take longer."
      )
    optimizer = st.selectbox(
        "Select Optimizer",
        options=["Adam", "SGD"],
        index=0,
        help="Choose the optimizer for the style transfer process."
    )
    lr = st.slider(
        "Select Learning Rate",
        min_value=0.0, max_value=1.0, value=0.1, step=0.01,
        help="Set the learning rate for the optimizer."
    )
    return epoch_slider, style_intensity

def process_gatys(content_image, style_image, epoch_slider : int, content_weight = 2.5e-8,style_intensity : float = 1e-6, total_variation_weight = 1e-6,ln = "vgg19"):
    loop_manager = LoopManager()
    results = get_layers(False,ln)
    style_layer_names, content_layer_names, style_weights, content_weights = results
    config_layers = {
    "style" : style_layer_names,
    "content" : style_layer_names
   }
    w = 512
    h = 512
    feature_extractor = get_model(ln,w,h, config_layers=config_layers)
    config = {
    "optimizer": "adam",
    "ln": ln,
    "lr": 1.0,
    "size": (w,h),
    "content_layer_names": content_layer_names,
    "style_layer_names": style_layer_names,
    "feature" : feature_extractor,
    "c_weight": content_weight,
    "s_weight": style_intensity,
    "tv_weight": total_variation_weight,
    "iterations": epoch_slider,
    }
    content_name = get_base_name(content_image)
    style_name = get_base_name(style_image)
    loop_manager.training_loop(
                content_image, style_image,
                content_name, style_name, config=config
            )
    return None

def generate_gatys_image(content_image, style_image, epoch_slider : int, style_intensity : float):
    return None

def video_transfer_style(video_file, style_image, width_resolution, height_resolution, fps=30):

    return None
def webcam_transfer_style(style_image, width_resolution, height_resolution, fps=30):

    return None