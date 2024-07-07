import streamlit as st
import pandas as pd
import toml
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title='PetConnect Management System', layout='wide')

con1 = st.container()
with con1:
    col1, col2= st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)

users = {"admin": "admin123", "user": "user123"}

# Define the login function
def login(username, password):
    if username in users and users[username] == password:
        return True
    else:
        return False


# Function to show the login form and handle the login process
def show_login_page():
    st.markdown("<h1 style='text-align: right; color: red;'>PetConnectברוך הבא ל</h1>", unsafe_allow_html=True)
    st.title("PetConnectברוך הבא ל")
    st.subheader("הזן שם משתמש וסיסמא")

    # User input for login
    username = st.text_input("שם משתמש")
    password = st.text_input("סיסמא", type="password")

    # Login button
    if st.button("Login"):
        if login(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.experimental_rerun()  # Refresh the page to update the content
        else:
            st.error("שם משתמש או סיסמא לא תקינים")

# Function to show the home page
def show_home_page():
    st.title(f"ברוך הבא, {st.session_state['username']}!")
    st.header(" מערכת הניהול של PetConnect ")
    dogs_file_path = "Data/Dogs.csv"
    dog_df = pd.read_csv(dogs_file_path, encoding='Windows-1255')
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
        # Add more column name translations as needed
    }
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
    dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

    st.subheader("כלבים שלא אומצו")
    filtered_df = dog_df_hebrew[
            (dog_df['adoptionStatus'] != 'אומץ')]

    st.write(filtered_df)

# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Main routing logic
if st.session_state['logged_in']:
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()  # Refresh the page to update the content
    else:
        show_home_page()
else:
    show_login_page()
