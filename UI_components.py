import streamlit as st
from streamlit_image_comparison import image_comparison
from PIL import Image
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
def method_slider(key="method_selector") -> str:
    method = st.sidebar.radio('Go To ->', options=['Image','Webcam', 'Camera'], key=key)
    if method is None:
        return ""
    return method
def camera_component():
    enable = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable)
    return picture

def display_image(image_path: str):

    img = Image.open(image_path)
    resized_img = img.resize((190, 250))
    st.image(resized_img)

def example_images():
    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content1.jpg")
    with col2:
        display_image(image_path="./assets/art1.png")

    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content2.jpg")
    with col2:
        display_image(image_path="./assets/art2.png")

    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content3.jpg")
    with col2:
        display_image(image_path="./assets/art3.png")
    
    col1,col2 = st.columns(2)
    with col1:
        st.video("./assets/man_at_sea_sliced.mp4")
def header():
    st.markdown(
        '<h1 style="text-align:center;">Style Transfer App</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;font-size: 20px;font-weight: 550;">Choose a method from the sidebar to get started!</p>', unsafe_allow_html=True)
    
    title = '<p style="text-align: center;font-size: 50px;font-weight: 350;font-family:Cursive "> Style Motion </p>'
    st.markdown(title, unsafe_allow_html=True)



    # Example Image
    st.image(image="./assets/nst.png")
    st.markdown("</br>", unsafe_allow_html=True)
    