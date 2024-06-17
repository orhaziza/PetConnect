import streamlit as st
import pandas as pd

# Set up the page configuration
st.set_page_config(page_title='PetConnect Management System', layout='wide')
st.markdown("""
<style>
    /* Importing the Roboto font from Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    /* Apply Roboto font family */
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif; /* Roboto is applied universally */
        background-color: #f8f9fa; /* Light grey background color */
    }

    /* Titles and subtitles with specific weight */
    .css-2trqyj, .css-1d391kg {
        color: #0c6efd; /* Bright blue for main titles */
    }
    
    .css-1e5imcs {
        color: #6c757d; /* Dark grey for subtitles */
    }
    
    /* Styling text input fields */
    .stTextInput input {
        border-radius: 10px; /* Rounded corners for text input */
        border: 1px solid #ced4da; /* Grey border for text inputs */
    }
    
    /* Customizing buttons */
    .stButton > button {
        border-radius: 20px; /* Rounded corners for buttons */
        border: none; /* No borders */
        background-color: #0d6efd; /* Bright blue background */
        color: white; /* White text */
    }

    /* Button hover effect */
    .stButton > button:hover {
        background-color: #0a58ca; /* Slightly darker blue on hover */
    }

    /* Adjusting columns padding and margin */
    .st-cx {
        padding: 10px 0; /* Padding for columns */
        margin: 0 10px; /* Margin around columns */
    }
</style>
""", unsafe_allow_html=True)

# User credentials (in a real app, use a secure method for handling credentials)
users = {"admin": "admin123", "user": "user123", "yuval": "yuval123"}

# Define the login function
def login(username, password):
    if username in users and users[username] == password:
        return True
    else:
        return False

# Function to show the login form and handle the login process
def show_login_page():
    st.title("PetConnect Management System")
    st.subheader("Please log in to access the system.")

    # User input for login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if login(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.experimental_rerun()  # Refresh the page to update the content
        else:
            st.error("Invalid username or password")

# Function to show the home page
def show_home_page():
    st.title(f"Welcome, {st.session_state['username']}!")
    st.header("PetConnect Management System")
    st.write("This is your personalized home screen.")

    st.subheader("Quick Links")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Manage Dogs")
        st.write("View and manage information about dogs.")
        if st.button("Go to Dogs"):
            st.experimental_rerun()  # Placeholder for navigating to dogs page

    with col2:
        st.subheader("Manage Foster Homes")
        st.write("Manage foster home details and availability.")
        if st.button("Go to Foster Homes"):
            st.experimental_rerun()  # Placeholder for navigating to foster homes page

    with col3:
        st.subheader("Manage Adopters")
        st.write("Track and manage adopter information and preferences.")
        if st.button("Go to Adopters"):
            st.experimental_rerun()  # Placeholder for navigating to adopters page

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
