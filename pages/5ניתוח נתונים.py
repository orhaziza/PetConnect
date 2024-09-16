# import streamlit as st
# import pandas as pd
# import os
# from datetime import datetime
# from streamlit_option_menu import option_menu
# import matplotlib.pyplot as plt
# import numpy as np
# from streamlit_gsheets import GSheetsConnection
# import altair as alt
# import background

# data_url = "https://docs.google.com/spreadsheets/d/1mzpSFmH7aRoeDF0DiSrrFgHPwRJTwUkk7Vuosy3yT6A/edit?usp=sharing"

# def show_data_analysis_page():
#     st.set_page_config(page_title='Data Analysis', layout='wide')

#     background.add_bg_from_local('./static/background3.png')
#     background.load_css('styles.css')

#     if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
#         st.error("לא ניתן לגשת לעמוד ללא התחברות")
#         st.stop()
    
#     with st.container():
#         col1, col2 = st.columns([15, 1])
#         with col1:
#             st.markdown("<h1 style='text-align: center;'>ניתוח נתונים</h1>", unsafe_allow_html=True)
#             st.markdown("<h4 style='text-align: center;'>כאן תוכלו לצפות בויזואליזציות על בסיס הנתונים שנאספו עד כה</h4>", unsafe_allow_html=True)
#             col3, col4, col5 = st.columns([2,1,2])
#             with col4:
#                 if st.button("רענן", use_container_width=True):
#                     st.success("המידע התעדכן בהצלחה")
#                     st.cache_data.clear()
#         with col2:
#             st.image("Data/Logo.png", width=100)

#     url = "https://docs.google.com/spreadsheets/d/1mzpSFmH7aRoeDF0DiSrrFgHPwRJTwUkk7Vuosy3yT6A/edit?usp=sharing"
#         # Custom CSS to center-align the option menu

   
#     adopter_file_path = "Data/Adopters.csv"
#     if not os.path.exists(adopter_file_path):
#         st.error("The adopter file does not exist.")
#         st.stop()
#     adopter_df = pd.read_csv(adopter_file_path, encoding='utf-8')

#     dogs_file_path = "Data/Dogs.csv"
#     if not os.path.exists(dogs_file_path):
#         st.error("Dogs file does not exist.")
#         st.stop()
#     dogs_df = pd.read_csv(dogs_file_path, encoding='utf-8')

#     FosterHome_file_path = "Data/FosterHome.csv"
#     if not os.path.exists(FosterHome_file_path):
#         st.error("Foster Home file does not exist.")
#         st.stop()
#     Foster_Home_df = pd.read_csv(FosterHome_file_path, encoding='utf-8')

#     with st.container():
#         col1 , col2 = st.columns([1,1], gap="small")
#         with col1:
#             st.markdown("<h5 style='text-align: center;'>התפלגות בתי אומנה</h5>", unsafe_allow_html=True)
#             plot_Fosters(Foster_Home_df)
#         with col2:
#             st.markdown("<h5 style='text-align: center;'>התפלגות הכלבים בעמותה</h5>", unsafe_allow_html=True)
#             plot_Dogs(dogs_df)
    
#     with st.container():
#         col1 , col2 , col3 = st.columns([1,1,1], gap="small")
#         with col1:
#             st.markdown("<h5 style='text-align: center;'>התפלגות בקשות אימוץ לפי פלטפורמת פרסום</h5>", unsafe_allow_html=True)
#             plot_Applications(fetch_data())
#         with col2:
#             st.markdown("<h5 style='text-align: center;'>בקשות אימוץ לאורך זמן</h5>", unsafe_allow_html=True)
#             plot_Applications_Flow(fetch_data())
#         with col3:
#             st.markdown("<h5 style='text-align: center;'>בקשות אימוץ לפי יום בשבוע</h5>", unsafe_allow_html=True)
#             plot_Applications_by_WkDay(fetch_data())

#     # Sidebar logout button
#     if st.sidebar.button("Log Out"):
#         st.session_state['logged_in'] = False
#         st.experimental_rerun()
        
# @st.cache_data()
# def fetch_data():
#     conn = st.connection("gsheets", type=GSheetsConnection)
#     return conn.read(spreadsheet=data_url)

# def plot_Applications(application_df):
#     platform_counts = application_df.iloc[:, 1].value_counts()
#     labels = [label[::-1] for label in platform_counts.index.tolist()]
#     values = platform_counts.tolist()
#     fig, ax = plt.subplots()
#     fig.patch.set_facecolor('none')
#     ax.patch.set_facecolor('none')
#     ax.pie(values, labels = labels, autopct='%1.1f%%', startangle=140)
#     ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     st.pyplot(fig)

# def plot_Fosters(Foster_Home_df):
#     lst = ['HouseSize','Backyard','NearDogPark','HouseMembers','AvailabilityAtHome','ChildrenFriendly','AnimalFriendly','MaximumCapacity','AllowedAtProperty','Allergies','IsMobile','EnergyLevel','PastFosters','PastExperience']
#     st.markdown(
#             """
#             <style>
#             .stSelectbox label {
#                 display: block;
#                 text-align: center;
#             }
#             </style>
#             """, 
#             unsafe_allow_html=True
#         )

