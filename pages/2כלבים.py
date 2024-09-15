import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu
import background
from google.oauth2.service_account import Credentials
from datetime import datetime
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

# Directory for storing adopter files
FILES_DIR = 'Data/Adopters/'
url = "https://docs.google.com/spreadsheets/d/1g1WWygeD3ZE_uDGQRd2EL44NUHioLHVacsX_7Z8uu5Q/edit?usp=sharing"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = SCOPES)
    client = gspread.authorize(creds)
    return client

# Open the spreadsheet and worksheet
def open_google_sheet():
    client = get_gspread_client()
    sheet = client.open_by_key("1g1WWygeD3ZE_uDGQRd2EL44NUHioLHVacsX_7Z8uu5Q")
    worksheet = sheet.worksheet("Sheet1")  # Name of the sheet
    return worksheet
    
def update_google_sheet(edited_df):
    worksheet = open_google_sheet()
    # Replace NaN and infinite values before saving
    edited_df.replace([float('inf'), float('-inf')], '', inplace=True)
    edited_df.fillna('', inplace=True)
    # Overwrite the entire sheet (simpler approach)
    worksheet.clear()  # Clear existing content
    worksheet.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())  # Update with new data

        
@st.cache_data()
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
    data = conn.read(spreadsheet=url)
    return data

    
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)

# Calculate age in months
def calculate_age_in_months(birth_date):
    today = datetime.today()
    age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
    return age_in_months

def show_dogs_page():
    st.set_page_config(page_title='Dogs', layout='wide')
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
        
    background.insert_logo("כלבים")
    # Hebrew column mapping
    hebrew_columns_dogs = {
        'DogID': 'מזהה כלב',
        'Name': 'שם',
        'DateOfBirth': 'תאריך לידה',
        'Age': 'גיל',
        'Breed': 'זן',
        'Weight': 'משקל',
        'Size': 'גודל',
        'Gender': 'מין',
        'RescueDate': 'תאריך חילוץ',
        'Rabies_Done': 'חיסון כלבת',
        'Hexagonal_1': 'חיסון משושה 1',
        'Hexagonal_2': 'חיסון משושה 2',
        'Hexagonal_3': 'חיסון משושה 3',
        'Hexagonal_Done': 'חיסון משושה',
        'Spayed': 'מעוקר',
        'De-worm': 'טיפול נגד תולעים',
        'Children_Friendly': 'ידידותי לילדים',
        'AnimalFriendly': 'ידידותי לכלבים',
        'HealthStatus': 'מצב הכלב',
        'EnergyLevel': 'רמת האנרגיה',
        'PhotographStatus': 'סטטוס הצילום',
        'AdoptionStatus': 'סטטוס אימוץ',
        'AdopterID': 'מזהה מאמץ',
        'PottyTrained': 'מחונך לצרכים',
        'AdoptionName': 'שם המאומץ'
    }

    # Translate English column names to Hebrew

    # Add your option_menu logic and other dog page features here

    selected = option_menu(
        menu_title="",  # Required
        options=["הוסף כלב","כל הטבלה"],  # Required
        icons=["upload",  "file", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=2,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
        )

    if selected == "כל הטבלה":
        data = fetch_data()  # Fetch the data from Google Sheets
        # Rename the columns using your Hebrew dictionary
        data.rename(columns=hebrew_columns_dogs, inplace=True)
        # Display the edtable DataFrame
        edited_df = st.experimental_data_editor(data)

        # Add a save button to save the changes
        if st.button('שמור שינויים'):
            update_google_sheet(edited_df)
    if selected == "הוסף כלב":
        st.subheader('הוסף כלב חדש')
        with st.form(key='insert_form'):
            DogID = st.text_input('מזהה כלב')
            name = st.text_input('שם')
            date_of_birth = st.date_input('תאריך לידה')
            breed = st.text_input('זן')
            weight = st.number_input('משקל', min_value=0.0, max_value=100.0, step=0.1)
            size = st.selectbox('גודל', ['קטן', 'בינוני', 'גדול'])
            gender = st.selectbox('מין', ['זכר', 'נקבה'])
            rescueDate = st.date_input('תאריך חילוץ')
            rabies_date = st.date_input('תאריך חיסון כלבת', value=None)
            hexagonal_1_date = st.date_input('תאריך חיסון משושה 1', value=None)
            hexagonal_2_date = st.date_input('תאריך חיסון משושה 2', value=None)
            hexagonal_3_date = st.date_input('תאריך חיסון משושה 3', value=None)
            de_worm_date = st.date_input('תאריך טיפול נגד תולעים', value=None)
            spayed = st.checkbox('מעוקר')
            children_friendly = st.checkbox('ידידותי לילדים')
            animal_friendly = st.checkbox('ידידותי לכלבים')
            health_status = st.text_input('מצב הכלב')
            energy_level = st.selectbox('רמת האנרגיה', ['נמוכה', 'בינונית', 'גבוהה'])
            photograph_status = st.selectbox('סטטוס הצילום', ['ממתין לצילום', 'צילום הושלם'])
            adoption_status = st.selectbox('סטטוס אימוץ', ['זמין לאימוץ', 'נאסף'])
            adopterID = st.text_input('מזהה מאמץ')
            potty_trained = st.checkbox('מחונך לצרכים')

            submit_button = st.form_submit_button(label='הוסף כלב')

        if submit_button:
            age = calculate_age_in_months(date_of_birth) if date_of_birth else 0
            new_dog = {
                'DogID': DogID,
                'Name': name,
                'DateOfBirth': date_of_birth.strftime('%Y-%m-%d'),
                'Age': age,
                'Breed': breed,
                'Weight': weight,
                'Size': size,
                'Gender': gender,
                'RescueDate': rescueDate.strftime('%Y-%m-%d'),
                'Rabies_Done': rabies_date.strftime('%Y-%m-%d') if rabies_date else np.nan,
                'Hexagonal_1': hexagonal_1_date.strftime('%Y-%m-%d') if hexagonal_1_date else np.nan,
                'Hexagonal_2': hexagonal_2_date.strftime('%Y-%m-%d') if hexagonal_2_date else np.nan,
                'Hexagonal_3': hexagonal_3_date.strftime('%Y-%m-%d') if hexagonal_3_date else np.nan,
                'De-worm': de_worm_date.strftime('%Y-%m-%d') if de_worm_date else np.nan,
                'Spayed': spayed,
                'Children_Friendly': children_friendly,
                'AnimalFriendly': animal_friendly,
                'HealthStatus': health_status,
                'EnergyLevel': energy_level,
                'PhotographStatus': photograph_status,
                'AdoptionStatus': adoption_status,
                'AdopterID': adopterID,
                'PottyTrained': potty_trained,
            }
            dog_df = dog_df.append(new_dog, ignore_index=True)
            # Update the Google Sheet with the new dog entry
            update_google_sheet(dog_df)
            st.success('הכלב הוסף בהצלחה!')

# Call the function to display the dogs page
show_dogs_page()
