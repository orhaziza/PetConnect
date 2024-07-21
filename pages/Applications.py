import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection

def show_application_page():
    st.set_page_config(page_title='Applications', layout='wide')
    
    # the logo and title
    con1 = st.container()
    with con1:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.title("Applicant Profile")
        with col2:
            st.image("Data/Logo.png", width=120)
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?resourcekey=&gid=1409837987#gid=1409837987"
    conn = st.experimental_connection("gsheets", type=GSheetsConnection)
    data = conn.read(spreadsheet=url, usecols=[0, ])
    st.write("Start!!!")
    st.dataframe(data)
    st.write("Finish!!!")
    
    # Use st.columns to create four equally sized columns
    # Use st.columns to create four equally sized columns
    col1, col2, col3, col4 = st.columns(4)

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

    applications_file_path = 'Data/AdoptionApplication.csv'
    if not os.path.exists(applications_file_path):
        st.error("The applications file does not exist.")
        st.stop()

    applications_df = pd.read_csv(applications_file_path, encoding='utf-8')

    # Define Hebrew column names for adopters
    hebrew_columns_applications = {
        'ApplictionID': 'מזהה בקשה',
        'ApplicantName': 'שם מבקש',
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
        dogs_df = pd.read_csv('Data/Dogs.csv')
        status = st.selectbox(
        "Select Adoption Status",
        ["כל הטבלה", "לא מאומצים", "מאומצים"]
    )

# Filter DataFrame based on selected adoption status
        if status == "לא מאומצים":
            filtered_df = dogs_df[dogs_df['AdoptionStatus'] == 0]
        elif status == "מאומצים":
            filtered_df = dogs_df[dogs_df['AdoptionStatus'] == 1]
        else:
            filtered_df = dogs_df

        
        st.title('Dog-Adopter Matching System')
        st.markdown("<h2>Dog List</h2>", unsafe_allow_html=True)
        for i, dog in filtered_df.iterrows():
            cols = st.columns([1, 2, 2, 2, 1])
            cols[0].text(dog['DogID'])
            cols[1].text(dog['Name'])
            cols[2].text(dog['Breed'])
            cols[3].text(dog['Age'])
            if cols[4].button('Show Profile', key=f"select_{dog['DogID']}"):
                st.session_state['selected_dog_id'] =dog['DogID']
                selected_dog = dogs_df[dogs_df['DogID'] == dog['DogID']].iloc[0]
                scores = []
                for j, applicant in applications_df.iterrows():
                    score = score_adopter(selected_dog, applicant)
                    scores.append({'Application ID': applicant['ApplictionID'], 'Applicant Name': applicant['ApplicantName'], 'Score': score})
                scores_df = pd.DataFrame(scores)
                st.session_state['scores_df'] = scores_df
                st.switch_page("pages/DogsProfile.py")
        # Display the dog table and let the manager select a dog
        # st.dataframe(filtered_df)
      

        # st.header('Select a Dog')
        # selected_dog_id = st.selectbox('Choose a Dog ID', filtered_df['DogID'])

        # Get selected dog details
        # selected_dog = dogs_df[dogs_df['DogID'] == selected_dog_id].iloc[0]




        # if st.button('View Dog Profile'):
        #     # Navigate to the DogProfile page
        #     st.session_state['selected_dog_id'] = selected_dog_id


            
        #     # st.experimental_rerun()

        # Display selected dog information
        # st.subheader('Selected Dog Information')
        # st.write(selected_dog)



        # # Calculate and display scores for each adopter for the selected dog
        # st.subheader('Adopter Scores for Selected Dog')

        #     # Create a DataFrame with the scores
        # scores_df = pd.DataFrame(scores)

        #     # Display the scores DataFrame
        # #st.dataframe(scores_df)
   


        
        #scores_df = pd.DataFrame(scores)
        #st.dataframe(scores_df)


        
        




def score_adopter(dog, applicant):
    score = 0
    
    if dog['Size'] == 'L' and applicant['Large']:
        score += 10
    if dog['Size'] == 'S' and applicant['Meduim']:
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
