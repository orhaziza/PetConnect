# import streamlit as st
# import pandas as pd
# import os
# from datetime import datetime
# from streamlit_option_menu import option_menu
# import background
# import numpy as np

# # Function to display a flash animation
# def show_flash_animation():
#     # HTML and CSS for the flash animation
#     flash_animation_html = """
#     <style>
#     .flash {
#         position: absolute;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background: rgba(255, 255, 255, 0.8);
#         animation: flash-animation 0.5s ease-out;
#         z-index: 9999;
#     }

#     @keyframes flash-animation {
#         0% { background: rgba(255, 255, 255, 0.8); }
#         50% { background: rgba(255, 255, 255, 0.1); }
#         100% { background: rgba(255, 255, 255, 0.8); }
#     }
#     </style>
#     <div class="flash"></div>
#     <script>
#     setTimeout(function() {
#         document.querySelector('.flash').remove();
#     }, 500);
#     </script>
#     """
#     # Display the flash animation
#     st.markdown(flash_animation_html, unsafe_allow_html=True)
# # Directory for storing adopter files

# FILES_DIR = 'Data/Adopters/'
# url = "https://docs.google.com/spreadsheets/d/1g1WWygeD3ZE_uDGQRd2EL44NUHioLHVacsX_7Z8uu5Q/edit?usp=sharing"

# SCOPES = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]



# def get_gspread_client():
#     creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = SCOPES)
#     client = gspread.authorize(creds)
#     return client

# def open_google_sheet():
#     client = get_gspread_client()
#     sheet = client.open_by_key("1g1WWygeD3ZE_uDGQRd2EL44NUHioLHVacsX_7Z8uu5Q")
#     worksheet = sheet.worksheet("גיליון1")  # Name of the sheet
#     return worksheet

# @st.cache_data()
# def fetch_data():
#     conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
#     return conn.read(spreadsheet=url)
    
# if not os.path.exists(FILES_DIR):
#     os.makedirs(FILES_DIR)

# def calculate_age_in_months(birth_date):
#     today = datetime.today()
#     age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
#     return age_in_months
    
# def show_dogs_page():
#     st.set_page_config(page_title='Dogs', layout='wide')

#     background.add_bg_from_local('./static/background3.png')
#     background.load_css('styles.css')

#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("לא ניתן לגשת לעמוד ללא התחברות")
#         st.stop()

#     background.insert_logo("כלבים")

#     url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"
    

#     # Creating Dataframe from csv
#     dogs_file_path = "Data/Dogs.csv"
#     dog_df = pd.read_csv(dogs_file_path, encoding='utf-8')


#     foster_home_file_path = "Data/FosterHome.csv"
#     if not os.path.exists(foster_home_file_path):
#         st.error("The foster home file does not exist.")
#         st.stop()

#     foster_home_df = pd.read_csv(foster_home_file_path, encoding='utf-8')

#     # Load the foster home data
#     foster_home_file_path = "Data/FosterHome.csv"
#     if not os.path.exists(foster_home_file_path):
#         st.error("The foster home file does not exist.")
#         st.stop()

#     foster_home_df = pd.read_csv(foster_home_file_path, encoding='utf-8')

#     # Defining Hebrew names
#     # Define Hebrew column names
#     hebrew_columns_dogs = {
#     'DogID': 'מזהה כלב',
#     'Name': 'שם',
#     'DateOfBirth': 'תאריך לידה',
#     'Age': 'גיל',
#     'Breed': 'זן',
#     'Weight': 'משקל',
#     'Size': 'גודל',
#     'Gender': 'מין',
#     'RescueDate': 'תאריך חילוץ',
#     'Rabies_Done': 'חיסון כלבת',
#     'Hexagonal_1': 'חיסון משושה 1',
#     'Hexagonal_2': 'חיסון משושה 2',
#     'Hexagonal_3': 'חיסון משושה 3',
#     'Hexagonal_Done': 'חיסון משושה',
#     'Spayed': 'מעוקר',
#     'De-worm': 'טיפול נגד תולעים',
#     'Children_Friendly': 'ידידותי לילדים',
#     'AnimalFriendly': 'ידידותי לכלבים',
#     'HealthStatus': 'מצב הכלב',
#     'EnergyLevel': 'רמת האנרגיה',
#     'PhotographStatus': 'סטטוס הצילום',
#     'AdoptionStatus': 'סטטוס אימוץ',
#     'AdopterID': 'מזהה מאמץ',
#     'PottyTrained': 'מחונך לצרכים',
#     'AdoptionName': 'שם המאומץ'
#     # Add more column name translations as needed
# }

