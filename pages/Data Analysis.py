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
    aplications_file_path = "Data/AdoptionApplication.csv"
    if not os.path.exists(aplications_file_path):
        st.error("No file")
        st.stop()
    df = pd.read_csv(aplications_file_path)
    df


show_data_analysis_page()
