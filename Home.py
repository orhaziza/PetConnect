import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import bcrypt
import datetime as dt

# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon='Data/Logo.png')

# Define CSS styles for better visual design
st.markdown("""
    <style>
        .header {
            text-align: center;
            font-size: 2.5em;
            margin-top: 20px;
            color: #1a73e8;
        }
        .subheader {
            text-align: center;
            font-size: 1.5em;
            color: #1a73e8;
        }
        .login-container {
            max-width: 500px;
            margin: auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            background-color: #f9f9f9;
        }
        .record {
            text-align: right;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-bottom: 10px;
            background-color: #f1f1f1;
        }
        .refresh-btn {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
    </style>
""", unsafe_allow_html=True)

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
    st.markdown("<h1 class='header'>ברוך הבא לPetConnect</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subheader'>Please log in to access the system.</h2>", unsafe_allow_html=True)

    # User input for login
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
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
    
    if 'seen_records' not in st.session_state:
        st.session_state['seen_records'] = []

    st.markdown("<h1 class='header'>מסך עדכונים</h1>", unsafe_allow_html=True)

    with st.container():
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
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Add a unique identifier to each record
    df['Record ID'] = df.index
    
    # Filter the DataFrame to include only records from the past two days and unseen records
    two_days_ago = dt.datetime.now() - dt.timedelta(days=2)
    recent_df = df[(df['Timestamp'] >= two_days_ago) & (~df['Record ID'].isin(st.session_state['seen_records']))]
    
    # Display the number of records
    if len(recent_df) > 0:
        st.markdown(f"<h2 class='subheader'>התקבלו {len(recent_df)} בקשות ביומיים האחרונים</h2>", unsafe_allow_html=True)
        
        # Display each record as text
        for i in range(len(recent_df)):
            st.markdown(f"""
            <div class='record'>
                <p><b>שם:</b> {recent_df.iloc[i]['Full Name']}</p>
                <p><b>כלב:</b> {recent_df.iloc[i]['Which dog are you interested in?']}</p>
                <p><b>מידע נוסף:</b> {recent_df.iloc[i]['Additional information']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.checkbox("ראיתי", key=f"seen_{recent_df.iloc[i]['Record ID']}"):
                st.session_state['seen_records'].append(recent_df.iloc[i]['Record ID'])
    else:
        st.markdown("<h2 class='subheader'>אין עדכונים חדשים!</h2>", unsafe_allow_html=True)

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
