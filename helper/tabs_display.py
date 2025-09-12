import streamlit as st

from helper.UI_components import example_images, header
from tabs.johnson_tab import johnson_tab
from tabs.default_tab import default_tab
def tabs_display():
    tab_list : list[str] = ["Main (StyleMotion)"]
    tab1, = st.tabs(tab_list[0:1])

    # -------------Header Section------------------------------------------------

    with tab1:
        header()



    # -------------Sidebar Section------------------------------------------------


    with st.sidebar:

        # ---------------------Example art images------------------------------

        example_images()

    # ----------------------------------------------------------------------

    # -------------Body Section------------------------------------------------
    with tab1:
        default_tab()

                

    # # -------------Gatys Model Section------------------------------------------------        

