import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import numpy as np
from streamlit_gsheets import GSheetsConnection


st.set_page_config(page_title='Data Analysis', layout='wide')
#logo
con1 = st.container()
with con1:
    col1, col2= st.columns([5, 1])
    with col1:
        st.markdown("<h1 style='text-align: center;'>Data Analysis Page</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>כאן תוכלו לצפות בויזואליזציות על בסיס הנתונים שנאספו עד כה</h3>", unsafe_allow_html=True)
    with col2:
        st.image("Data/Logo.png", width=100)

def plot_Applications(application_df):
    platform_counts = application_df.iloc[:, 1].value_counts()
    labels = [label[::-1] for label in platform_counts.index.tolist()]
    values = platform_counts.tolist()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    ax.pie(values, labels = labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

def plot_Fosters(Foster_Home_df):
    lst = ['HouseSize','Backyard','NearDogPark','HouseMembers','AvailabilityAtHome','ChildrenFriendly','AnimalFriendly','MaximumCapacity','AllowedAtProperty','Allergies','IsMobile','EnergyLevel','PastFosters','PastExperience']
    characteristic = st.selectbox('בחר מאפיין', lst)
    if Foster_Home_df[characteristic].dtype == 'bool':
        distribution = Foster_Home_df[characteristic].astype(str).value_counts()
        st.subheader(f'Distribution of foster homes by {characteristic.capitalize()}')
        st.bar_chart(distribution)
    else:
        distribution = Foster_Home_df[characteristic].value_counts()
        st.subheader(f'Distribution of foster homes by {characteristic.capitalize()}')
        st.bar_chart(distribution)

def plot_Dogs(dogs_df):
    lst = ['Age','Breed','Weight','Size','Gender','RescueDate','Rabies_Done','Hexagonal_1','Hexagonal_2','Hexagonal_3','Hexagonal_Done','Spayed','De-worm','ChildrenFriendly','AnimalFriendly','HealthStatus','EnergyLevel','PhotographStatus','AdoptionStatus','AdopterID','PottyTrained']
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

def plot_Applications_Flow(application_df):
    df = application_df["חותמת זמן"]
    df["חותמת זמן"] = pd.to_datetime(df["חותמת זמן"])
    view = st.radio("Select View", ("שבועי", "חודשי"))
    if view == "שבועי":
        df['Period'] = df["חותמת זמן"].dt.to_period('W').apply(lambda r: r.start_time)
        period_format = "%Y-%W"
    else:
        df['Period'] = df["חותמת זמן"].dt.to_period('M').apply(lambda r: r.start_time)
        period_format = "%Y-%m"
    df
    
def show_data_analysis_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"

    @st.cache_data()
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(spreadsheet=url)
    if st.button("עדכן"):
        st.cache_data.clear()
    
    adopter_file_path = "Data/Adopters.csv"
    if not os.path.exists(adopter_file_path):
        st.error("The adopter file does not exist.")
        st.stop()
    adopter_df = pd.read_csv(adopter_file_path, encoding='utf-8')

    dogs_file_path = "Data/Dogs.csv"
    if not os.path.exists(dogs_file_path):
        st.error("Dogs file does not exist.")
        st.stop()
    dogs_df = pd.read_csv(dogs_file_path, encoding='utf-8')

    FosterHome_file_path = "Data/FosterHome.csv"
    if not os.path.exists(FosterHome_file_path):
        st.error("Foster Home file does not exist.")
        st.stop()
    Foster_Home_df = pd.read_csv(FosterHome_file_path, encoding='utf-8')
    
    with st.container():
        col1 , col2 = st.columns([1,1], gap="small")
        with col1:
            st.write('התפלגות בקשות אימוץ לפי פלטפורמת פרסום:')
            plot_Applications(fetch_data())
        with col2:
            st.write('התפלגות הכלבים בעמותה:')
            plot_Dogs(dogs_df)

    with st.container():
        col1 , col2 = st.columns([1,1], gap="small")
        with col1:
            st.write('התפלגות בתי אומנה:')
            plot_Fosters(Foster_Home_df)
        with col2:
            st.write('בקשות אימוץ לאורך זמן:')
            plot_Applications_Flow(fetch_data())
            
show_data_analysis_page()
