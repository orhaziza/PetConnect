import streamlit as st
import pandas as pd
from Pages import Dogs, FosterHome, adopters
# Set up the page configuration
st.set_page_config(page_title='PetConnect Management System', layout='wide')

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
            st.session_state['current_page'] = 'Dogs'
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
        if st.session_state['current_page'] == 'Home':
            show_home_page()
        elif st.session_state['current_page'] == 'Dogs':
            Dogs.show_dogs_page()
else:
    show_login_page()
