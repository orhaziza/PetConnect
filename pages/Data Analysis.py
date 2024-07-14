import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title='Data Analysis', layout='wide')
st.markdown("<h1 style='text-align: center;'>Data Analysis Page</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>כאן תוכלו לצפות בויזואליזציות על בסיס הנתונים שנאספו עד כה</h3>", unsafe_allow_html=True)

def plot_Applications(application_df):
    platform_counts = application_df['SourcePlatform'].value_counts()
    labels = [label[::-1] for label in platform_counts.index.tolist()]
    values = platform_counts.tolist()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    
    ax.pie(values, labels, colors=['b', 'r', 'g'], autopct='%1.1f%%', startangle=140, radius=1.5)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

def plot_Dogs(dogs_df):
    lst = ['age', 'breed', 'size', 'gender', 'vaccine_1', 'vaccine_2', 'isSpay', 'childrenFirendly', 'animalFirendly', 'healthStatus', 'energylevel', 'photographStatus', 'adoptionStatus', 'pottyTrained']
    characteristic = st.selectbox('בחר מאפיין', lst)
    
    if dogs_df[characteristic].dtype == 'bool':
      # Convert boolean to string
        distribution = dogs_df[characteristic].astype(str).value_counts()
        st.subheader(f'Distribution of Dogs by {characteristic.capitalize()}')
        st.bar_chart(distribution)
        
    else:
        distribution = dogs_df[characteristic].value_counts()
        st.subheader(f'Distribution of Dogs by {characteristic.capitalize()}')
        st.bar_chart(distribution)

    
def show_data_analysis_page():
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
            st.write('התפלגות בקשות אימוץ לפי פלטפורמת פרסום:')
            plot_Applications(application_df)
        with col2:
            st.write('התפלגות הכלבים בעמותה:')
            plot_Dogs(dogs_df)

    with st.container():
        col1 , col2 = st.columns([1,1], gap="small")
        with col1:
            st.write('התפלגות בקשות אימוץ לפי פלטפורמת פרסום:')
            plot_Applications(application_df)
        with col2:
            st.write('התפלגות הכלבים בעמותה:')
            plot_Dogs(dogs_df)

show_data_analysis_page()
