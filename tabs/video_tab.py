import streamlit as st
from PIL import Image
from ui_video import get_ui_video_sliders
from helper import display_instructions
from upload_types import content_types, video_types
from video_transfer import video_transfer_style
def video_tab():
    st.markdown('<h3 style="text-align:center;">Video Style Transfer</h3>', unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=video_types, key="video_uploader"
    )

    style_images = st.file_uploader(
        "Upload Style Images (PNG & JPG, select multiple)", type=content_types, accept_multiple_files=True, key="style_images_uploader"
    )
    # resolution slider
    width_resolution, height_resolution,fps,content_weight, style_weight = get_ui_video_sliders()
  

    video_process(video_file,style_images,width_resolution,height_resolution,fps)
    display_instructions()


