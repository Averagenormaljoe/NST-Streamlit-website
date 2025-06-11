import streamlit as st

from UI_components import example_images, header
from tabs import default_tab, gatys_tab, huang_tab, johnson_tab, video_tab
def tabs_display():
    tab_list : list[str] = ["Image", "Video", "Johnson model", "Gatys model", "Huang model"]
    tab1, tab2, tab3,tab4,tab5 = st.tabs(tab_list)

    # -------------Header Section------------------------------------------------

    with tab1:
        header()
    with tab2:
        header()
    with tab3:
        header()
    with tab4:
        header()
    with tab5:
        header()


    # -------------Sidebar Section------------------------------------------------


    with st.sidebar:

        # ---------------------Example art images------------------------------

        example_images()

    # ----------------------------------------------------------------------


    # -------------Body Section------------------------------------------------
    with tab1:
        default_tab()

    # -------------Video Style Transfer Section------------------------------------------------

    with tab2:
        video_tab()
                
    # -------------Johnson Model Section------------------------------------------------             
    with tab3:
        johnson_tab()
    # -------------Gatys Model Section------------------------------------------------        
    with tab4:
        gatys_tab()
    # -------------Huang Model Section------------------------------------------------    

    with tab5:
        huang_tab()