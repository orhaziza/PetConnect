import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Applications', layout='wide')
    
def show_application_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"
        # Custom CSS to center-align the option menu
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap');
        
        /* Apply Rubik font globally and enforce RTL layout */
        * {
            font-family: 'Rubik', sans-serif !important;
            direction: rtl !important;
        }

        /* Specific adjustments for DataFrame content */
        .stDataFrame div, .stTable div, .dataframe th, .dataframe td {
            font-family: 'Rubik', sans-serif !important;
            direction: rtl !important;
        }

        /* Specific adjustments for option_menu */
        .nav-link, .nav-link span {
            font-family: 'Rubik', sans-serif !important;
            direction: rtl !important;
        }
        .option-menu-container {
        font-family: 'Roboto', sans-serif;
        }
        .stButton > button {
        color: #ffffff; /* White text for buttons */
        background-color: #30475E; /* Dark blue color for buttons */
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-size: 1em;
        }
        .stButton > button:hover {
            background-color: #25394C; /* Darker blue on hover */
            transform: scale(1.05);
        }
        .stButton > button.logout {
            background-color: #F05454; /* Red color for logout button */
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.3s;
            padding: 10px 20px;
            font-size: 1em;
        }
        .stButton > button.logout:hover {
            background-color: #C74444; /* Darker red on hover */
            transform: scale(1.05);
        }
        .icon-button {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .icon-button img {
            margin-right: 5px;
        }
        .option-menu-container {
            display: flex;
            justify-content: center;
        }
        .dataframe-container {
            background-color: #ffffff; /* White background for dataframe */
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 10px;
        }
        .file-upload-container {
            background-color: #ffffff; /* White background for file upload */
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-top: 20px;
        }
        .stDownloadButton > button {
            color: #ffffff; /* White text for download buttons */
            background-color: #30475E; /* Dark blue color for download buttons */
            border-radius: 5px;
            padding: 10px 20px;
            transition: background-color 0.3s, transform 0.3s;
            font-size: 1em;
        }
        .stDownloadButton > button:hover {
            background-color: #25394C; /* Darker blue on hover */
            transform: scale(1.05);
        }
        </style>

            """,
            unsafe_allow_html=True
        )
    

    # the logo and title
    with st.container():
        col4, col1, col2 = st.columns([1, 10, 1])
        with col1:
            st.markdown("<h1 style='text-align: center;'>בקשות אימוץ</h1>", unsafe_allow_html=True)
        with col2:
            st.image("Data/Logo.png", width=100)


    # Define the menu options
    selected = option_menu(
        menu_title="",  # Required
        options=["בקשות עם ציון", "כל הבקשות"],  # Added new option for the table with scores
        icons=["search", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=1,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
    )

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"

    @st.cache_data()
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        return conn.read(spreadsheet=url)

    col1, col2, col3= st.columns([1.5, 1, 1])

    with col2:
        if st.button("רענן"):
            st.cache_data.clear()
            st.success("המידע עודכן!")
    
    data = fetch_data()

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()
    
    # applications_file_path = 'Data/AdoptionApplication.csv'
    # if not os.path.exists(applications_file_path):
    #     st.error("The applications file does not exist.")
    #     st.stop()

    # applications_df = pd.read_csv(applications_file_path, encoding='utf-8')

    # Define Hebrew column names for adopters
    # hebrew_columns_applications = {
    #     'ApplictionID': 'מזהה בקשה',
    #     'ApplicantName': 'שם מבקש',
    #     'dogID': 'מזהה כלב',
    #     'AdopterID': 'מזהה מאמץ',
    #     'applicationDate': 'תאריך בקשה',
    #     'status': 'סטטוס בקשה',
    #     'messageContect': 'תוכן בקשה',
    #     'SourcePlatform': 'מאיפה הגעת אלינו',
    # }

    # # adopter_df_hebrew = adopter_df.rename(columns=dict(zip(adopter_df.columns, [hebrew_columns_adopters.get(col, col) for col in adopter_df.columns])))
    # applic_df_hebrew = applications_df.rename(columns=dict(
    #     zip(applications_df.columns, [hebrew_columns_applications.get(col, col) for col in applications_df.columns])))

    if selected == "כל הבקשות":
        # Filters
        with st.expander("סינון:"):
            col1, col2 = st.columns(2)
            with col1:
                filter_date = st.date_input("תאריך:", value=None)
            with col2:
                filter_name = st.text_input("שם:")

        # Apply filters only if inputs are provided
        if filter_date is not None:
            data = data[data['חותמת זמן'].str.contains(filter_date.strftime('%Y-%m-%d'))]
        if filter_name:
            data = data[data['שם פרטי ושם משפחה '].str.contains(filter_name, case=False, na=False)]

        st.dataframe(data)

        
    if selected == "בקשות עם ציון":
        dogs_df = pd.read_csv('Data/Dogs.csv')
        status = st.selectbox(
        "Select Adoption Status",
        ["כל הבקשות", "לא מאומצים", "מאומצים"]
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
    multi = 0
    # if dog['Name'] == applicant['בנוגע לאיזה מהכלבים שלנו פניתם 🐕']:
    #     multi = 1
    # if dog['Children_Friendly'] and applicant["מספר הנפשות הגרות בבית"]> 0:
    #     score +=10
    # if dog['Children_Friendly'] and applicant
    
    # if dog['EnergyLevel'] <=1 and applicant["Calm"] == 1:
    #     score += 20
    # if dog['EnergyLevel'] >1 and applicant["Active"]:
    #     score +=20
    

    # if dog['AnimalFriendly'] and applicant['Animal Friendly']:
    #     score += 15

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
