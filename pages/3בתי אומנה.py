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
url = "https://docs.google.com/spreadsheets/d/1lAY6gHYO-scPukLMTH8msFzwG9DoNsdq5-kNf2lKbqM/edit?usp=sharing"

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
    sheet = client.open_by_key("1lAY6gHYO-scPukLMTH8msFzwG9DoNsdq5-kNf2lKbqM")
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
    

        
def save_file(foster_home_id, uploaded_file):
    with open(os.path.join(FILES_DIR, f'{foster_home_id}_{uploaded_file.name}'), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f'קובץ {uploaded_file.name} נשמר בהצלחה!')

def save_foster_home_to_csv(foster_home_df_hebrew, new_foster_home_df, csv_file_path):
    # Append the new data to the existing DataFrame
    updated_df = pd.concat([foster_home_df_hebrew, new_foster_home_df], ignore_index=True)

    # Debug: Print the DataFrame before saving
    st.write("Updated DataFrame:")
    st.write(updated_df)

    # Save to CSV
    updated_df.to_csv(csv_file_path, index=False, encoding='utf-8')

    # Debug: Check if the file was saved correctly
    if os.path.exists(csv_file_path):
        st.success(f"File saved successfully to {csv_file_path}.")
    else:
        st.error(f"Failed to save the file to {csv_file_path}.")

    return updated_df
def delete_file(file_name):
    os.remove(os.path.join(FILES_DIR, file_name))
    st.success(f'קובץ {file_name} נמחק בהצלחה!')

def add_foster_home_to_google_sheet(new_foster_home):
    worksheet = open_google_sheet()

    # Replace NaN and infinite values before saving
    def sanitize_value(value):
        if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
            return ''
        return value

    # Append the new foster home data as a new row in the sheet
    worksheet.append_row([
        sanitize_value(new_foster_home['FosterHomeID']),
        sanitize_value(new_foster_home['FosterName']),
        sanitize_value(new_foster_home['Address']),
        sanitize_value(new_foster_home['HouseSize']),
        sanitize_value(new_foster_home['Contactinfomation']),
        sanitize_value(new_foster_home['Backyard']),
        sanitize_value(new_foster_home['nearDogPark']),
        sanitize_value(new_foster_home['HouseMembers']),
        sanitize_value(new_foster_home['AvailabilityAtHome']),
        sanitize_value(new_foster_home['ChildrenFriendly']),
        sanitize_value(new_foster_home['AnimalFriendly']),
        sanitize_value(new_foster_home['MaximumCapacity']),
        sanitize_value(new_foster_home['allowedAtProperty']),
        sanitize_value(new_foster_home['allergies']),
        sanitize_value(new_foster_home['IsMobile']),
        sanitize_value(new_foster_home['EnergyLevel']),
        sanitize_value(new_foster_home['pastFosters']),
        sanitize_value(new_foster_home['pastExperience']),
        sanitize_value(new_foster_home['documents']),
    ])  # Add the new foster home's data


