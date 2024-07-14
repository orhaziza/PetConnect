import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

def plot_Applications(application_df):
    platform_counts = df['SourcePlatform'].value_counts()
    # plt.figure(figsize=(8, 8))
    # plt.pie(platform_counts, labels=platform_counts.index, autopct='%1.1f%%', startangle=140)
    fig, ax = plt.subplots()
    ax.pie(platform_counts, labels=platform_counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Requests by Platform')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)
    
def show_data_analysis_page():
    st.set_page_config(page_title='Data Analysis', layout='wide')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
    
    application_file_path = "Data/AdoptionApplication.csv"
    if not os.path.exists(application_file_path):
        st.error("applications file does not exist.")
        st.stop()
    application_df = pd.read_csv(application_file_path, encoding='Windows-1255')
    
    adopter_file_path = "Data/adopter.csv"
    if not os.path.exists(adopter_file_path):
        st.error("The adopter file does not exist.")
        st.stop()
    adopter_df = pd.read_csv(adopter_file_path, encoding='Windows-1255')

    dogs_file_path = "Data/Dogs.csv"
    if not os.path.exists(dogs_file_path):
        st.error("Dogs file does not exist.")
        st.stop()
    dogs_df = pd.read_csv(dogs_file_path, encoding='Windows-1255')

    FosterHome_file_path = "Data/FosterHome.csv"
    if not os.path.exists(FosterHome_file_path):
        st.error("Foster Home file does not exist.")
        st.stop()
    Foster_Home_df = pd.read_csv(dogs_file_path, encoding='Windows-1255')
    
    with st.container():
        col1 , col2 = st.columns([1,1], gap="small")
        with col1:
            plot_Applications(application_df)

show_data_analysis_page()
