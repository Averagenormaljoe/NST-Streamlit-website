import streamlit as st

from UI_components import example_images, header
from tabs.gatys_tab import gatys_tab
from tabs.johnson_tab import johnson_tab
from tabs.video_tab import video_tab
from tabs.huang_tab import huang_tab
from tabs.default_tab import default_tab
def tabs_display():
  
    # -------------Header Section------------------------------------------------

    
    header()
  
    # with tab3:
    #     header()
    # with tab4:
    #     header()
    # with tab5:
    #     header()


    # -------------Sidebar Section------------------------------------------------


    with st.sidebar:

        # ---------------------Example art images------------------------------

        example_images()

    # ----------------------------------------------------------------------

    # -------------Body Section------------------------------------------------
    
    default_tab()

    # # -------------Video Style Transfer Section------------------------------------------------
                
    # # -------------Johnson Model Section------------------------------------------------             
    # with tab3:
    #     johnson_tab()
    # # -------------Gatys Model Section------------------------------------------------        
    # with tab4:
    #     gatys_tab()
    # # -------------Huang Model Section------------------------------------------------    

    # with tab5:
    #     huang_tab()