def show_foster_homes_page():
    st.set_page_config(page_title='Foster Homes', layout='wide')
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    background.insert_logo("בתי אומנה")

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"
        
    # Load foster home data
    foster_home_file_path = "Data/FosterHome.csv"
    if not os.path.exists(foster_home_file_path):
        st.error("The foster home file does not exist.")
        st.stop()

    foster_home_df = pd.read_csv(foster_home_file_path, encoding='utf-8')


    # Define Hebrew column names for foster homes
    hebrew_columns_foster_homes = {
        'FosterHomeID': 'מזהה בית אומנה',
        'FosterName': 'שם בית אומנה',
        'Address': 'כתובת',
        'HouseSize': 'גודל הבית',
        'Contactinfomation': 'פרטי קשר',
        'Backyard': 'חצר',
        'nearDogPark': 'קרוב לגן כלבים',
        'HouseMembers': 'חברי בית',
        'AvailabilityAtHome': 'זמינות בבית',
        'ChildrenFriendly': 'ידידותי לילדים',
        'AnimalFriendly': 'ידידותי לכלבים',
        'MaximumCapacity': 'קיבולת מקסימלית',
        'allowedAtProperty': 'מותר בנכס',
        'allergies': 'אלרגיות',
        'IsMobile': 'נייד',
        'EnergyLevel': 'רמת אנרגיה',
        'pastFosters': 'אומנויות קודמות',
        'pastExperience': 'ניסיון קודם',
        'documents': 'מסמכים',
    }

    # Define the menu options
    # with st.sidebar:
    #     selected = option_menu("בתים לבית אומנה", ["כל הטבלה", "מצא בית אומנה", "הוסף בית אומנה", "מסמכים"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)

    # # Use st.columns to create four equally sized columns
    # col1, col2, col3, col4 = st.columns(4)

    # # Button 1 in the first column
    # with col1:
    #     if st.button("כלבים 🐶"):
    #         st.switch_page("pages/Dogs.py")

    # # Button 2 in the second column
    # with col2:
    #     if st.button("בתי אומנה 🏠"):
    #         st.switch_page("pages/FosterHome.py")

    # # Button 3 in the third column
    # with col3:
    #     if st.button("אומצים 👤"):
    #         st.switch_page("pages/adopters.py")

    # # Button 4 in the fourth column
    # with col4:
    #     if st.button("בקשות 📁"):
    #         st.switch_page("pages/Applications.py")

    # Create the option menu inside a div with the custom class
    selected = option_menu(
        menu_title="",  # Required
        options=["ערוך מסמך","הוסף בית אומנה","מצא בית אומנה","כל הטבלה"],  # Required
        icons=["upload", "file", "search", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=3,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
    )

    # Translate column names
    foster_home_df_hebrew = foster_home_df.rename(columns=dict(
        zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))
    if st.button('רענן את העמוד'):
        st.cache_data.clear()
        st.success("המידע עודכן!")
    # Display different pages based on selected option
    if selected == "כל הטבלה":
        # data = fetch_data()  # Fetch the data from Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1lAY6gHYO-scPukLMTH8msFzwG9DoNsdq5-kNf2lKbqM/edit?usp=sharing")

        # Rename the columns using your Hebrew dictionary
        data.rename(columns=hebrew_columns_foster_homes, inplace=True)

        # Display the editable DataFrame
        edited_df = st.experimental_data_editor(data)

        # Add a save button to save the changes
        if st.button('שמור שינויים'):
            update_google_sheet(edited_df)
            st.success("השינויים נשמרו!")

    elif selected == "מצא בית אומנה":
        st.subheader('מצא בית אומנה')


        # Fetch the foster home data from Google Sheets
        # data = fetch_data()  # Fetch the data from Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        data = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1lAY6gHYO-scPukLMTH8msFzwG9DoNsdq5-kNf2lKbqM/edit?usp=sharing")   

    
        # Define Hebrew column names for foster homes (same as before)
        hebrew_columns_foster_homes = {
        'FosterHomeID': 'מזהה בית אומנה',
        'FosterName': 'שם בית אומנה',
        'Address': 'כתובת',
        'HouseSize': 'גודל הבית',
        'Contactinfomation': 'פרטי קשר',
        'Backyard': 'חצר',
        'nearDogPark': 'קרוב לגן כלבים',
        'HouseMembers': 'חברי בית',
        'AvailabilityAtHome': 'זמינות בבית',
        'ChildrenFriendly': 'ידידותי לילדים',
        'AnimalFriendly': 'ידידותי לכלבים',
        'MaximumCapacity': 'קיבולת מקסימלית',
        'allowedAtProperty': 'מותר בנכס',
        'allergies': 'אלרגיות',
        'IsMobile': 'נייד',
        'EnergyLevel': 'רמת אנרגיה',
        'pastFosters': 'אומנויות קודמות',
        'pastExperience': 'ניסיון קודם',
        'documents': 'מסמכים',
        }

        # Rename the columns using the Hebrew dictionary
        foster_home_df_hebrew = data.rename(columns=dict(
            zip(data.columns, [hebrew_columns_foster_homes.get(col, col) for col in data.columns])))

        # Create search filters for foster homes
        col1, col2, col3 = st.columns(3)

        with col1:
            foster_name = st.text_input('שם בית אומנה')
        with col2:
            house_size = st.selectbox('גודל הבית', [''] + list(foster_home_df_hebrew['גודל הבית'].unique()))
        with col3:
            children_friendly = st.selectbox('ידידותי לילדים', [''] + list(foster_home_df_hebrew['ידידותי לילדים'].unique()))

        # Apply search filters
        filtered_foster_homes = foster_home_df_hebrew[
            (foster_home_df_hebrew['שם בית אומנה'].str.contains(foster_name, na=False, case=False)) &
            (foster_home_df_hebrew['גודל הבית'].isin([house_size]) if house_size else True) &
            (foster_home_df_hebrew['ידידותי לילדים'].isin([children_friendly]) if children_friendly else True)
        ]

        st.dataframe(filtered_foster_homes)


    elif selected == "הוסף בית אומנה":
        st.subheader('הוסף בית אומנה חדש')

        # Input fields for the foster home form
        foster_home_id = st.text_input('מזהה בית אומנה')
        foster_name = st.text_input('שם בית אומנה')
        address = st.text_input('כתובת')
        house_size = st.number_input('גודל הבית (במ"ר)', min_value=0.0, max_value=1000.0, step=1.0)
        contact_information = st.text_input('פרטי קשר')
        backyard = st.checkbox('חצר')
        near_dog_park = st.checkbox('קרוב לגן כלבים')
        house_members = st.text_input('חברי בית')
        availability_at_home = st.selectbox('זמינות בבית', ['נמוכה', 'בינונית', 'גבוהה'])
        children_friendly = st.checkbox('ידידותי לילדים')
        animal_friendly = st.checkbox('ידידותי לחיות')
        maximum_capacity = st.number_input('קיבולת מקסימלית', min_value=0, max_value=20, step=1)
        allowed_at_property = st.checkbox('מותר בנכס')
        allergies = st.text_input('אלרגיות')
        is_mobile = st.checkbox('נייד')
        energy_level = st.selectbox('רמת אנרגיה', ['נמוכה', 'בינונית', 'גבוהה'])
        past_fosters = st.text_input('אומנויות קודמות')
        past_experience = st.text_area('ניסיון קודם')
        documents = st.file_uploader('העלה מסמכים', type=['pdf', 'docx'])

        # Save the new foster home data
        if st.button('שמור בית אומנה'):
            new_foster_home = {
            'FosterHomeID': foster_home_id,
            'FosterName': foster_name,
            'Address': address,
            'HouseSize': house_size,
            'Contactinfomation': contact_information,
            'Backyard': backyard,
            'nearDogPark': near_dog_park,
            'HouseMembers': house_members,
            'AvailabilityAtHome': availability_at_home,
            'ChildrenFriendly': children_friendly,
            'AnimalFriendly': animal_friendly,
            'MaximumCapacity': maximum_capacity,
            'allowedAtProperty': allowed_at_property,
            'allergies': allergies,
            'IsMobile': is_mobile,
            'EnergyLevel': energy_level,
            'pastFosters': past_fosters,
            'pastExperience': past_experience,
            'documents': documents.name if documents else '',
            }

            try:
                # Add the new foster home record to the Google Sheet
                add_foster_home_to_google_sheet(new_foster_home)
                st.success('בית אומנה חדש נשמר בהצלחה!')
                st.balloons()  # Show the balloons animation for success
            except Exception as e:
                st.error(f'Error saving foster home: {e}')
    elif selected == "ערוך מסמך":
        st.title('מסמכים')
        # Foster_df = fetch_data()  # Fetch the data from Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        Foster_df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1lAY6gHYO-scPukLMTH8msFzwG9DoNsdq5-kNf2lKbqM/edit?usp=sharing")


        foster_home_id = st.selectbox('Select Foster Home ID', Foster_df['מזהה בית אומנה'])

        if foster_home_id:
            st.subheader(f'מסמכים של {foster_home_id}')

            files = [f for f in os.listdir(FILES_DIR) if f.startswith(f'{foster_home_id}_')]
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

            uploaded_file = st.file_uploader('העלאת קובץ', type='pdf')
            if uploaded_file is not None:
                if uploaded_file.name:
                    save_file(foster_home_id, uploaded_file)
                else:
                    st.error('אין שם לקובץ ')

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

st.session_state["step"] = 0
show_foster_homes_page()