#     characteristic = st.selectbox(':בחר מאפיין', lst)
#     if Foster_Home_df[characteristic].dtype == 'bool':
#         distribution = Foster_Home_df[characteristic].astype(str).value_counts()
#         # st.subheader(f'Distribution of foster homes by {characteristic.capitalize()}')
#         st.bar_chart(distribution)
#     else:
#         distribution = Foster_Home_df[characteristic].value_counts()
#         # st.subheader(f'Distribution of foster homes by {characteristic.capitalize()}')
#         st.bar_chart(distribution)

# def plot_Dogs(dogs_df):
#     lst = ['Age','Breed','Weight','Size','Gender','RescueDate','Rabies_Done','Hexagonal_1','Hexagonal_2','Hexagonal_3','Hexagonal_Done','Spayed','De-worm','ChildrenFriendly','AnimalFriendly','HealthStatus','EnergyLevel','PhotographStatus','AdoptionStatus','AdopterID','PottyTrained']

#     st.markdown(
#         """
#         <style>
#         .stSelectbox label {
#             display: block;
#             text-align: center;
#         }
#         </style>
#         """, 
#         unsafe_allow_html=True
#     )
#     characteristic = st.selectbox(':בחר מאפיין', lst)
    
#     if dogs_df[characteristic].dtype == 'bool':
#       # Convert boolean to string
#         distribution = dogs_df[characteristic].astype(str).value_counts()
#         # st.subheader(f'Distribution of Dogs by {characteristic.capitalize()}')
#         st.bar_chart(distribution)
#     else:
#         distribution = dogs_df[characteristic].value_counts()
#         # st.subheader(f'Distribution of Dogs by {characteristic.capitalize()}')
#         st.bar_chart(distribution)

# def plot_Applications_Flow(application_df):
#     df = application_df
#     df["חותמת זמן"] = pd.to_datetime(application_df["חותמת זמן"], yearfirst=True, format='%d/%m/%Y %H:%M:%S')

#     st.markdown(
#         """
#         <style>
#         .stRadio {
#             display: flex;
#             align-items: center;
#             justify-content: flex-start; /* Align the label and options to the start (left) */
#             direction: rtl; /* Set the direction to RTL to handle Hebrew text correctly */
#         }
#         .stRadio > label {
#             margin-left: 100px;  /* Add space between the label and the options */
#             font-weight: bold;  /* Optional: Make the label bold */
#             white-space: nowrap; /* Prevent the label from wrapping to the next line */
#         }
#         .stRadio div {
#             display: flex;
#             flex-direction: row-reverse; /* Display the options to the left of the label */
#         }
#         .stRadio div label {
#             margin-left: 15px; /* Add space between the options */
#             display: flex;
#             align-items: center;
#         }
#         </style>
#         """, 
#         unsafe_allow_html=True
#     )

#     view = st.radio("בחר:", ("שבועי", "חודשי"))

#     if view == "שבועי":
#         df["Period"] = df["חותמת זמן"].dt.to_period('W').apply(lambda r: r.start_time)
#         df['Period'] = df['Period'].dt.strftime('%Y-%m-%d')
#     else:
#         df["Period"] = df["חותמת זמן"].dt.to_period('M').apply(lambda r: r.start_time)
#         df['Period'] = df['Period'].dt.strftime('%Y-%m')

#     # Count the number of requests per period
#     request_counts = df['Period'].value_counts().sort_index()
#     request_counts = request_counts.reset_index()
#     request_counts.columns = ['Period', 'RequestCount']
#     request_counts.set_index('Period', inplace=True)

#     # Plot the request counts using st.line_chart
#     st.line_chart(request_counts)

# def plot_Applications_by_WkDay(application_df):
#     df = application_df
#     df["חותמת זמן"] = pd.to_datetime(application_df["חותמת זמן"], yearfirst=True, format='%d/%m/%Y %H:%M:%S').dt.day_name()
#     distribution = df["חותמת זמן"].value_counts()
#     days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     distribution = distribution.reindex(days_of_week, fill_value=0)
#     distribution_df = distribution.reset_index()
#     distribution_df.columns = ['Day', 'Count']
    
#     # Create a bar chart using Altair
#     chart = alt.Chart(distribution_df).mark_bar().encode(
#         x=alt.X('Day', sort=days_of_week),y='Count')
#     st.altair_chart(chart, use_container_width=True)



# show_data_analysis_page()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from streamlit_gsheets import GSheetsConnection
import background

adopter_data_url = "https://docs.google.com/spreadsheets/d/1zGvjYm0Co2tLrA4TD1hiMkq4zbeNtagNbj21kAXeWc0/edit?usp=sharing"
dogs_data_url = "https://docs.google.com/spreadsheets/d/1USkylM0mrZMqs3unWUYCtabu-GgQn5HWxt1cIi2C-hw/edit?usp=sharing"
foster_home_data_url = "https://docs.google.com/spreadsheets/d/1lAY6gHYO-scPukLMTH8msFzwG9DoNsdq5-kNf2lKbqM/edit?usp=sharing"

