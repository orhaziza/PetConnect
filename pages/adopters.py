import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
# Set up the page configuration at the top


def show_adopters_page():
    st.set_page_config(page_title='Adopters', layout='wide')
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    # Load adopter data
    adopter_file_path = "Data/Adopters.csv"
    if not os.path.exists(adopter_file_path):
        st.error("The adopter file does not exist.")
        st.stop()

    adopter_df = pd.read_csv(adopter_file_path, encoding='utf-8')

# Define Hebrew column names for adopters
    hebrew_columns_adopters = {
    'dog_chipID': 'שבב כלב',
    'AdopterID': 'מזהה מאמץ',
    'AdopterName': 'שם מאמץ',
    'Second_adopterID': 'מזהה מאמץ שני',
    'Second_adopterName': 'שם מאמץ שני',
    'Floor': 'קומה',
    'Apartment': 'דירה',
    'Address_street_number': 'מספר רחוב',
    'Address_street': 'רחוב',
    'Address_city': 'עיר',
    'adopter_phone_num': 'מספר טלפון של המאמץ',
    'Second_adopter_phone_num': 'מספר טלפון של המאמץ שני',
    'Adopter_mail': 'דואר אלקטרוני של המאמץ',
    'Second_adopter_mail': 'דואר אלקטרוני של המאמץ שני',
    'preferences': 'העדפות',
    'LifeStyleInformation': 'מידע על אופני חיים',
    'AdoptionDate': 'תאריך אימוץ',
    'Documents': 'מסמכים',
    'ownership_form': 'טופס בעלות',
    'ownership_transfer': 'העברת בעלות',
    'Payment_type': 'סוג תשלום',
    'Recieipt_Num': 'מספר קבלה',
    'Security_payment': 'תשלום ביטחון'
    # Add more column name translations as needed
    }



    # Use st.columns to create four equally sized columns
    # Use st.columns to create four equally sized columns
    col1, col2, col3, col4 = st.columns(4)

    # Button 1 in the first column
    with col1:
        if st.button("כלבים 🐶"):
            st.switch_page("pages/Dogs.py")

    # Button 2 in the second column
    with col2:
        if st.button("בתי אומנה 🏠"):
            st.switch_page("pages/FosterHome.py")

    # Button 3 in the third column
    with col3:
        if st.button("מאמצים 👤"):
            st.switch_page("pages/adopters.py")

    # Button 4 in the fourth column
    with col4:
        if st.button("בקשות 📁"):
            st.switch_page("pages/Applications.py")

    # # Define the menu options
    # with st.sidebar:
    #     selected = option_menu("מאמצים", ["כל הטבלה", "מצא מאמץ", "הוסף מאמץ", "ערוך מסמך"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)

    # Custom CSS to center-align the option menu
    st.markdown(
        """
        <style>
        .option-menu-container {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Define the menu options
    selected = option_menu(
        menu_title="מאמצים",  # Required
        options=["כל הטבלה", "מצא מאמץ", "הוסף מאמץ", "ערוך מסמך"],  # Required
        icons=["file", "search", "file", "upload"],  # Optional
        menu_icon="menu",  # Optional
        default_index=0,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles={
            "container": {"class": "option-menu-container"}
        }
    )

    # Translate column names
    adopter_df_hebrew = adopter_df.rename(
        columns=dict(zip(adopter_df.columns, [hebrew_columns_adopters.get(col, col) for col in adopter_df.columns])))

    # Display different pages based on selected option
    if selected == "כל הטבלה":
        st.dataframe(adopter_df_hebrew)

    elif selected == "מצא מאמץ":
        st.subheader('מצא מאמץ')

        # Create search filters for adopters
        col1, col2 = st.columns(2)

        with col1:
            adopter_name = st.text_input('שם מאמץ')
        with col2:
            adoption_date = st.date_input('תאריך אימוץ')

        # Apply search filters
        filtered_adopters = adopter_df_hebrew[
            (adopter_df_hebrew['שם מאמץ'].str.contains(adopter_name, na=False, case=False)) &
            (adopter_df_hebrew['תאריך אימוץ'] == adoption_date.strftime('%Y-%m-%d'))
            ]

        st.dataframe(filtered_adopters)

    elif selected == "הוסף מאמץ":
        st.subheader('הוסף מאמץ')

        # Add adoption form or input fields here
        adopter_id = st.text_input('מזהה מאמץ')
        adopter_name = st.text_input('שם מאמץ')
        address = st.text_area('כתובת')
        contact_info = st.text_input('פרטי קשר')
        preferences = st.text_area('העדפות')
        lifestyle_info = st.text_area('מידע על אופני חיים')
        adoption_date = st.date_input('תאריך אימוץ', datetime.today())
        documents = st.text_area('מסמכים')

        if st.button('שמור מאמץ'):
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
            # Create a DataFrame from the new adopter entry
            new_adopter_df = pd.DataFrame([new_adopter])
            
            # Concatenate the existing DataFrame with the new entry
            adopter_df_hebrew = pd.concat([adopter_df_hebrew, new_adopter_df], ignore_index=True)
            adopter_df_hebrew.to_csv(adopter_file_path, index=False, encoding='utf-8')
            st.success('מאמץ חדש נשמר בהצלחה!')
            # Show balloon animation
            st.balloons()  

    elif selected == "ערוך מסמך":
        st.subheader('ערוך מסמך')

        # Edit document functionality
        # Implement as per your requirements

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()



show_adopters_page()
