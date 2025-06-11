import streamlit as st
from streamlit_image_comparison import image_comparison
def render_ui_sliders() -> tuple[int, int, int, float, float]: 
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
def method_slider(key="method_selector"):
    method = st.sidebar.radio('Go To ->', options=['Webcam', 'Image', 'Camera'], key=key)
    return method
def camera_component():
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    return picture
def example_images():
    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content1.jpg")
    with col2:
        st.image(image="./assets/art1.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content2.jpg")
    with col2:
        st.image(image="./assets/art2.png")

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content3.jpg")
    with col2:
        st.image(image="./assets/art3.png")
    
    col1,col2 = st.columns(2)
    with col1:
        st.video("./assets/man_at_sea_sliced.mp4")