def show_data_analysis_page():
    st.set_page_config(page_title='Data Analysis', layout='wide')

    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
    
    with st.container():
        col1, col2 = st.columns([15, 1])
        with col1:
            st.markdown("<h1 style='text-align: center;'>ניתוח נתונים</h1>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center;'>כאן תוכלו לצפות בויזואליזציות על בסיס הנתונים שנאספו עד כה</h4>", unsafe_allow_html=True)
            col3, col4, col5 = st.columns([2,1,2])
            with col4:
                if st.button("רענן", use_container_width=True):
                    st.success("המידע התעדכן בהצלחה")
                    st.cache_data.clear()
        with col2:
            st.image("Data/Logo.png", width=100)

    # Load data from Google Sheets
    adopter_df = fetch_data(adopter_data_url)
    dogs_df = fetch_data(dogs_data_url)
    foster_home_df = fetch_data(foster_home_data_url)
    application_url = "https://docs.google.com/spreadsheets/d/1mzpSFmH7aRoeDF0DiSrrFgHPwRJTwUkk7Vuosy3yT6A/edit?usp=sharing"
    with st.container():
        col1 , col2 = st.columns([1,1], gap="small")
        with col1:
            st.markdown("<h5 style='text-align: center;'>התפלגות בתי אומנה</h5>", unsafe_allow_html=True)
            plot_Fosters(foster_home_df)
        with col2:
            st.markdown("<h5 style='text-align: center;'>התפלגות הכלבים בעמותה</h5>", unsafe_allow_html=True)
            plot_Dogs(dogs_df)
    
    with st.container():
        col1 , col2 , col3 = st.columns([1,1,1], gap="small")
        with col1:
            st.markdown("<h5 style='text-align: center;'>התפלגות בקשות אימוץ לפי פלטפורמת פרסום</h5>", unsafe_allow_html=True)
            plot_Applications(fetch_data(application_url))
        with col2:
            st.markdown("<h5 style='text-align: center;'>בקשות אימוץ לאורך זמן</h5>", unsafe_allow_html=True)
            plot_Applications_Flow(fetch_data(application_url))
        with col3:
            st.markdown("<h5 style='text-align: center;'>בקשות אימוץ לפי יום בשבוע</h5>", unsafe_allow_html=True)
            plot_Applications_by_WkDay(fetch_data(application_url))

    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

@st.cache_data()
def fetch_data(sheet_url):
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(spreadsheet=sheet_url)

def plot_Applications(application_df):
    platform_counts = application_df.iloc[:, 1].value_counts()
    labels = [label[::-1] for label in platform_counts.index.tolist()]
    values = platform_counts.tolist()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('none')
    ax.patch.set_facecolor('none')
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)

def plot_Fosters(Foster_Home_df):
    lst = ["גודל הבית","זמינות בבית","קיבולת מקסימלית","PastExperience","רמת אנרגיה","ידידותי לילדים","ידידותי לכלבים","חברי בית"]
    
    characteristic = st.selectbox(':בחר מאפיין', lst)
    distribution = Foster_Home_df[characteristic].value_counts()
    st.bar_chart(distribution)

def plot_Dogs(dogs_df):
    lst = ["גיל", "משקל", "מין", "זן", "מעוקר", "חיסון משושה", "סטטוס הצילום" ]

    characteristic = st.selectbox(':בחר מאפיין', lst)
    distribution = dogs_df[characteristic].value_counts()
    st.bar_chart(distribution)

def plot_Applications_Flow(application_df):
    df = application_df
    df["חותמת זמן"] = pd.to_datetime(df["חותמת זמן"], yearfirst=True, format='%d/%m/%Y %H:%M:%S')

    view = st.radio("בחר:", ("שבועי", "חודשי"))

    if view == "שבועי":
        df["Period"] = df["חותמת זמן"].dt.to_period('W').apply(lambda r: r.start_time)
        df['Period'] = df['Period'].dt.strftime('%Y-%m-%d')
    else:
        df["Period"] = df["חותמת זמן"].dt.to_period('M').apply(lambda r: r.start_time)
        df['Period'] = df['Period'].dt.strftime('%Y-%m')

    request_counts = df['Period'].value_counts().sort_index()
    request_counts = request_counts.reset_index()
    request_counts.columns = ['Period', 'RequestCount']
    request_counts.set_index('Period', inplace=True)

    st.line_chart(request_counts)

def plot_Applications_by_WkDay(application_df):
    df = application_df
    df["חותמת זמן"] = pd.to_datetime(df["חותמת זמן"], yearfirst=True, format='%d/%m/%Y %H:%M:%S').dt.day_name()
    distribution = df["חותמת זמן"].value_counts()
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    distribution = distribution.reindex(days_of_week, fill_value=0)
    distribution_df = distribution.reset_index()
    distribution_df.columns = ['Day', 'Count']

    chart = alt.Chart(distribution_df).mark_bar().encode(x=alt.X('Day', sort=days_of_week), y='Count')
    st.altair_chart(chart, use_container_width=True)

st.session_state["step"] = 0
show_data_analysis_page()
