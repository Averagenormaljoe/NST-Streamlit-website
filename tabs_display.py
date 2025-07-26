import streamlit as st

from UI_components import example_images, header
from tabs.gatys_tab import gatys_tab
from tabs.johnson_tab import johnson_tab
from tabs.video_tab import video_tab
from tabs.huang_tab import huang_tab
from tabs.default_tab import default_tab
def tabs_display():
    tab_list : list[str] = ["Main (StyleMotion)", "Johnson model", "Gatys model", "Huang model"]
    tab1, tab2,tab3,tab4 = st.tabs(tab_list[0:4])  # Exclude the last tab for now

    # -------------Header Section------------------------------------------------

    with tab1:
        header()

    with tab2:
        header() 
    with tab3:
        header()
    # with tab4:
    #     header()


    # -------------Sidebar Section------------------------------------------------


    with st.sidebar:

        # ---------------------Example art images------------------------------

        example_images()

    # ----------------------------------------------------------------------

    # -------------Body Section------------------------------------------------
    with tab1:
        default_tab()

                
    # # -------------Johnson Model Section------------------------------------------------             
    with tab2:
         johnson_tab()
    # # -------------Gatys Model Section------------------------------------------------        
    with tab3:
         gatys_tab()
    # # -------------Huang Model Section------------------------------------------------    

    # with tab4:
    #     huang_tab()
