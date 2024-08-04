import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import bcrypt
import datetime as dt

# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon='Data/Logo.png')

# Define CSS styles for the vibrant design
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #ffffff; /* White background */
        }
        .header {
            text-align: center;
            font-size: 2.5em;
            margin-top: 20px;
            color: #7C00FE; /* Purple color for headers */
        }
        .subheader {
            text-align: center;
            font-size: 1.5em;
            color: #F9E400; /* Bright yellow color for subheaders */
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
            background-color: #FFAF00; /* Orange color for buttons */
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.3s;
        }
        .stButton > button:hover {
            background-color: #E09F00; /* Darker orange on hover */
            transform: scale(1.05);
        }
        .stButton > button.logout {
            background-color: #F5004F; /* Pink color for logout button */
            border-radius: 5px;
            transition: background-color 0.3s, transform 0.3s;
        }
        .stButton > button.logout:hover {
            background-color: #CC0041; /* Darker pink on hover */
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

con1 = st.container()
with con1:
    col1, col2 = st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)

# User credentials (in a real app, use a 
