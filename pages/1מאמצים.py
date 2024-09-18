import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
import background
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

# Directory for storing adopter files
FILES_DIR = 'Data/Adopters/'
url = "https://docs.google.com/spreadsheets/d/1zGvjYm0Co2tLrA4TD1hiMkq4zbeNtagNbj21kAXeWc0/edit?usp=sharing"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = SCOPES)
    client = gspread.authorize(creds)
    return client

# Open the spreadsheet and workshe
def open_google_sheet():
    client = get_gspread_client()
    sheet = client.open_by_key("1zGvjYm0Co2tLrA4TD1hiMkq4zbeNtagNbj21kAXeWc0")
    worksheet = sheet.worksheet("Sheet1")  # Name of the sheet
    return worksheet
    
def update_google_sheet(edited_df):
    worksheet = open_google_sheet()

    # Replace NaN and infinite values before saving
    edited_df.replace([float('inf'), float('-inf')], '', inplace=True)
    edited_df.fillna('', inplace=True)

    # Option 1: Overwrite the entire sheet (simpler approach)
    worksheet.clear()  # Clear existing content
    worksheet.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())  # Update with new data

        
@st.cache_data()
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
    return conn.read(spreadsheet=url)
    
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
    
def load_adopters_data():
    adopter_file_path = 'Data/Adopters.csv'
    adopters_df = pd.read_csv(adopter_file_path, encoding='utf-8')
    return adopters_df

# Function to save a file
def save_file(adopter_id, file):
    try:
        file_name = f'{adopter_id}_{file.name}'
        file_path = os.path.join(FILES_DIR, file_name)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        st.success('File saved successfully')
    except Exception as e:
        st.error(f'Error saving file: {e}')
        raise

# Function to delete a file
def delete_file(file_name):
    try:
        file_path = os.path.join(FILES_DIR, file_name)
        os.remove(file_path)
        st.success(f'File {file_name} deleted successfully.')
    except Exception as e:
        st.error(f'Error deleting file: {e}')
        raise

# Function to load a file for download
def load_file(file_name):
    file_path = os.path.join(FILES_DIR, file_name)
    with open(file_path, 'rb') as f:
        file_bytes = f.read()
    return file_bytes

def add_adopter_to_google_sheet(new_adopter):
    worksheet = open_google_sheet()
        # Replace NaN and infinite values before saving
    def sanitize_value(value):
        if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
            return ''
        return value
    
    # Append the new adopter data as a new row in the sheet
    worksheet.append_row([
        new_adopter['dog_chipID'],
        new_adopter['AdopterID'],
        new_adopter['AdopterName'],
        new_adopter['Second_adopterID'],
        new_adopter['Second_adopterName'],
        new_adopter['Floor'],
        new_adopter['Apartment'],
        new_adopter['Address_street_number'],
        new_adopter['Address_street'],
        new_adopter['Address_city'],
        new_adopter['adopter_phone_num'],
        new_adopter['Second_adopter_phone_num'],
        new_adopter['Adopter_mail'],
        new_adopter['Second_adopter_mail'],
        new_adopter['preferences'],
        new_adopter['LifeStyleInformation'],
        new_adopter['AdoptionDate'],
        new_adopter['Documents'],
        new_adopter['ownership_form'],
        new_adopter['ownership_transfer'],
        new_adopter['Payment_type'],
        new_adopter['Recieipt_Num'],
        new_adopter['Security_payment']
    ])  # Add the new adopter's data

