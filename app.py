
import streamlit as st
from PIL import Image
from UI_components import example_images, render_ui_sliders, method_slider, camera_component,header
from johnson import johnson_header,johnson_image_input, johnson_webcam_input
from video_transfer import video_transfer_style
from gatys import render_gatys_ui_sliders
from helper import display_instructions, generate_image_btn
from webcam_methods import process_webcam
from data import style_models_name
st.set_page_config(page_title="Style motion - Style Transfer",
                   page_icon="./assets/favicon.png", layout="centered")

# title 

st.markdown("<hr>", unsafe_allow_html=True)
tab1, tab2, tab3,tab4,tab5 = st.tabs(["Image", "Video", "Johnson model","Gatys model", "Huang model"])

# -------------Header Section------------------------------------------------

with tab1:
    header()
with tab2:
    header()
with tab3:
    header()
with tab4:
    header()
with tab5:
    header()


# -------------Sidebar Section------------------------------------------------


with st.sidebar:

    # ---------------------Example art images------------------------------

    example_images()

 # ----------------------------------------------------------------------


# -------------Body Section------------------------------------------------
with tab1:


    # Upload Images

    content_image = None
    style_image = None
    picture = None
    webcam_stylization_enabled = False
    method = method_slider(key="main_method")
    col1, col2 = st.columns(2)
    with col1:
       match method:
        case 'Image':
                content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg', "jpeg"], key="content_image_uploader")
        case 'Webcam':
            process_webcam(style_image)
        case 'Camera':
            picture = camera_component()
            
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=['png', 'jpg', "jpeg"])

    
    st.sidebar.header('Options')
    
    if st.button("Clear"):
        st.success("Cleared the images successfully!")
    print("Chosen method:",method)
    match method:
        case 'Image':
            st.markdown('<h3 style="text-align:center;">Image Style Transfer</h3>', unsafe_allow_html=True)
            print("Content Image: ", content_image)
            print("Style Image: ", style_image)
            generate_image_btn(content_image, style_image)
        case 'Video':
            pass
        case 'Camera':
            if picture is not None:
                generate_image_btn(picture, style_image)
        case 'Webcam':
            if st.button("Toggle Webcam Stylization" + " (currently " + ("On" if webcam_stylization_enabled else "Off") + ")"):
                webcam_stylization_enabled = not webcam_stylization_enabled
                if webcam_stylization_enabled:
                    st.success("Webcam stylization enabled.")
                else:
                    st.success("Webcam stylization disabled.")
            
        case _:
            st.error("Please select a valid method from the sidebar.")
    display_instructions()




# -------------Video Style Transfer Section------------------------------------------------

with tab2:
    st.markdown('<h3 style="text-align:center;">Video Style Transfer</h3>', unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload Video (MP4 & gif only)", type=['mp4','gif'], key="video_uploader"
    )

    style_images = st.file_uploader(
        "Upload Style Images (PNG & JPG, select multiple)", type=['png', 'jpg', "jpeg"], accept_multiple_files=True, key="style_images_uploader"
    )
    # resolution slider
    width_resolution, height_resolution,fps,content_weight, style_weight = render_ui_sliders()
    # style intensity slider
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;font-size: 20px;font-weight: 550;">Select Style Intensity</p>', unsafe_allow_html=True)
    style_intensity = st.slider(
        "Style Intensity",
        min_value=0.1, max_value=1.0, value=0.5, step=0.1,
        help="Adjust the intensity of the style transfer effect."
    )

    if video_file is not None and style_images and len(style_images) > 0:
        st.info(f"{len(style_images)} style image(s) selected.")
        if st.button("Generate Styled Video"):
            with st.spinner("Stylizing video... This may take a few minutes."):
                is_processing = True
                # Read style images as numpy arrays
                style_imgs = [Image.open(img) for img in style_images]
                # Stylize video (implement this function in your API)
                video_transfer_style(
                    video_file,  style_imgs[0], width_resolution,height_resolution,fps=fps
                )
    display_instructions()
              
  # -------------Johnson Model Section------------------------------------------------             
with tab3:
    johnson_header()
    select_model_name = st.sidebar.selectbox("Choose the style model: ", style_models_name)
    method = method_slider(key="johnson_method")

    match method:
        case 'Image':
            content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg', "jpeg"])
            johnson_image_input(content_image, select_model_name)
        case 'Webcam':
            johnson_webcam_input(select_model_name)
        case'Camera':
            picture = camera_component()
            johnson_image_input(picture, select_model_name)
        case "video":
            pass
    display_instructions()
# -------------Gatys Model Section------------------------------------------------        
with tab4:
    render_gatys_ui_sliders()
    method = method_slider(key="gatys_method")
    match method:
        case 'Image':
            content_image = st.file_uploader(
                    "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg', "jpeg"])
            johnson_image_input(content_image, select_model_name)
        case'Camera':
            picture = camera_component()
            johnson_image_input(picture, select_model_name)
    display_instructions()

    
    
    
   
# -------------Huang Model Section------------------------------------------------    
    

with tab5:
      st.markdown('<h3 style="text-align:center;">Huang Style Transfer</h3>', unsafe_allow_html=True)
      display_instructions()