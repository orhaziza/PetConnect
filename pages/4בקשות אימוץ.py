import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
from streamlit_gsheets import GSheetsConnection
import background
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title='Applications', layout='wide')
    
def show_application_page():
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"
    
    background.insert_logo("בקשות אימוץ")
    

    # Define the menu options
    selected = option_menu(
        menu_title="",  # Required
        options=["בקשות עם ציון", "כל הבקשות"],  # Added new option for the table with scores
        icons=["search", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=1,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
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
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_dog = st.selectbox(label='שם הכלב:',options=data['בנוגע לאיזה מהכלבים שלנו פניתם 🐕'].unique(),index=None)
            with col2:
                filter_date = st.date_input("תאריך:", value=None)
            with col3:
                filter_name = st.text_input("שם המבקש:")

        # Apply filters only if inputs are provided
        if filter_name:
            data = data[data['שם פרטי ושם משפחה '].str.contains(filter_name, case=False, na=False)]
        if filter_date is not None:
            data = data[data['חותמת זמן'].str.contains(filter_date.strftime('%Y-%m-%d'))]
        if filter_dog:
            data = data[data['בנוגע לאיזה מהכלבים שלנו פניתם 🐕'].str.contains(filter_dog, case=False, na=False)]

        st.dataframe(data)

        
    if selected == "בקשות עם ציון":
        dogs_df = pd.read_csv('Data/Dogs.csv')

        # Select a dog
        st.markdown("<h2>בקשות אימוץ לפי כלב</h2>", unsafe_allow_html=True)
        dog_selection = st.selectbox("בחר כלב לחיפוש", dogs_df["Name"])

        # Filter the selected dog's data
        selected_dog = dogs_df[dogs_df["Name"] == dog_selection].iloc[0]

        # Calculate scores for all applicants for the selected dog
        scores = []
        for i, applicant in data.iterrows():
            score = score_adopter(selected_dog, applicant)
            scores.append({
                'Application ID': applicant['חותמת זמן'],
                'Applicant Name': applicant['שם פרטי ושם משפחה '],
                # 'Contact': data.loc[i,['מספר טלפון']],
                # 'City': data.loc[i,['עיר מגורים']],
                # 'House memebers': data.loc[i,['מספר הנפשות הגרות בבית']],
                # 'Backyard': data.loc[i,['האם יש גינה (מגודרת) בבית?']],
                # 'experience': data.loc[i,['ניסיון עם בעלי חיים?']],
                # 'Adittional animals': data.loc[i,['האם יש בעלי חיים נוספים בבית?']],
                # 'messageContect': data.loc[i,['כל אינפורמציה נוספת שנראית לכם רלוונטית 🌺']],
                # 'SourcePlatform': data.loc[i,['איך הגעתם אלינו?']],
                'Score': score
            })

        # Convert the scores into a DataFrame and display it
        scores_df = pd.DataFrame(scores)
        st.dataframe(scores_df)

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
    score = 30
    multi = 0
    if dog['Name'] == applicant['בנוגע לאיזה מהכלבים שלנו פניתם 🐕']:
        multi = 1
    if dog['Children_Friendly'] == False and applicant["מספר הנפשות הגרות בבית"] > 0:
        score -= 10
    if dog['Children_Friendly'] == False and applicant["גילאי ילדים במידה ויש"] != "בית ללא ילדים":
        score -= 10

    if applicant["האם אימצת אצלנו בעבר?"] == "כן":
        score += 10

    if applicant["האם יש גינה (מגודרת) בבית?"] == "כן":
        score += 10
    if dog['AnimalFriendly'] == False and applicant["האם יש בעלי חיים נוספים בבית?"] == "כן":
        score -= 10

    return score * multi

    

st.session_state["step"] = 0
show_application_page()
