
import streamlit as st
from PIL import Image
import numpy as np
from io import BytesIO
from API import transfer_style


st.markdown("<hr>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Image", "Video"])

# Set page configs. Get emoji names from WebFx
st.set_page_config(page_title="PixelMix - Style Transfer",
                   page_icon="./assets/favicon.png", layout="centered")

# -------------Header Section------------------------------------------------

title = '<p style="text-align: center;font-size: 50px;font-weight: 350;font-family:Cursive "> PixelMix </p>'
st.markdown(title, unsafe_allow_html=True)


st.markdown(
    "<b> <i> Create Digital Art using Machine Learning ! </i> </b>  &nbsp; We takes 2 images — Content Image & Style Image — and blends "
    "them together so that the resulting output image retains the core elements of the content image, but appears to "
    "be “painted” in the style of the style reference image.", unsafe_allow_html=True
)


# Example Image
st.image(image="./assets/nst.png")
st.markdown("</br>", unsafe_allow_html=True)


# -------------Sidebar Section------------------------------------------------


with st.sidebar:

    st.image(image="./assets/speed-brush.gif")
    st.markdown("</br>", unsafe_allow_html=True)

    st.markdown('<p style="font-size: 25px;font-weight: 550;">Some Inspiration 🎨</p>',
                unsafe_allow_html=True)
    st.markdown('Below are some of the art we created using PixelMix.',
                unsafe_allow_html=True)

    # ---------------------Example art images------------------------------

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

    col1, col2 = st.columns(2)
    with col1:
        st.image(image="./assets/content4.jpg")
    with col2:
        st.image(image="./assets/art4.png")

 # ----------------------------------------------------------------------


# -------------Body Section------------------------------------------------
with tab1:


    # Upload Images
    col1, col2 = st.columns(2)
    content_image = None
    style_image = None
    with col1:
        content_image = st.file_uploader(
            "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg'])
    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=['png', 'jpg'])


    st.markdown("</br>", unsafe_allow_html=True)
    st.warning('NOTE : You need atleast Intel i3 with 8GB memory for proper functioning of this application. ' +
    ' Images greater then (2000x2000) are resized to (1000x1000).')


    if content_image is not None and style_image is not None:

        with st.spinner("Styling Images...will take about 20-30 secs"):

            content_image = Image.open(content_image)
            style_image = Image.open(style_image)

            # Convert PIL Image to numpy array
            content_image = np.array(content_image)
            style_image = np.array(style_image)

            # Path of the pre-trained TF model
            model_path = r"model"

            # output image
            styled_image = transfer_style(content_image, style_image, model_path)
            if style_image is not None:
                # some baloons
                st.balloons()

            col1, col2 = st.columns(2)
            with col1:
                # Display the output
                st.image(styled_image)
            with col2:

                st.markdown("</br>", unsafe_allow_html=True)
                st.markdown(
                    "<b> Your Image is Ready ! Click below to download it. </b>", unsafe_allow_html=True)

                # de-normalize the image
                styled_image = (styled_image * 255).astype(np.uint8)
                # convert to pillow image
                img = Image.fromarray(styled_image)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                st.download_button(
                    label="Download image",
                    data=buffered.getvalue(),
                    file_name="output.png",
                    mime="image/png")
                


# -------------Video Style Transfer Section------------------------------------------------





with tab2:
    st.markdown('<h3 style="text-align:center;">Video Style Transfer</h3>', unsafe_allow_html=True)

    video_file = st.file_uploader(
        "Upload Video (MP4 only)", type=['mp4'], key="video_uploader"
    )

    style_images = st.file_uploader(
        "Upload Style Images (PNG & JPG, select multiple)", type=['png', 'jpg'], accept_multiple_files=True, key="style_images_uploader"
    )

    if video_file is not None and style_images and len(style_images) > 0:
        st.info(f"{len(style_images)} style image(s) selected.")
        with st.spinner("Stylizing video... This may take a few minutes."):
            # Read video bytes
            video_bytes = video_file.read()
            # Read style images as numpy arrays
            style_imgs = [np.array(Image.open(img)) for img in style_images]
            # Path of the pre-trained TF model
            model_path = r"model"
            # Stylize video (implement this function in your API)
            output_video_bytes = transfer_video_style(video_bytes, style_imgs, model_path)
            # Display result
            st.video(output_video_bytes)
            st.download_button(
                label="Download Stylized Video",
                data=output_video_bytes,
                file_name="stylized_output.mp4",
                mime="video/mp4"
            )
