import streamlit as st

from helper.UI_components import example_images, header
from tabs.johnson_tab import johnson_tab
def tabs_display():
    tab_list : list[str] = ["Johnson model"]
    tab1, = st.tabs(tab_list)

    # -------------Header Section------------------------------------------------

    with tab1:
        header()
        johnson_tab()




    # -------------Sidebar Section------------------------------------------------


    with st.sidebar:

        # ---------------------Example art images------------------------------

        example_images()
