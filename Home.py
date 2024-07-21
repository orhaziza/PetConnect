import streamlit as st
import pandas as pd
    
# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon = 'Data/Logo.png' )

con1 = st.container()
with con1:
    col1, col2= st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)


# User credentials (in a real app, use a secure method for handling credentials)
users = {"admin": "admin123", "user": "user123"}

# Define the login function
def login(username, password):
    
    if username in users and users[username] == password:
        return True
    else:
        return False

# Function to show the login form and handle the login process
def show_login_page():
    st.markdown("<h1 style='text-align: right;'>PetConnectברוך הבא ל</h1>", unsafe_allow_html=True)
    
    # st.title("PetConnect Management System")
    # st.image('Data/Logo.png', use_column_width=True)  # Replace 'path_to_your_logo.png' with your logo file path

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

def add_logo():
    st.sidebar.markdown(
        """
        <style>
            .logo-container {
                display: flex;
                justify-content: flex-start; /* Aligns the logo to the top left */
                align-items: center;
                height: 100px; /* Adjust height as needed */
            }
            .logo-container img {
                width: 80px; /* Adjust width as needed */
                cursor: pointer; /* Pointer cursor on hover */
            }
        </style>
        <div class="logo-container">
            <a href="/">
                <img src="Data/Logo.png" alt="Logo">
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
# Function to show the home page
def show_home_page():
    # st.sidebar.image('Data/Logo.png', use_column_width=True)  # Replace 'path_to_your_logo.png' with your logo file path
    # add_logo()
    st.title(f"Welcome, {st.session_state['username']}!")
    st.header("PetConnect Management System")
    st.write("This is your personalized home screen.")
    # col_logo, _ = st.columns([3, 1])
    # with col_logo:
    #     if st.button("Home", key='home_button'):
    #         st.experimental_set_query_params(page="home")
    #         st.experimental_rerun()
    #
    #
    # st.subheader("Quick Links")
    # col1, col2, col3 = st.columns(3)
    #
    # with col1:
    #     st.subheader("Manage Dogs")
    #     st.write("View and manage information about dogs.")
    #     if st.button("Go to Dogs"):
    #         st.experimental_set_query_params(page="dogs")
    #
    # with col2:
    #     st.subheader("Manage Foster Homes")
    #     st.write("Manage foster home details and availability.")
    #     if st.button("Go to Foster Homes"):
    #         st.experimental_rerun()  # Placeholder for navigating to foster homes page
    #
    # with col3:
    #     st.subheader("Manage Adopters")
    #     st.write("Track and manage adopter information and preferences.")
    #     if st.button("Go to Adopters"):
    #         st.query_params(page="Dogs")

    # Logo display as a button on the home page
    col_logo, _ = st.columns([3, 1])
    with col_logo:
        if st.button("Home", key='home_button'):
            st.session_state['page'] = "home"

    st.write("This is your personalized home screen.")

    st.subheader("Quick Links")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Manage Dogs")
        st.write("View and manage information about dogs.")
        if st.button("Go to Dogs"):
            st.switch_page("pages/Dogs.py")
    with col2:
        st.subheader("Manage Foster Homes")
        st.write("Manage foster home details and availability.")
        if st.button("Go to Foster Homes"):
            st.switch_page('pages/FosterHome.py')
    with col3:
        st.subheader("Manage Adopters")
        st.write("Track and manage adopter information and preferences.")
        if st.button("Go to Adopters"):
            st.switch_page("pages/adopters.py")

    # Logo display on the right side of every page


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

