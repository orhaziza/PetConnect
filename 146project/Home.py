import streamlit as st
from Pages import Dogs
 # Ensure these modules exist and are accessible

# Set up the page configuration
st.set_page_config(page_title='PetConnect Management System', layout='wide')

# User credentials (in a real app, use a secure method for handling credentials)
users = {"admin": "admin123", "user": "user123", "yuval": "yuval123"}

# Define the login function
def login(username, password):
    return username in users and users[username] == password

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
            st.session_state['current_page'] = 'Home'  # Initialize to Home page after login
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
            st.experimental_rerun()  # Navigate to Dogs page

    with col2:
        st.subheader("Manage Foster Homes")
        st.write("Manage foster home details and availability.")
        if st.button("Go to Foster Homes"):
            st.session_state['current_page'] = 'FosterHomes'
            st.experimental_rerun()  # Navigate to Foster Homes page

    with col3:
        st.subheader("Manage Adopters")
        st.write("Track and manage adopter information and preferences.")
        if st.button("Go to Adopters"):
            st.session_state['current_page'] = 'Adopters'
            st.experimental_rerun()  # Navigate to Adopters page

# Main routing logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Check if the user is logged in
if st.session_state['logged_in']:
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.session_state['current_page'] = 'Home'
        st.experimental_rerun()  # Refresh the page to update the content
    else:
        # Navigate based on current page
        if 'current_page' not in st.session_state:
            show_login_page()
        if st.session_state['current_page'] == 'Home':
            show_home_page()
        elif st.session_state['current_page'] == 'Dogs':
            Dogs.show_dogs_page()
        elif st.session_state['current_page'] == 'FosterHomes':
            FosterHome.show_foster_homes_page()
        elif st.session_state['current_page'] == 'Adopters':
            Adopters.show_adopters_page()
else:
    show_login_page()
