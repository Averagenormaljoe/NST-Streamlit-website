import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
def processing_btn(is_processing : bool) -> bool:
    if is_processing:
        if st.button("Stop Processing"):
            is_processing = False
            st.warning("Processing stopped by user.")
    return is_processing


def file_uploader_for_images(method =  "") -> tuple[UploadedFile | None, UploadedFile | None]:
    col1, col2 = st.columns(2)

    with col2:
        style_image = st.file_uploader(
            "Upload Style Image (PNG & JPG images only)", type=['png', 'jpg'])
    with col1:
        if method == 'Image':
            content_image = st.file_uploader(
                "Upload Content Image (PNG & JPG images only)", type=['png', 'jpg'])
            return content_image, style_image
    return None, style_image