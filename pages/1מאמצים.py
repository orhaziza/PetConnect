import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import background


# Directory for storing adopter files
FILES_DIR = 'Data/Adopters/'

# Ensure the directory exists
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
# Function to load adopters data
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

# Load the existing adopters data
adopter_df_hebrew = load_adopters_data()

        
def show_adopters_page():
    st.set_page_config(page_title='Adopters', layout='wide')
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
        
    background.insert_logo("מאמצים")

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

    # # Define the menu options
    # with st.sidebar:
    #     selected = option_menu("מאמצים", ["כל הטבלה", "מצא מאמץ", "הוסף מאמץ", "ערוך מסמך"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)


    selected = option_menu(
        menu_title="",  # Required
        options=["ערוך מסמך","הוסף מאמץ", "מצא מאמץ","כל הטבלה"],  # Required
        icons=["upload",  "file","search", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=3,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
        )

    # Translate column names
    adopter_df_hebrew = adopter_df.rename(
        columns=dict(zip(adopter_df.columns, [hebrew_columns_adopters.get(col, col) for col in adopter_df.columns])))
    dog_df_hebrew = pd.read_csv('Data/Dogs.csv')  # Replace with your actual data source

    # Merge adopter and dog data on a common key (like AdopterID or dog_chipID)
    # Load adopter and dog data
    dog_df_hebrew = pd.read_csv('Data/Dogs.csv')  # Replace with your actual data source

    # Verify the column names
    # st.write("Adopter columns:", adopter_df_hebrew.columns.tolist())
    # st.write("Dog columns:", dog_df_hebrew.columns.tolist())

    # Check if the necessary columns exist before merging
    if 'שבב כלב' in adopter_df_hebrew.columns and 'DogID' in dog_df_hebrew.columns:
        merged_df = pd.merge(adopter_df_hebrew, dog_df_hebrew, how='left', left_on='שבב כלב', right_on='DogID')
    else:
        st.error("The necessary columns for merging are missing.")
        st.stop()  
    if st.button('רענן את העמוד'):
        st.experimental_rerun()
    # Display different pages based on selected option
    if selected == "כל הטבלה":
        # Select only the adopter columns and the 'Name' column from the dogs table
        selected_columns = list(adopter_df_hebrew.columns) + ['Name']

        # Check if the 'Name' column exists after merging
        if 'Name' in merged_df.columns:
            merged_df = merged_df[selected_columns]

            # Move the 'Name' column to the second position
            cols = merged_df.columns.tolist()
            cols.insert(1, cols.pop(cols.index('Name')))  # Move 'Name' to the second position
            merged_df = merged_df[cols]
        else:
            st.warning("'Name' column not found in the merged table.")

        # Allow editing of the merged DataFrame
        edited_df = st.experimental_data_editor(merged_df)

        # Add a save button to save the changes
        if st.button('שמור שינויים'):
            try:
                # Extract the relevant changes for the adopter_df_hebrew
                edited_adopter_df = edited_df[adopter_df_hebrew.columns].copy()
                edited_dog_name_df = edited_df[['שבב כלב', 'Name']].copy()

                # Update the original adopter_df_hebrew DataFrame
                adopter_df_hebrew.update(edited_adopter_df)

                # If there are changes to the dog names, update the dog_df_hebrew
                if not edited_dog_name_df.empty:
                    for index, row in edited_dog_name_df.iterrows():
                        dog_chipID = row['שבב כלב']
                        dog_name = row['Name']
                        dog_df_hebrew.loc[dog_df_hebrew['DogID'] == dog_chipID, 'Name'] = dog_name

                # Save the updated DataFrames to their respective CSV files
                adopter_df_hebrew.to_csv(adopter_file_path, index=False, encoding='utf-8')
                dog_df_hebrew.to_csv('Data/Dogs.csv', index=False, encoding='utf-8')

                st.success('מידע עודכן בהצלחה!')
            except Exception as e:
                st.error(f'Error saving changes: {e}')

        # # Select only the adopter columns and the 'Name' column from the dogs table
        # selected_columns = list(adopter_df_hebrew.columns) + ['Name']
    
        # # Check if the 'Name' column exists after merging
        # if 'Name' in merged_df.columns:
        #     merged_df = merged_df[selected_columns]
        
        #     # Move the 'Name' column to the second position
        #     cols = merged_df.columns.tolist()
        #     cols.insert(1, cols.pop(cols.index('Name')))  # Move 'Name' to the second position
        #     merged_df = merged_df[cols]
        # else:
        #     st.warning("'Name' column not found in the merged table.")
    
        # st.dataframe(merged_df)
    elif selected == "מצא מאמץ":
        st.warning('תכניס לפחות קרטריון אחד')

        # Ensure columns are treated as strings
        merged_df['שבב כלב'] = merged_df['שבב כלב'].astype(str)
        merged_df['מזהה מאמץ'] = merged_df['מזהה מאמץ'].astype(str)
        merged_df['שם מאמץ'] = merged_df['שם מאמץ'].astype(str)
        merged_df['Name'] = merged_df['Name'].astype(str)  # Assuming 'Name' is the dog's name column

        # Rearrange columns to place 'Name' as the second column
        cols = merged_df.columns.tolist()
        if 'Name' in cols:
            cols.insert(1, cols.pop(cols.index('Name')))  # Move 'Name' to the second position
        merged_df = merged_df[cols]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            dog_chipID = st.text_input('מזהה שבב כלב')
        with col2:
            adopter_id = st.text_input('מזהה מאמץ')
        with col3:
            adopter_name = st.text_input('שם מאמץ')
        with col4:
            dog_name = st.text_input('שם כלב')  # New input for dog's name

        # Add a search button
        if st.button('Search'):
            # Initialize filter conditions
            conditions = pd.Series([True] * len(merged_df))  # Start with all True

            # Apply each filter if a criterion is provided
            if dog_chipID:
                conditions &= merged_df['שבב כלב'].str.contains(dog_chipID, na=False, case=False)

            if adopter_id:
                conditions &= merged_df['מזהה מאמץ'].str.contains(adopter_id, na=False, case=False)

            if adopter_name:
                conditions &= merged_df['שם מאמץ'].str.contains(adopter_name, na=False, case=False)

            if dog_name:
                 conditions &= merged_df['Name'].str.contains(dog_name, na=False, case=False)  # Filter by dog's name

             # Apply the combined conditions to filter the DataFrame
            filtered_adopters = merged_df[conditions]

            if not filtered_adopters.empty:
                # Display the filtered DataFrame and allow editing
                edited_df = st.experimental_data_editor(filtered_adopters)

                # Add a save button to save the changes
        if st.button('שמור שינויים'):
            try:
                # Extract the relevant changes for the adopter_df_hebrew
                edited_adopter_df = edited_df[adopter_df_hebrew.columns].copy()
                edited_dog_name_df = edited_df[['שבב כלב', 'Name']].copy()

                # Update the original adopter_df_hebrew DataFrame
                adopter_df_hebrew.update(edited_adopter_df)

                # If there are changes to the dog names, update the dog_df_hebrew
                if not edited_dog_name_df.empty:
                    for index, row in edited_dog_name_df.iterrows():
                        dog_chipID = row['שבב כלב']
                        dog_name = row['Name']
                        dog_df_hebrew.loc[dog_df_hebrew['DogID'] == dog_chipID, 'Name'] = dog_name

                # Save the updated DataFrames to their respective CSV files
                adopter_df_hebrew.to_csv(adopter_file_path, index=False, encoding='utf-8')
                dog_df_hebrew.to_csv('Data/Dogs.csv', index=False, encoding='utf-8')

                st.success('מידע עודכן בהצלחה!')
            except Exception as e:
                st.error(f'Error saving changes: {e}')
            else:
                st.warning('אין תוצאות למסננים שהיזנת!')
        # st.warning('תכניס לפחות קרטריון אחד')

        #  # Ensure columns are treated as strings
        # merged_df['שבב כלב'] = merged_df['שבב כלב'].astype(str)
        # merged_df['מזהה מאמץ'] = merged_df['מזהה מאמץ'].astype(str)
        # merged_df['שם מאמץ'] = merged_df['שם מאמץ'].astype(str)
        # merged_df['Name'] = merged_df['Name'].astype(str)  # Assuming 'Name' is the dog's name column

        # col1, col2, col3, col4 = st.columns(4)

        # with col1:
        #     dog_chipID = st.text_input('מזהה שבב כלב')
        # with col2:
        #     adopter_id = st.text_input('מזהה מאמץ')
        # with col3:
        #     adopter_name = st.text_input('שם מאמץ')
        # with col4:
        #     dog_name = st.text_input('שם כלב')  # New input for dog's name

        # # Add a search button
        # if st.button('Search'):
        #     # Initialize filter conditions
        #     conditions = pd.Series([True] * len(merged_df))  # Start with all True

        #     # Apply each filter if a criterion is provided
        #     if dog_chipID:
        #         conditions &= merged_df['שבב כלב'].str.contains(dog_chipID, na=False, case=False)

        #     if adopter_id:
        #         conditions &= merged_df['מזהה מאמץ'].str.contains(adopter_id, na=False, case=False)

        #     if adopter_name:
        #         conditions &= merged_df['שם מאמץ'].str.contains(adopter_name, na=False, case=False)

        #     if dog_name:
        #         conditions &= merged_df['Name'].str.contains(dog_name, na=False, case=False)  # Filter by dog's name

        #     # Apply the combined conditions to filter the DataFrame
        #     filtered_adopters = merged_df[conditions]

        #     if not filtered_adopters.empty:
        #         st.dataframe(filtered_adopters)
        #     else:
        #         st.warning('אין תוצאות למסננים שהיזנת!')
    elif selected == "הוסף מאמץ":
        st.subheader('הוסף מאמץ')

        # Add adoption form or input fields here
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
        # st.title('מסמכים')

        # # Select adopter
        # adopter_id = st.selectbox('Select Adopter ID', adopter_df_hebrew['מזהה מאמץ'])

        # if adopter_id:
        #     st.subheader(f'מסמכים של {adopter_id}')

        #     # List existing files
        #     files = [f for f in os.listdir(FILES_DIR) if f.startswith(f'{adopter_id}_')]
        #     if files:
        #         st.write('קבצים שיש במערכת ')
        #         for file_name in files:
        #             st.write(file_name)
        #             with open(os.path.join(FILES_DIR, file_name), "rb") as file:
        #                 btn = st.download_button(
        #                     label=f"הורד {file_name}",
        #                     data=file,
        #                     file_name=file_name,
        #                     mime='application/octet-stream'
        #                 )
        #             if st.button(f'מחק {file_name}', key=f'מחק_{file_name}'):
        #                 delete_file(file_name)

        #     # Upload new file
        #     uploaded_file = st.file_uploader('העלאת קובץ', type='pdf')
        #     if uploaded_file is not None:
        #         if uploaded_file.name:
        #             save_file(adopter_id, uploaded_file)
        #         else:
        #             st.error('אין שם לקובץ ')
        st.title('מסמכים')

        # Select adopter
        adopter_id = st.selectbox('Select Adopter ID', adopter_df_hebrew['מזהה מאמץ'])

        if adopter_id:
            st.subheader(f'מסמכים של {adopter_id}')
    
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


show_adopters_page()