#     hebrew_columns_foster_homes = {
#         'FosterHomeID': 'מזהה בית אומנה',
#         'FosterName': 'שם בית אומנה',
#         'Address': 'כתובת',
#         'HouseSize': 'גודל הבית',
#         'Contactinfomation': 'פרטי קשר',
#         'Backyard': 'חצר',
#         'nearDogPark': 'קרוב לגן כלבים',
#         'HouseMembers': 'חברי בית',
#         'AvailabilityAtHome': 'זמינות בבית',
#         'ChildrenFriendly': 'ידידותי לילדים',
#         'AnimalFriendly': 'ידידותי לכלבים',
#         'MaximumCapacity': 'קיבולת מקסימלית',
#         'allowedAtProperty': 'מורשה ברחם',
#         'allergies': 'אלרגיות',
#         'IsMobile': 'ניידות',
#         'EnergyLevel': 'רמת אנרגיה',
#         'pastFosters': 'כולל אמנה קודמת',
#         'pastExperience': 'ניסיון קודם',
#         'documents': 'מסמכים',
#     }

#     foster_home_df_hebrew = foster_home_df.rename(columns=dict(
#         zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))

    
#     selected = option_menu(
#         menu_title="",  
#         options=["הוסף כלב","מצא כלב","כל הטבלה"] , # Required
#         icons=["upload", "search", "file"],  # Optional
#         menu_icon="menu",
#         default_index = 2, # Optional
#         orientation="horizontal",  # To place the menu in the center horizontally
#         styles=background.styles,
#     )

#     images_folder = "DogsPhotos"
#     # Translate English column names to Hebrew
#     hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]

#     # Display DataFrame with Hebrew column names
#     file_path = "Data/Dogs.csv"

#     # Check if the file exists
#     if not os.path.exists(file_path):
#         st.error("The file does not exist.")
#         st.stop()

#         # Read CSV file
#     dog_df = pd.read_csv(file_path, encoding='utf-8')
#     hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
#     dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

#     # Display the editable table

#     # Button to save changes

#     if selected == "כל הטבלה":
#         edited_df = st.data_editor(dog_df_hebrew, use_container_width=True, height=400)
#         if st.button("שמור שינויים"):
#             # Rename columns back to English for saving
#             edited_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
#             # Save the edited dataframe to the CSV file
#             edited_df.to_csv(file_path, index=False, encoding='utf-8')
#             st.success("השינויים נשמרו בהצלחה!")

#     if selected == "מצא כלב":
#         # st.subheader('<div style="direction: rtl;">מצא כלב</div>', unsafe_allow_html=True)
#         # Create search filters in columns
#         col1, col2, col3, col4 = st.columns(4)

#         with col1:
#         # Filter out NaN values from Breed options
#             breed_options = dog_df["Breed"].dropna().unique()
#             breed = st.selectbox('זן', options=[''] + list(breed_options))

#         with col2:
#         # Handle the age filter (assuming no NaN values for Age)
#             age = st.slider('גיל', min_value=0, max_value=int(dog_df['Age'].max()), value=(0, int(dog_df['Age'].max())))

#         with col3:
#         # Filter out NaN values from Size options
#             size_options = dog_df["Size"].dropna().unique()
#             size = st.selectbox('גודל', options=[''] + list(size_options))

#         with col4:
#         # Filter out NaN values from Gender options
#             gender_options = dog_df["Gender"].dropna().unique()
#             gender = st.selectbox('מין', options=[''] + list(gender_options))

#         # Apply search filters
#         filtered_df = dog_df_hebrew[
#             (dog_df['Breed'].isin([breed]) if breed else True) &
#             (dog_df['Age'] >= age[0]) & (dog_df['Age'] <= age[1]) &
#             (dog_df['Size'].isin([size]) if size else True) &
#             (dog_df['Gender'].isin([gender]) if gender else True)
#             ]

#         st.write(filtered_df)

#     if selected == "הוסף כלב":
#         st.subheader('הוסף כלב חדש')

