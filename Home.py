import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import datetime as dt
import hashlib

# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon='Data/Logo.png')



con1 = st.container()
with con1:
    col1, col2 = st.columns([1, 5])
    with col2:
        st.markdown("<h1 style='text-align: center; PetConnect ברוך הבא ל</h1>", unsafe_allow_html=True)
    with col1:
        st.image("Data/Logo.png", width=120)

# Function to hash the password using SHA-256
def hash_password(password):
    sha_signature = hashlib.sha256(password.encode()).hexdigest()
    return sha_signature

# Function to check password
def check_password(password, hashed):
    return hash_password(password) == hashed

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
        # Custom CSS to center-align the option menu
    st.markdown(
        """
        <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    
    .stButton > button {
        color: #ffffff; /* White text for buttons */
        background-color: #30475E; /* Dark blue color for buttons */
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-size: 1em;
    }
    .stButton > button:hover {
        background-color: #25394C; /* Darker blue on hover */
        transform: scale(1.05);
    }
    .stButton > button.logout {
        background-color: #F05454; /* Red color for logout button */
        border-radius: 5px;
        transition: background-color 0.3s, transform 0.3s;
        padding: 10px 20px;
        font-size: 1em;
    }
    .stButton > button.logout:hover {
        background-color: #C74444; /* Darker red on hover */
        transform: scale(1.05);
    }
    .icon-button {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .icon-button img {
        margin-right: 5px;
    }
    .option-menu-container {
        display: flex;
        justify-content: center;
    }
    .dataframe-container {
        background-color: #ffffff; /* White background for dataframe */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 10px;
    }
    .file-upload-container {
        background-color: #ffffff; /* White background for file upload */
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin-top: 20px;
    }
    .stDownloadButton > button {
        color: #ffffff; /* White text for download buttons */
        background-color: #30475E; /* Dark blue color for download buttons */
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s, transform 0.3s;
        font-size: 1em;
    }
    .stDownloadButton > button:hover {
        background-color: #25394C; /* Darker blue on hover */
        transform: scale(1.05);
    }
    </style>

        """,
        unsafe_allow_html=True
    )
    @st.cache_data()
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        return conn.read(spreadsheet=url)
    
    if 'seen_records' not in st.session_state:
        st.session_state['seen_records'] = []
    
    with st.container():
        col1, col2, col3 = st.columns([1.5, 1, 1])
        with col2:
            if st.button("רענן"):
                st.cache_data.clear()
                st.success("המידע עודכן!")
    
    df = fetch_data()
    
    # Clean up the column names
    df.columns = [col.strip() for col in df.columns]
    
    # Mapping Hebrew column names to English equivalents
    columns_mapping = {
        'חותמת זמן': 'Timestamp',
        'איך הגעתם אלינו?': 'How did you hear about us?',
        'בנוגע לאיזה מהכלבים שלנו פניתם 🐕': 'Which dog are you interested in?',
        'שם פרטי ושם משפחה': 'Full Name',
        'עיר מגורים': 'City',
        'מספר הנפשות הגרות בבית': 'Number of people in household',
        'גילאי ילדים במידה ויש': 'Ages of children (if any)',
        'כל אינפורמציה נוספת שנראית לכם רלוונטית 🌺': 'Additional information',
        'מספר טלפון': 'Phone number',
        'האם אימצת אצלנו בעבר?': 'Have you adopted from us before?',
        'האם יש גינה (מגודרת) בבית?': 'Do you have a garden (fenced)?',
        'ניסיון עם בעלי חיים?': 'Experience with animals?',
        'האם יש בעלי חיים נוספים בבית': 'Do you have other pets?',
        'זמינות': 'Availability',
        'במידה ויש, אילו?': 'If any, which?'
    }

    # Rename the columns in the DataFrame
    df.rename(columns=columns_mapping, inplace=True)

    # Ensure the timestamp column is in datetime format
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%d/%m/%Y %H:%M:%S")
    
    # Add a unique identifier to each record
    df['Record ID'] = df.index
    
    # Filter the DataFrame to include only records from the past two days and unseen records
    two_days_ago = dt.datetime.now() - dt.timedelta(days=2)
    recent_df = df[(df['Timestamp'] >= two_days_ago) & (~df['Record ID'].isin(st.session_state['seen_records']))]
    
    # Set the title and subtitle
    st.markdown("<h1 style='text-align: center;'>מסך עדכונים</h1>", unsafe_allow_html=True)
    
    # Display the number of records
    if len(recent_df) > 0:
        st.markdown(f"<h2 style='text-align: center;'>התקבלו {len(recent_df)} בקשות ביומיים האחרונים</h2>", unsafe_allow_html=True)
        
        # Display each record as text
        for i in range(len(recent_df)):
            phone_number = str(int(recent_df.iloc[i]['Phone number'])).zfill(10)
            formatted_phone_number = f"0{phone_number[:2]}-{phone_number[2:]}"
            
            st.markdown(f"""
            <div style='text-align: right;'>
                <p><b>שם:</b> {recent_df.iloc[i]['Full Name']}</p>
                <p><b>כלב:</b> {recent_df.iloc[i]['Which dog are you interested in?']}</p>
                <p><b>מידע נוסף:</b> {recent_df.iloc[i]['Additional information']}</p>
                <p><b>מספר הטלפון:</b> {formatted_phone_number}</p>
            </div>
            <hr>
            """, unsafe_allow_html=True)
            if st.checkbox("ראיתי", key=f"seen_{recent_df.iloc[i]['Record ID']}"):
                st.session_state['seen_records'].append(recent_df.iloc[i]['Record ID'])

    else:
        st.markdown("<h2 style='text-align: center;'>אין עדכונים חדשים!</h2>", unsafe_allow_html=True)

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
