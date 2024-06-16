# Pages/Dogs.py
import streamlit as st
import pandas as pd
import os

def show_dogs_page():
    st.title("Manage Dogs")

    # Path to the CSV files
    dogs_file_path = "Data/Dogs.csv"
    foster_home_file_path = "Data/FosterHome.csv"
    images_folder = "DogsPhotos"

    # Load data
    if not os.path.exists(dogs_file_path):
        st.error("The dogs data file does not exist.")
        return

    dog_df = pd.read_csv(dogs_file_path, encoding='Windows-1255')

    # Hebrew column translations
    hebrew_columns_dogs = {
        'DogID': 'מזהה כלב',
        'name': 'שם',
        'age': 'גיל',
        'breed': 'זן',
        'size': 'גודל',
        'gender': 'מין',
        'rescueDate': 'תאריך חילוץ',
        'vaccine_1': 'חיסון כלבת',
        'vaccine_2': 'חיסון משושה',
        'isSpay': 'מעוקר',
        'childrenFirendly': 'ידידותי לילדים',
        'healthStatus': 'מצב הכלב',
        'energylevel': 'רמת האנרגיה',
        'photographStatus': 'סטטוס הצילום',
        'adoptionStatus': 'סטטוס אימוץ',
        'adopterID': 'מזהה מאמץ',
        'pottyTrained': 'מחונך לצרכים',
        'animalFirendly': 'ידידותי לכלבים',
    }

    # Translate English column names to Hebrew
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
    dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

    # Define the menu options
    with st.sidebar:
        selected = st.selectbox("Select an option", ["All Dogs", "Find a Dog", "Add a Dog", "Edit Image"])

    # Display based on menu selection
    if selected == "All Dogs":
        st.dataframe(dog_df_hebrew)
        if st.button("Save Changes"):
            # Rename columns back to English for saving
            dog_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
            dog_df.to_csv(dogs_file_path, index=False, encoding='Windows-1255')
            st.success("Changes saved successfully!")

    elif selected == "Find a Dog":
        st.subheader('Find a Dog')
        # Add search logic

    elif selected == "Add a Dog":
        st.subheader('Add a New Dog')
        # Add form to add a new dog

    elif selected == "Edit Image":
        st.subheader('Edit Dog Image')
        # Add logic to edit images

