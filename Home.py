import streamlit as st
import pandas as pd
import bcrypt
# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon = 'Data/Logo.png' )

con1 = st.container()
with con1:
    col1, col2= st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)


# User credentials (in a real app, use a secure method for handling credentials)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to check password
def check_password(password, hashed):
    st.write("Checking password:", password)  # Debug: Show the entered password
    st.write("With hashed password:", hashed)  # Debug: Show the stored hashed password
    if isinstance(hashed, str):
        hashed = hashed.encode()
    return bcrypt.checkpw(password.encode(), hashed)
    
def load_users():
    df = pd.read_csv("Data/Users.csv")
    return df
    


def login(username, password):
    users = load_users()
    st.write("Loaded users:", users)  # Debug: Show the loaded users DataFrame
    
    user = users[users['username'] == username]
    st.write("Filtered user:", user)  # Debug: Show the filtered user DataFrame
    
    if not user.empty:
        stored_password = user.iloc[0]['password']
        st.write("Stored password for user:", stored_password)  # Debug: Show the stored password
        if check_password(password, stored_password):
            return True
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
    df = pd.read_csv('Data/AdoptionApplication.csv')
    st.dataframe(df)

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

