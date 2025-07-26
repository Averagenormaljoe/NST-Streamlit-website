import streamlit as st
def get_video_uploader(video_types=["mp4", "gif","mov"], key: str = "video_uploader"):
    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=video_types, key=key
    )
    if video_file is not None:
        st.info("Video uploaded successfully.")

    return video_file

def get_ui_video_sliders() -> tuple[int, int, int, float, float]: 
    # Resolution slider
    # width
    width_resolution = st.slider(
        "Select Output Resolution (Width)", 
        min_value=256, max_value=1080, value=512, step=64, 
        help="Set the width (in pixels) for the output video. Height will be scaled proportionally."
    )
    # height
    height_resolution = st.slider(
        "Select Output Resolution (WHeight)", 
        min_value=256, max_value=1080, value=512, step=64, 
        help="Set the Height(in pixels) for the output video."
    )
    # FPS slider
    fps = st.slider(
        "Select Output FPS (Frames Per Second)", 
        min_value=1, max_value=30, value=30, step=1, 
        help="Set the frames per second for the output video."
    )
    
    content_weight = st.slider(
    "Select Content Weight",
    min_value=0.1, max_value=10.0, value=1.0, step=0.1,
    help="Adjust how much the original content is preserved in the output."
    ) 
    style_weight = st.slider(
    "Select Style Weight",
    min_value=0.1, max_value=10.0, value=1.0, step=0.1,
    help="Adjust how much the style is applied to the content."
    ) 
    
    
    return width_resolution, height_resolution, fps, content_weight, style_weight