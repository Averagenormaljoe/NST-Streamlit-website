
import streamlit as st
from gatys_model import gatys_functions

from shared_utils.file_nav import get_base_name
from gatys_functions.LoopManager import LoopManager
from gatys_functions.get_model import get_model
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
    optimizer : str = st.selectbox(
        "Select Optimizer",
        options=["Adam", "SGD"],
        index=0,
        help="Choose the optimizer for the style transfer process."
    )
    lr : float = st.slider(
        "Select Learning Rate",
        min_value=0.0, max_value=1.0, value=0.1, step=0.01,
        help="Set the learning rate for the optimizer."
    )
    return epoch_slider, style_intensity

def process_gatys(content_path, style_path, epoch_slider : int, content_weight = 2.5e-8,style_weight : float = 1e-6, total_variation_weight = 1e-6,ln = "vgg19"):

    w = 512
    h = 512
    style_layer_names = [
    "block1_conv1",
    "block2_conv1",
    "block3_conv1",
    "block4_conv1",
    "block5_conv1",
    ]
    # content layers
    content_layer_names = ["block5_conv2"]
    config_layers = {
    "style" : style_layer_names,
    "content" : style_layer_names
    }
    
    feature_extractor = get_model("vgg",w,h, config_layers=config_layers)
    config = {
    "optimizer": "adam",
    "ln": "vgg19",
    "lr": 1.0,
    "size": (512, 512),
    "content_layer_names": content_layer_names,
    "style_layer_names": style_layer_names,
    "feature" : feature_extractor,
    "c_weight": content_weight,
    "s_weight": style_weight,
    "tv_weight": total_variation_weight,
    "video_mode": False
    
  }
    content_name = get_base_name(content_path)
    style_name = get_base_name(style_path)
    loop_manager = LoopManager(config)
    results = loop_manager.training_loop(
            content_path, style_path,
            content_name, style_name, config=config
        )
    if results is None:
        print(f"Gatys process for ({content_name}) and ({style_name}). Next loop...")
        return None
    results = loop_manager.training_loop(
        content_path, style_path,
        content_name, style_name, config=config
    )
    generated_images, best_image,log_data = results
    return best_image.get_image()

def generate_gatys_image(content_image, style_image, epoch_slider : int, style_intensity : float):
    return None

def video_transfer_style(video_file, style_image, width_resolution, height_resolution, fps=30):

    return None
def webcam_transfer_style(style_image, width_resolution, height_resolution, fps=30):

    return None