import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

def show_data_analysis_page():
    st.set_page_config(page_title='Data Analysis', layout='wide')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    # Load adopter data
    adopter_file_path = "Data/adopter.csv"
    if not os.path.exists(adopter_file_path):
        st.error("The adopter file does not exist.")
        st.stop()


show_data_analysis_page()
