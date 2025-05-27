import streamlit as st
def processingBtn(is_processing : bool) -> bool:
    if is_processing:
        if st.button("Stop Processing"):
            is_processing = False
            st.warning("Processing stopped by user.")
    return is_processing
