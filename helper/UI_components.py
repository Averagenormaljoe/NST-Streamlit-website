import traceback
import streamlit as st
from streamlit_image_comparison import image_comparison
from PIL import Image

from helper.styles import get_header_style, get_title_style
from PIL import ImageFile
def method_slider(key : str ="method_selector") -> str:
    method : str =  st.selectbox('Select your chosen mode', options=['Image','Webcam', 'Camera', 'Video'], key=key)
    if method is None:
        return ""
    return method
def camera_component(key : str = "main_model"):
    enable : bool = st.checkbox("Enable camera",key=key)
    picture = st.camera_input("Take a picture", disabled=not enable)
    if picture is None:
        st.warning("Please take a picture using the camera.")
        return None
    
    return picture

def display_image(image_path: str) -> None:
    try:
        img : ImageFile = Image.open(image_path)
        resized_img = img.resize((190, 250))
        st.image(resized_img)
    except Exception as e:
        traceback.print_exc()
        print(f"Error for 'display_image': {e}")  
   

def example_images() -> None:
    
    st.title("Example Images")
    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content/content1.jpg")
    with col2:
        display_image(image_path="./assets/style/art1.png")

    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content/content2.jpg")
    with col2:
        display_image(image_path="./assets/style/art2.png")

    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content/content3.jpg")
    with col2:
        display_image(image_path="./assets/style/art3.png")
        
        
    col1, col2 = st.columns(2)
    with col1:
        display_image(image_path="./assets/content/content5.jpg")
    with col2:
        display_image(image_path="./assets/style/art5.png")
    
    col1,col2 = st.columns(2)
    with col1:
        st.video("./assets/video/man_at_sea_sliced.mp4")
def header() -> None:
    header_style : str = get_header_style()
    title_style : str = get_title_style()
    st.markdown(
        '<h1 style="text-align:center;">Neural Style Transfer App</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p style={header_style} >Choose a image from the sidebar to get started!</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p style={header_style}>Change methods using the dropdown menu</p>', unsafe_allow_html=True)
    
    title = f'<p style="{title_style}"> Style Motion </p>'
    st.markdown(title, unsafe_allow_html=True)



    # Example Image
    st.image(image="./assets/nst.png")
    st.markdown("</br>", unsafe_allow_html=True)

def output_size() -> tuple[int,int]:
    width_slider : int = st.slider(
          "Select Epochs",
          min_value=1, max_value=1000, value=10, step=1,
          help="Set the number of epochs for the style transfer. More epochs may yield better results but will take longer."
    )
    height_slider : int = st.slider(
          "Select Epochs",
          min_value=1, max_value=1000, value=10, step=1,
          help="Set the number of epochs for the style transfer. More epochs may yield better results but will take longer."
    )
    return width_slider,height_slider
    
    
    