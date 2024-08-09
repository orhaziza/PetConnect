
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

st.session_state['list'] = False
items_file_path = "Data/Shopping List.csv"
items_df = pd.read_csv(items_file_path, encoding='utf-8')
dogs_file_path = "Data/Dogs.csv"
dog_df = pd.read_csv(dogs_file_path, encoding='utf-8')
dog_df = dog_df[dog_df['AdoptionStatus'] == 0]

def show_shopping_list_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    st.set_page_config(page_title='Shopping List', layout='wide')
    with st.container():
        col4, col1, col2 = st.columns([1, 10, 1])
        with col1:
            st.markdown("<h1 style='text-align: center;'>רשימת קניות</h1>", unsafe_allow_html=True)
        with col2:
            st.image("Data/Logo.png", width=100)

        url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"
        # Custom CSS to center-align the option menu
    st.markdown(
        """
        <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    .stButton > button {
        color: #ffffff; /* White text for buttons */
        background-color: #30475E; /* Dark blue color for buttons */
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-size: 1em;
    }
    .stButton > button:hover {
        background-color: #25394C; /* Darker blue on hover */
        transform: scale(1.05);
    }
    .stButton > button.logout {
        background-color: #F05454; /* Red color for logout button */
        border-radius: 5px;
        transition: background-color 0.3s, transform 0.3s;
        padding: 10px 20px;
        font-size: 1em;
    }
    .stButton > button.logout:hover {
        background-color: #C74444; /* Darker red on hover */
        transform: scale(1.05);
    }
    .icon-button {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .icon-button img {
        margin-right: 5px;
    }
    .option-menu-container {
        display: flex;
        justify-content: center;
    }
    .dataframe-container {
        background-color: #ffffff; /* White background for dataframe */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 10px;
    }
    .file-upload-container {
        background-color: #ffffff; /* White background for file upload */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-top: 20px;
    }
    .stDownloadButton > button {
        color: #ffffff; /* White text for download buttons */
        background-color: #30475E; /* Dark blue color for download buttons */
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-size: 1em;
    }
    .stDownloadButton > button:hover {
        background-color: #25394C; /* Darker blue on hover */
        transform: scale(1.05);
    }
    </style>

        """,
        unsafe_allow_html=True
    )
    # Define the menu options
    selected = option_menu(
        menu_title="",  # Required
        options=["צור רשימה לכלב", "הוסף מוצר"],  # Added new option for the table with scores
        icons=["file", "search", "file", "upload", "table"],  # Optional
        menu_icon="menu",  # Optional
        default_index=0,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles={
            "container": {"class": "option-menu-container"}}
                    )
    if selected == "צור רשימה לכלב":
        col3, col1, col2, col4 = st.columns([0.5, 4.5, 1, 0.5])
        with col1:
            st.markdown(
                """
                <style>
                [data-baseweb="select"] {
                    margin-top: -40px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            dog = st.selectbox(label='',options=dog_df['Name'].unique(),index=None, placeholder="בחר כלב")
        with col2:
            if st.button("צור רשימה"):
                st.session_state['list']=True
            
    if st.session_state['list']:
        create_list(dog)

    if selected == "הוסף מוצר":
        st.write("not yet")

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.switch_page("Home.py")
        st.experimental_rerun()

def create_list(dog):
    df = dog_df.loc[dog_df['Name'] == dog].reset_index()
    categories = items_df['Product Category'].unique()
    sl = items_df.iloc[:0,:].copy()
    flag = False
    if not (df["Size"][0]=='XS' or df["Size"][0]=='S' or df["Size"][0]=='M' or df["Size"][0]=='L' or df["Size"][0]=='XL'):
        st.warning('Dog has NO size!')
        st.stop
        flag = True
    for c in categories:
        if c=="גורים":
            if df["Age"][0]<12:
                category_products = items_df[items_df['Product Category'] == c]
                sl = pd.concat([sl, category_products], ignore_index=True) 
        else:    
            if not flag:
                category_products = items_df[items_df['Product Category'] == c]
                sl = pd.concat([sl, category_products[category_products['Dog Size'] == df["Size"][0]]], ignore_index=True) 
    
    sl['new_column'] = True
    sl = st.data_editor(sl) 
        
    
show_shopping_list_page()
