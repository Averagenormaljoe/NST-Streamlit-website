    
import streamlit as st
def display_styled_video(output_video : str, is_processing : bool = False):
    if output_video is None:
        st.error("No video generated.")
        return
    col1, col2 = st.columns(2)
    with col1:
        video_format = "video/mp4"
        st.video(output_video, format= video_format)
    with col2:
        is_processing = False
        video_ready_st(output_video)
    return is_processing     

def video_ready_st(f : str):
    st.markdown("</br>", unsafe_allow_html=True)
    st.markdown("<b> Your Stylized Video is Ready! Click below to download it. </b>", unsafe_allow_html=True)
    st.download_button("Download your video", f, file_name="output_video.mp4", mime="video/mp4")   
