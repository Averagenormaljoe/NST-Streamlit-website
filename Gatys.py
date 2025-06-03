import streamlit as st


def render_gatys_ui_sliders():
    # Style intensity slider
    style_intensity = st.slider(
        "Select Style Intensity", 
        min_value=0.1, max_value=1.0, value=0.5, step=0.1, 
        help="Adjust the intensity of the style transfer effect."
    )
    
    st.markdown('<h3 style="text-align:center;">Gatys model</h3>', unsafe_allow_html=True)
    st.markdown('<h4 style="text-align:center;">Provides the highest style quality at the cost of speed (will take around 5 minutes)</h4>', unsafe_allow_html=True)
    epoch_slider = st.slider(
          "Select Epochs",
          min_value=1, max_value=1000, value=10, step=1,
          help="Set the number of epochs for the style transfer. More epochs may yield better results but will take longer."
      )
    return epoch_slider, style_intensity