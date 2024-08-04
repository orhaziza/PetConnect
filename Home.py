import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import bcrypt
import datetime as dt

# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon='Data/Logo.png')

con1 = st.container()
with con1:
    col1, col2 = st.columns([5, 1])
    with col2:
        st.image("Data/Logo.png", width=120)

# User credentials (in a real app, use a secure method for handling credentials)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Function to check password
def check_password(password, hashed):
    return password == hashed

def load_users():
    df = pd.read_csv("Data/Users.csv")
    return df

def login(username, password):
    users = load_users()
    user = users[users['username'] == username]
    
    if not user.empty:
        stored_password = user.iloc[0]['password']
        if check_password(password, stored_password):
            return True
    return False

# Function to show the login form and handle the login process
def show_login_page():
    st.markdown("<h1 style='text-align: right;'>PetConnectברוך הבא ל</h1>", unsafe_allow_html=True)
    
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
    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"

    @st.cache_data()
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        return conn.read(spreadsheet=url)
        
    if st.button("רענן"):
        st.cache_data.clear()
        st.success("המידע עודכן!")
    
    df = fetch_data()
    
    # Ensure the timestamp column is in datetime format
    df['חותמת זמן'] = pd.to_datetime(df['חותמת זמן'])
    
    # Filter the DataFrame to include only records from the past two days
    two_days_ago = dt.datetime.now() - dt.timedelta(days=2)
    recent_df = df[df['חותמת זמן'] >= two_days_ago]
    
    # Set the title and subtitle
    st.markdown("<h1 style='text-align: center;'>מסך עדכונים</h1>", unsafe_allow_html=True)
    
    # Display the number of records
    st.markdown(f"<h2 style='text-align: center;'>התקבלו {len(recent_df)} בקשות ביומיים האחרונים</h2>", unsafe_allow_html=True)
    
    # Display each record as text
    for index, row in recent_df.iterrows():
        st.markdown(f"""
        <div style='text-align: right;'>
            <p>שם: {row['שם פרטי ושם משפחה']}</p>
            <p>כלב: {row['בנוגע לאיזה מהכלבים שלנו פניתם 🐕']}</p>
            <p>מידע נוסף: {row['כל אינפורמציה נוספת שנראית לכם רלוונטית 🌺']}</p>
        </div>
        <hr>
        """, unsafe_allow_html=True)

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
