
import streamlit as st
from PIL import Image
from UI_components import example_images, render_ui_sliders, method_slider, camera_component,header
from johnson import johnson_header,johnson_image_input, johnson_webcam_input
from page_config import initial_page_config
from tabs import default_tab, gatys_tab, huang_tab, johnson_tab, video_tab
from tabs_display import tabs_display
from video_transfer import video_transfer_style
from gatys import render_gatys_ui_sliders
from helper import display_instructions, generate_image_btn
from webcam_methods import process_webcam
from data import style_models_name
initial_page_config()
tabs_display()