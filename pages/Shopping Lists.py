
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title='ShoppingList', layout='wide')
st.session_state['list'] = False


con1 = st.container()
with con1:
    col1, col2= st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)


def show_shopping_list_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
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
        dogs_file_path = "Data/Dogs.csv"
        dog_df = pd.read_csv(dogs_file_path, encoding='utf-8')
        dog_df = dog_df[dog_df['AdoptionStatus'] == 0]

        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.selectbox('בחר כלב:', dog_df['Name'].unique())
            with col2:
                if st.button("צור רשימה"):
                    st.session_state['list'] = True

    if selected == "הוסף מוצר":
        st.session_state['list'] = False
        st.write("not yet")



show_shopping_list_page()