def show_adopters_page():
    st.set_page_config(page_title='Adopters', layout='wide')
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
        
    background.insert_logo("מאמצים")
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

    selected = option_menu(
        menu_title="",  # Required
        options=["ערוך מסמך","הוסף מאמץ","כל הטבלה"],  # Required
        icons=["upload",  "file", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=2,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
        )

    if st.button('רענן את העמוד'):
        st.cache_data.clear()
        st.success("המידע עודכן!")
    # Display different pages based on selected option
    if selected == "כל הטבלה":
        # data = fetch_data()  # Fetch the data from Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1zGvjYm0Co2tLrA4TD1hiMkq4zbeNtagNbj21kAXeWc0/edit?usp=sharing")

        # Rename the columns using your Hebrew dictionary
        data.rename(columns=hebrew_columns_adopters, inplace=True)

        # Display the editable DataFrame
        edited_df = st.experimental_data_editor(data)

        # Add a save button to save the changes
        if st.button('שמור שינויים'):
            update_google_sheet(edited_df)
            st.success("השינויים נשמרו!")
                
    elif selected == "הוסף מאמץ":
        st.subheader('הוסף מאמץ')
        # Input fields for the adopter form
        dog_chipID = st.text_input('מזהה שבב כלב')
        adopter_id = st.text_input('מזהה מאמץ')
        adopter_name = st.text_input('שם מאמץ')
        second_adopter_id = st.text_input('מזהה מאמץ נוסף')
        second_adopter_name = st.text_input('שם מאמץ נוסף')
        floor = st.text_input('קומה')
        apartment = st.text_input('דירה')
        address_street_number = st.text_input('מספר רחוב')
        address_street = st.text_input('רחוב')
        address_city = st.text_input('עיר')
        adopter_phone_num = st.text_input('מספר טלפון מאמץ')
        second_adopter_phone_num = st.text_input('מספר טלפון מאמץ נוסף')
        adopter_mail = st.text_input('דוא"ל מאמץ')
        second_adopter_mail = st.text_input('דוא"ל מאמץ נוסף')
        preferences = st.text_area('העדפות')
        lifestyle_info = st.text_area('מידע על אופני חיים')
        adoption_date = st.date_input('תאריך אימוץ', datetime.today())
        documents = st.text_area('מסמכים')
        ownership_form = st.text_input('טופס בעלות')
        ownership_transfer = st.text_input('העברת בעלות')
        payment_type = st.text_input('סוג תשלום')
        receipt_num = st.text_input('מספר קבלה')
        security_payment = st.text_input('תשלום ביטחון')

        # Save the new adopter data
        if st.button('שמור מאמץ'):
            new_adopter = {
                'dog_chipID': dog_chipID,
                'AdopterID': adopter_id,
                'AdopterName': adopter_name,
                'Second_adopterID': second_adopter_id,
                'Second_adopterName': second_adopter_name,
                'Floor': floor,
                'Apartment': apartment,
                'Address_street_number': address_street_number,
                'Address_street': address_street,
                'Address_city': address_city,
                'adopter_phone_num': adopter_phone_num,
                'Second_adopter_phone_num': second_adopter_phone_num,
                'Adopter_mail': adopter_mail,
                'Second_adopter_mail': second_adopter_mail,
                'preferences': preferences,
                'LifeStyleInformation': lifestyle_info,
                'AdoptionDate': adoption_date.strftime('%Y-%m-%d'),
                'Documents': documents,
                'ownership_form': ownership_form,
                'ownership_transfer': ownership_transfer,
                'Payment_type': payment_type,
                'Recieipt_Num': receipt_num,
                'Security_payment': security_payment
            }

            try:
                # Add the new record to the Google Sheet
                add_adopter_to_google_sheet(new_adopter)
                st.success('מאמץ חדש נשמר בהצלחה!')
                st.balloons()  # Show the balloons animation for success
            except Exception as e:
                st.error(f'Error saving adopter: {e}')
            
            st.success('מאמץ חדש נשמר בהצלחה!')
            # Show balloon animation
            st.balloons()

    elif selected == "ערוך מסמך":
        st.title('מסמכים')
        
        # Load adopter data
        # adopter_df = fetch_data()  # Fetch the data from Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1zGvjYm0Co2tLrA4TD1hiMkq4zbeNtagNbj21kAXeWc0/edit?usp=sharing")
        hebrew_columns_adopters = {
            # Your column translation dictionary for adopters
            'AdopterID': 'מזהה מאמץ',
            # Add other columns as needed
        }
       

        # Select adopter
        adopter_id = st.selectbox('Select Adopter ID', adopter_df['מזהה מאמץ'])

        if adopter_id:
            st.subheader(f'מסמכים של מאמץ {adopter_id}')

            # List existing files
            files = [f for f in os.listdir(FILES_DIR) if f.startswith(f'{adopter_id}_')]
            if files:
                st.write('קבצים שיש במערכת ')
                for file_name in files:
                    st.write(file_name)
                    with open(os.path.join(FILES_DIR, file_name), "rb") as file:
                        btn = st.download_button(
                        label=f"הורד {file_name}",
                        data=file,
                        file_name=file_name,
                        mime='application/octet-stream'
                        )
                    if st.button(f'מחק {file_name}', key=f'מחק_{file_name}'):
                        delete_file(file_name)

        # File upload section
            uploaded_file = st.file_uploader('העלאת קובץ', type='pdf')
    
            if uploaded_file is not None:
                if uploaded_file.name:
                    if st.button('העלה את הקובץ'):
                        save_file(adopter_id, uploaded_file)
                else:
                    st.error('אין שם לקובץ ')

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

st.session_state["step"] = 0
show_adopters_page()
