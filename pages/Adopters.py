import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

# Set up the page configuration at the top
st.set_page_config(page_title='Adopters', layout='wide')

# Function to load adopters data
def load_adopters_data():
    adopter_file_path = 'Data/Adopters.csv'
    adopters_df = pd.read_csv(adopter_file_path, encoding='utf-8')
    return adopters_df

# Function to save a file
def save_file(adopter_id, file):
    try:
        file_name = f'{adopter_id}_{file.name}'
        file_path = os.path.join(FILES_DIR, file_name)

        # Write the file
        with open(file_path, 'wb') as f:
            f.write(file.read())

        st.success('File saved successfully')
    except Exception as e:
        st.error(f'Error saving file: {e}')
        raise

# Function to delete a file
def delete_file(file_name):
    file_path = os.path.join(FILES_DIR, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

def show_adopters_page():
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
    }

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #E8E8E8; /* Light grey background */
        }
        .header {
            text-align: center;
            font-size: 2.5em;
            margin-top: 20px;
            color: #222831; /* Dark color for headers */
        }
        .subheader {
            text-align: center;
            font-size: 1.5em;
            color: #222831; /* Dark color for subheaders */
        }
        .login-container {
            max-width: 500px;
            margin: auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #ffffff; /* White background for the login container */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .record {
            text-align: right;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-bottom: 10px;
            background-color: #ffffff; /* White background for records */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .refresh-btn {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        .stButton > button {
            color: #ffffff; /* White text for buttons */
            background-color: #30475E; /* Dark blue color for buttons */
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.3s;
        }
        .stButton > button:hover {
            background-color: #25394C; /* Darker blue on hover */
            transform: scale(1.05);
        }
        .stButton > button.logout {
            background-color: #F05454; /* Red color for logout button */
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.3s;
        }
        .stButton > button.logout:hover {
            background-color: #C74444; /* Darker red on hover */
            transform: scale(1.05);
        }
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin: 20px 0;
        }
        .dataframe {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 1.1em;
            min-width: 400px;
            border-radius: 5px 5px 0 0;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
        }
        .dataframe thead tr {
            background-color: #30475E;
            color: #ffffff;
            text-align: left;
            font-weight: bold;
            position: sticky;
            top: 0;
        }
        .dataframe th, .dataframe td {
            padding: 12px 15px;
        }
        .dataframe tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .dataframe tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .dataframe tbody tr:hover {
            background-color: #f1f1f1;
        }
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
        st.dataframe(adopter_df_hebrew, height=600)

    elif selected == "מצא מאמץ":
        st.warning('תכניס לפחות קרטריון אחד')

        # Ensure columns are treated as strings
        adopter_df_hebrew['שבב כלב'] = adopter_df_hebrew['שבב כלב'].astype(str)
        adopter_df_hebrew['מזהה מאמץ'] = adopter_df_hebrew['מזהה מאמץ'].astype(str)
        adopter_df_hebrew['שם מאמץ'] = adopter_df_hebrew['שם מאמץ'].astype(str)
        col1, col2, col3 = st.columns(3)

        with col1:
            dog_chipID = st.text_input('מזהה שבב כלב')
        with col2:
            adopter_id = st.text_input('מזהה מאמץ')
        with col3:
            adopter_name = st.text_input('שם מאמץ')

        # Initialize filter conditions
        conditions = pd.Series([True] * len(adopter_df_hebrew))  # Start with all True

        # Apply each filter if a criterion is provided
        if dog_chipID:
            conditions &= adopter_df_hebrew['שבב כלב'].str.contains(dog_chipID, na=False, case=False)
        
        if adopter_id:
            conditions &= adopter_df_hebrew['מזהה מאמץ'].str.contains(adopter_id, na=False, case=False)
    
        if adopter_name:
            conditions &= adopter_df_hebrew['שם מאמץ'].str.contains(adopter_name, na=False, case=False)

        # Apply the combined conditions to filter the DataFrame
        filtered_adopters = adopter_df_hebrew[conditions]

        if not filtered_adopters.empty:
            st.dataframe(filtered_adopters)
        else:
            st.warning('אין תוצאות למסננים שהיזנת!')
    elif selected == "הוסף מאמץ":
        st.subheader('הוסף מאמץ')

        # Add adoption form or input fields here
        st.markdown("<div class='card'>", unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button('שמור מאמץ'):
            # Save adopter data to CSV or database
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
        # Directory for storing adopter files
        FILES_DIR = 'Data/Adopters/'

        # Ensure the directory exists
        if not os.path.exists(FILES_DIR):
            os.makedirs(FILES_DIR)
        
        # Load the existing adopters data
        adopter_df_hebrew = load_adopters_data()

        # Show the page
        st.title('Adopter Files Management')

        # Select adopter
        adopter_id = st.selectbox('Select Adopter ID', adopter_df_hebrew['AdopterID'])

        if adopter_id:
            st.subheader(f'Files for Adopter {adopter_id}')

            # List existing files
            files = [f for f in os.listdir(FILES_DIR) if f.startswith(f'{adopter_id}_')]
            if files:
                st.write('Existing files:')
                for file_name in files:
                    st.write(file_name)
                    with open(os.path.join(FILES_DIR, file_name), "rb") as file:
                        btn = st.download_button(
                            label=f"Download {file_name}",
                            data=file,
                            file_name=file_name,
                            mime='application/octet-stream'
                        )
            if st.button(f'Delete {file_name}'):
                delete_file(file_name)
                st.experimental_rerun()
            # Upload new file
            uploaded_file = st.file_uploader('Upload a PDF file', type='pdf')
            if uploaded_file is not None:
                if uploaded_file.name:
                    save_file(adopter_id, uploaded_file)
                    st.success('File uploaded successfully.')
                else:
                    st.error('Uploaded file does not have a name.')

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

show_adopters_page()