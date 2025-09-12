import streamlit as st

from helper.UI_components import example_images, header
from tabs.johnson_tab import johnson_tab
from tabs.default_tab import default_tab
def tabs_display() -> None:
    tab_list : list[str] = ["Johnson model"]
    tab1,  = st.tabs(tab_list)

    # -------------Header Section------------------------------------------------

    with tab1:
        header()




    # -------------Sidebar Section------------------------------------------------


    with st.sidebar:

        # ---------------------Example art images------------------------------

        example_images()

    # ----------------------------------------------------------------------

    # -------------Body Section------------------------------------------------
                
    # # -------------Johnson Model Section------------------------------------------------             
    with tab1:
         johnson_tab()
    # # -------------Gatys Model Section------------------------------------------------        

