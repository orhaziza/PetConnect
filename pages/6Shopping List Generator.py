
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
    st.set_page_config(page_title='ShoppingList', layout='wide')

    con1 = st.container()
    with con1:
        col1, col2= st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)

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
            col1, col2 = st.columns([3, 1])
            with col1:
                dog = st.selectbox('בחר כלב:', dog_df['Name'].unique())
            with col2:
                if st.button("צור רשימה"):
                    with st.form("my_form"):
                        create_list(dog)
                        submitted = st.form_submit_button("Download")
                        if submitted:
                            st.write("downloading data")

    if selected == "הוסף מוצר":
        st.write("not yet")

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

def create_list(dog):
    df = dog_df.loc[dog_df['Name'] == dog].reset_index()
    categories = items_df['Product Category'].unique()
    sl = items_df.iloc[:0,:].copy()
    flag = False
    if not (df["Size"][0]=='XS' or df["Size"][0]=='S' or df["Size"][0]=='M' or df["Size"][0]=='L' or df["Size"][0]=='XL'):
        st.warning('Dog has NO size!')
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
