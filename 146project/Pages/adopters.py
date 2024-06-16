import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Adopters', layout='wide')

if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("לא ניתן לגשת לעמוד ללא התחברות")
    st.stop()

# Load adopter data
adopter_file_path = "Data/adopter.csv"
if not os.path.exists(adopter_file_path):
    st.error("The adopter file does not exist.")
    st.stop()

adopter_df = pd.read_csv(adopter_file_path, encoding='Windows-1255')

# Define Hebrew column names for adopters
hebrew_columns_adopters = {
    'AdopterID': 'מזהה אומץ',
    'AdopterName': 'שם אומץ',
    'Address': 'כתובת',
    'contactinformation': 'פרטי קשר',
    'preferences': 'העדפות',
    'LifeStyleInformation': 'מידע על אופני חיים',
    'AdoptionDate': 'תאריך אימוץ',
    'Documents': 'מסמכים',
}

# Define the menu options
with st.sidebar:
    selected = option_menu("אומצים", ["כל הטבלה", "מצא אומץ", "הוסף אומץ", "ערוך מסמך"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)

# Translate column names
adopter_df_hebrew = adopter_df.rename(columns=dict(zip(adopter_df.columns, [hebrew_columns_adopters.get(col, col) for col in adopter_df.columns])))

# Display different pages based on selected option
if selected == "כל הטבלה":
    st.dataframe(adopter_df_hebrew)

elif selected == "מצא אומץ":
    st.subheader('מצא אומץ')

    # Create search filters for adopters
    col1, col2 = st.columns(2)

    with col1:
        adopter_name = st.text_input('שם אומץ')
    with col2:
        adoption_date = st.date_input('תאריך אימוץ')

    # Apply search filters
    filtered_adopters = adopter_df_hebrew[
        (adopter_df_hebrew['שם אומץ'].str.contains(adopter_name, na=False, case=False)) &
        (adopter_df_hebrew['תאריך אימוץ'] == adoption_date.strftime('%Y-%m-%d'))
    ]

    st.dataframe(filtered_adopters)

elif selected == "הוסף אומץ":
    st.subheader('הוסף אומץ')

    # Add adoption form or input fields here
    adopter_id = st.text_input('מזהה אומץ')
    adopter_name = st.text_input('שם אומץ')
    address = st.text_area('כתובת')
    contact_info = st.text_input('פרטי קשר')
    preferences = st.text_area('העדפות')
    lifestyle_info = st.text_area('מידע על אופני חיים')
    adoption_date = st.date_input('תאריך אימוץ', datetime.today())
    documents = st.text_area('מסמכים')

    if st.button('שמור אומץ'):
        # Save adopter data to CSV or database
        new_adopter = {
            'מזהה אומץ': adopter_id,
            'שם אומץ': adopter_name,
            'כתובת': address,
            'פרטי קשר': contact_info,
            'העדפות': preferences,
            'מידע על אופני חיים': lifestyle_info,
            'תאריך אימוץ': adoption_date.strftime('%Y-%m-%d'),
            'מסמכים': documents
        }
        adopter_df_hebrew = adopter_df_hebrew.append(new_adopter, ignore_index=True)
        adopter_df_hebrew.to_csv(adopter_file_path, index=False, encoding='Windows-1255')
        st.success('אומץ חדש נשמר בהצלחה!')

elif selected == "ערוך מסמך":
    st.subheader('ערוך מסמך')

    # Edit document functionality
    # Implement as per your requirements

# Sidebar logout button
if st.sidebar.button("Log Out"):
    st.session_state['logged_in'] = False
    st.experimental_rerun()