#         with st.form(key='insert_form'):
#             DogID = st.text_input('מזהה כלב')
#             name = st.text_input('שם')
#             date_of_birth = st.date_input('תאריך לידה')
#             breed = st.text_input('זן')
#             weight = st.number_input('משקל', min_value=0.0, max_value=100.0, step=0.1)
#             size = st.selectbox('גודל', ['קטן', 'בינוני', 'גדול'])
#             gender = st.selectbox('מין', ['זכר', 'נקבה'])
#             rescueDate = st.date_input('תאריך חילוץ')
#             rabies_date = st.date_input('תאריך חיסון כלבת', value = None)
#             hexagonal_1_date = st.date_input('תאריך חיסון משושה 1', value = None)
#             hexagonal_2_date = st.date_input('תאריך חיסון משושה 2', value = None)
#             hexagonal_3_date = st.date_input('תאריך חיסון משושה 3', value = None)
#             de_worm_date = st.date_input('תאריך טיפול נגד תולעים', value = None)
#             spayed = st.checkbox('מעוקר')
#             children_friendly = st.checkbox('ידידותי לילדים')
#             animal_friendly = st.checkbox('ידידותי לכלבים')
#             health_status = st.text_input('מצב הכלב')
#             energy_level = st.selectbox('רמת האנרגיה', ['נמוכה', 'בינונית', 'גבוהה'])
#             photograph_status = st.selectbox('סטטוס הצילום', ['ממתין לצילום', 'צילום הושלם'])
#             adoption_status = st.selectbox('סטטוס אימוץ', ['זמין לאימוץ', 'נאסף'])
#             adopterID = st.text_input('מזהה מאמץ')
#             potty_trained = st.checkbox('מחונך לצרכים')

#             submit_button = st.form_submit_button(label='הוסף כלב')

#         if submit_button:
#             age = calculate_age_in_months(date_of_birth) if date_of_birth else 0
#             new_dog = {
#             'DogID': DogID,
#             'Name': name,
#             'DateOfBirth': date_of_birth.strftime('%Y-%m-%d'),
#             'Age': age,
#             'Breed': breed,
#             'Weight': weight,
#             'Size': size,
#             'Gender': gender,
#             'RescueDate': rescueDate.strftime('%Y-%m-%d'),
#             'Rabies_Done': rabies_date.strftime('%Y-%m-%d') if rabies_date else np.nan,
#             'Hexagonal_1': hexagonal_1_date.strftime('%Y-%m-%d') if hexagonal_1_date else np.nan,
#             'Hexagonal_2': hexagonal_2_date.strftime('%Y-%m-%d') if hexagonal_2_date else np.nan,
#             'Hexagonal_3': hexagonal_3_date.strftime('%Y-%m-%d') if hexagonal_3_date else np.nan,
#             'De-worm': de_worm_date.strftime('%Y-%m-%d') if de_worm_date else np.nan,
#             'Spayed': spayed,
#             'Children_Friendly': children_friendly,
#             'AnimalFriendly': animal_friendly,
#             'HealthStatus': health_status,
#             'EnergyLevel': energy_level,
#             'PhotographStatus': photograph_status,
#             'AdoptionStatus': adoption_status,
#             'AdopterID': adopterID,
#             'PottyTrained': potty_trained,
#         }
#             dog_df = dog_df.append(new_dog, ignore_index=True)
#             dog_df.to_csv(file_path, index=False, encoding='utf-8')
#             st.success('הכלב הוסף בהצלחה!')

#     # Sidebar logout button
#     if st.sidebar.button("Log Out"):
#         st.session_state['logged_in'] = False
#         st.experimental_rerun()


# # Call the function to display the dogs page
# show_dogs_page()


import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import numpy as np

# Directory for storing adopter files
FILES_DIR = 'Data/Adopters/'
url = "https://docs.google.com/spreadsheets/d/16HGmdzrp3IZ5vz5KRwM8MVMRZuxdQS9KC3uuZVq_OCA/edit?usp=sharing"

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
    sheet = client.open_by_key("16HGmdzrp3IZ5vz5KRwM8MVMRZuxdQS9KC3uuZVq_OCA")
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

# Calculate age in months
def calculate_age_in_months(birth_date):
    today = datetime.today()
    age_in_months = (today.year - birth_date.year) * 12 + today.month - birth_date.month
    return age_in_months

def show_dogs_page():
    st.set_page_config(page_title='Dogs', layout='wide')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    # Fetch dog data from Google Sheets
    dog_df = fetch_data_from_google_sheet()

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
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
    dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

    # Add your option_menu logic and other dog page features here

    selected = st.selectbox("בחר פעולה", options=["הוסף כלב", "מצא כלב", "כל הטבלה"])

    if selected == "כל הטבלה":
        data = fetch_data()  # Fetch the data from Google Sheets

        # Rename the columns using your Hebrew dictionary
        data.rename(columns=hebrew_columns_dogs, inplace=True)

        # Display the editable DataFrame
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
