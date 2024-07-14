import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

def show_data_analysis_page():
    st.set_page_config(page_title='Data Analysis', layout='wide')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    # Load data
    application_file_path = "Data/AdoptionApplication.csv"
    if not os.path.exists(application_file_path):
        st.error("No file")
        st.stop()
        
    df = pd.read_csv(application_file_path, encoding='Windows-1255')
    platform_counts = df['SourcePlatform'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(platform_counts, labels=platform_counts.index, autopct='%1.1f%%', startangle=140)
    plt.show()


show_data_analysis_page()
