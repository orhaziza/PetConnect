# Pages/Adopters.py
import streamlit as st
import pandas as pd
import os

def show_adopters_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Cannot access the page without logging in.")
        st.stop()

    st.title("Manage Adopters")

    # Load adopters data
    adopters_file_path = "Data/Adopters.csv"
    if not os.path.exists(adopters_file_path):
        st.error("The adopters data file does not exist.")
        return

    adopters_df = pd.read_csv(adopters_file_path, encoding='Windows-1255')

    # Hebrew column translations for adopters
    hebrew_columns_adopters = {
        'AdopterID': 'מזהה מאמץ',
        'Name': 'שם',
        'ContactInformation': 'פרטי קשר',
        'Address': 'כתובת',
        'Age': 'גיל',
        'Gender': 'מין',
        'AdoptionDate': 'תאריך אימוץ',
        'PreferredBreed': 'זן מועדף',
        'HasChildren': 'יש ילדים',
        'HasOtherPets': 'יש חיות מחמד אחרות',
        'HomeType': 'סוג בית',
        'Yard': 'חצר',
        'AdoptedDogs': 'כלבים מאומצים',
    }

    # Translate English column names to Hebrew
    hebrew_column_names = [hebrew_columns_adopters.get(col, col) for col in adopters_df.columns]
    adopters_df_hebrew = adopters_df.rename(columns=dict(zip(adopters_df.columns, hebrew_column_names)))

    # Define the menu options
    with st.sidebar:
        selected = st.selectbox("Select an option", ["All Adopters", "Find an Adopter", "Add an Adopter", "Edit Adopter"])

    # Display based on menu selection
    if selected == "All Adopters":
        st.dataframe(adopters_df_hebrew)
        if st.button("Save Changes"):
            # Rename columns back to English for saving
            adopters_df.rename(columns={v: k for k, v in hebrew_columns_adopters.items()}, inplace=True)
            adopters_df.to_csv(adopters_file_path, index=False, encoding='Windows-1255')
            st.success("Changes saved successfully!")

    elif selected == "Find an Adopter":
        st.subheader('Find an Adopter')
        # Add search logic
        name = st.text_input('Name')
        preferred_breed = st.selectbox('Preferred Breed', options=[''] + list(adopters_df['PreferredBreed'].unique()))
        has_children = st.selectbox('Has Children', options=['', 'Yes', 'No'])
        has_other_pets = st.selectbox('Has Other Pets', options=['', 'Yes', 'No'])

        # Apply search filters
        filtered_df = adopters_df_hebrew[
            (adopters_df['Name'].str.contains(name, na=False, case=False)) &
            (adopters_df['PreferredBreed'].isin([preferred_breed]) if preferred_breed else True) &
            (adopters_df['HasChildren'].isin([has_children]) if has_children else True) &
            (adopters_df['HasOtherPets'].isin([has_other_pets]) if has_other_pets else True)
        ]
        st.write(filtered_df)

    elif selected == "Add an Adopter":
        st.subheader('Add a New Adopter')
        with st.form(key='adopter_form'):
            adopter_id = st.text_input('Adopter ID')
            name = st.text_input('Name')
            contact_info = st.text_input('Contact Information')
            address = st.text_area('Address')
            age = st.number_input('Age', min_value=0, max_value=120, step=1)
            gender = st.selectbox('Gender', ['Male', 'Female'])
            adoption_date = st.date_input('Adoption Date')
            preferred_breed = st.text_input('Preferred Breed')
            has_children = st.selectbox('Has Children', ['Yes', 'No'])
            has_other_pets = st.selectbox('Has Other Pets', ['Yes', 'No'])
            home_type = st.selectbox('Home Type', ['Apartment', 'House', 'Other'])
            yard = st.selectbox('Yard', ['Yes', 'No'])
            adopted_dogs = st.text_area('Adopted Dogs')

            submit_button = st.form_submit_button(label='Save Adopter')

        if submit_button:
            new_adopter = {
                'AdopterID': adopter_id,
                'Name': name,
                'ContactInformation': contact_info,
                'Address': address,
                'Age': age,
                'Gender': gender,
                'AdoptionDate': adoption_date.strftime('%Y-%m-%d'),
                'PreferredBreed': preferred_breed,
                'HasChildren': has_children,
                'HasOtherPets': has_other_pets,
                'HomeType': home_type,
                'Yard': yard,
                'AdoptedDogs': adopted_dogs,
            }
            adopters_df = adopters_df.append(new_adopter, ignore_index=True)
            adopters_df.to_csv(adopters_file_path, index=False, encoding='Windows-1255')
            st.success('The adopter has been added successfully!')

    elif selected == "Edit Adopter":
        st.subheader('Edit Adopter')
        # Add logic to edit adopter information
