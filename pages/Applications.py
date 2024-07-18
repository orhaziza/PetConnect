import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

def show_application_page():
    st.set_page_config(page_title='Applications', layout='wide')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()


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
        if st.button("אומצים 👤"):
            st.switch_page("pages/adopters.py")

    # Button 4 in the fourth column
    with col4:
        if st.button("בקשות 📁"):
            st.switch_page("pages/Applications.py")


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
        menu_title="בקשות",  # Required
        options=["כל הטבלה", "טבלה עם ציון"],  # Added new option for the table with scores
        icons=["file", "search", "file", "upload", "table"],  # Optional
        menu_icon="menu",  # Optional
        default_index=0,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles={
            "container": {"class": "option-menu-container"}
        }
    )

    applications_file_path = "Data/AdoptionApplication.csv"
    if not os.path.exists(applications_file_path):
        st.error("The applications file does not exist.")
        st.stop()

    applications_df = pd.read_csv(applications_file_path, encoding='Windows-1255')

    # Define Hebrew column names for adopters
    hebrew_columns_applications = {
        'ApplictionID': 'מזהה בקשה',
        'dogID': 'מזהה כלב',
        'AdopterID': 'מזהה מאמץ',
        'applicationDate': 'תאריך בקשה',
        'status': 'סטטוס בקשה',
        'messageContect': 'תוכן בקשה',
        'SourcePlatform': 'מאיפה הגעת אלינו',
    }

    # adopter_df_hebrew = adopter_df.rename(columns=dict(zip(adopter_df.columns, [hebrew_columns_adopters.get(col, col) for col in adopter_df.columns])))
    applic_df_hebrew = applications_df.rename(columns=dict(
        zip(applications_df.columns, [hebrew_columns_applications.get(col, col) for col in applications_df.columns])))

    if selected == "כל הטבלה":
        st.dataframe(applic_df_hebrew)
    if selected == "טבלה עם ציון":
        
        dog = {
    'DogID': 1,
    'Name': 'Buddy',
    'DateOfBirth': '2020-01-01',
    'Age': 3,
    'Breed': 'Labrador',
    'Weight': 30,
    'Size': 'L',
    'Gender': 'זכר',
    'RescueDate': '2021-01-01',
    'Rabies_Done': True,
    'Hexagonal_1': True,
    'Hexagonal_2': True,
    'Hexagonal_3': False,
    'Hexagonal_Done': True,
    'Spayed': True,
    'De-worm': True,
    'Children_Friendly': True,
    'AnimalFriendly': True,
    'HealthStatus': 'טוב',
    'EnergyLevel': 2,
    'PhotographStatus': 'Yes',
    'AdoptionStatus': 'Available',
    'AdopterID': None,
    'PottyTrained': True,
    'AdoptionName': 'Buddy'
        }

        
        scores = []
        for j, applicant in applications_df.iterrows():
            score = score_adopter(dog, applicant)
            scores.append({'DogID': dog['DogID'], 'AdopterID': applicant['AdopterID'], 'Score': score})

        scores_df = pd.DataFrame(scores)
        st.dataframe(scores_df)


        
        




def score_adopter(dog, applicant):
    score = 0
    
    if dog['Size'] == 'L' and applicant['Large']:
        score += 10
    if dog['Size'] == 'S' and aplicant['Medium']:
        score += 10
    if dog['Size'] == 'Small' and applicant['Small']:
        score += 10
    
    if dog['EnergyLevel'] <=1 and applicant["Calm"] == 1:
        score += 20
    if dog['EnergyLevel'] >1 and applicant["Active"]:
        score +=20
    

    if dog['AnimalFriendly'] and applicant['Animal Friendly']:
        score += 15

    #if dog["HealthStatus"] == 'טוב' and applicant['Healthy']:
        #score +=10

    #if dog["HealthStatus"] == 'חייב יחס' and applicant['Needs Attention']:
        #score +=10
    
    #if dog['Children_Friendly'] and applicant['Children_Friendly']:
        #score += 15
            
    #if dog['Spayed'] == "TRUE" and applicant['Spayed']:
        #score += 5

    return score
    


show_application_page()
