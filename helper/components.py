import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
def processing_btn(is_processing : bool) -> bool:
    if is_processing:
        if st.button("Stop Processing"):
            is_processing = False
            st.warning("Processing stopped by user.")
    return is_processing
