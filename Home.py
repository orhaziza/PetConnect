import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import datetime as dt
import hashlib
import background
import gspread
from google.oauth2.service_account import Credentials

# Set up the page configuration
st.set_page_config(page_title='פט קונקט', layout='wide', page_icon='Data/Logo.png')
background.add_bg_from_local('static/background3.png')
background.load_css('styles.css')

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_gspread_client():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes = SCOPES)
    client = gspread.authorize(creds)
    return client

# Open the spreadsheet and worksheet
def open_google_sheet():
    client = get_gspread_client()
    sheet = client.open_by_key("1mzpSFmH7aRoeDF0DiSrrFgHPwRJTwUkk7Vuosy3yT6A")
    worksheet = sheet.worksheet("תגובות לטופס 2")  # Name of the sheet
    return worksheet

# Function to update the "Seen" column
def mark_as_seen(record_id):
    worksheet = open_google_sheet()

    try:
        # Convert the record_id (timestamp) to the format used in Google Sheets
        formatted_record_id = record_id.strftime('%d/%m/%Y %H:%M:%S')  # Change format here for search
        cell = worksheet.find(formatted_record_id)  # Search for formatted timestamp
        if cell:
            worksheet.update_cell(cell.row, 16, 1)  # Update 'Seen' column (P)
            return True
    except Exception as e:
        st.error(f"Error updating Google Sheet: {e}")
    return False

    
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
    con1 = st.container()
    with con1:
        col1, col2 = st.columns([6,1])
        with col1:
            st.markdown("<h1 style='text-align: right;'>ברוך הבא לPetConnect</h1>", unsafe_allow_html=True)
            st.subheader("אנא התחבר למערכת")
        with col2:
            st.image("Data/Logo.png", width=120)

    # User input for login
    username = st.text_input("שם משתמש")
    password = st.text_input("סיסמה", type="password")
    flag = False
    con1 = st.container()
    with con1:
        col1, col2 = st.columns([7,1])
        with col2:
            # Login button
            if st.button("התחבר", use_container_width=True):
                if login(username, password):
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.experimental_rerun()  # Refresh the page to update the content
                else:
                    flag = True
    if flag:
        st.error("Invalid username or password")
                    

# Function to show the home page
def show_home_page():
    url = "https://docs.google.com/spreadsheets/d/1mzpSFmH7aRoeDF0DiSrrFgHPwRJTwUkk7Vuosy3yT6A/edit?usp=sharing"
        # Custom CSS to center-align the option menu
    
    @st.cache_data()
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
        return conn.read(spreadsheet=url)
    
    if 'seen_records' not in st.session_state:
        st.session_state['seen_records'] = []
    
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
    df['Record ID'] = df['Timestamp']
    
    # Filter the DataFrame to include only records from the past two days and unseen records
    two_days_ago = dt.datetime.now() - dt.timedelta(days=2)
    recent_df = df[(df['Timestamp'] >= two_days_ago) &  (df['Seen'] != 1) & (~df['Record ID'].isin(st.session_state['seen_records']))]
    

    with st.container():
        col4, col1, col2 = st.columns([1, 10, 1])
        with col1:
            st.markdown("<h1 style='text-align: center;'>מסך עדכונים</h1>", unsafe_allow_html=True)
        with col2:
            st.image("Data/Logo.png", width=100)
    
    with st.container():
        col1, col2, col3 = st.columns([10, 2.5, 9])
        with col2:
            if st.button("רענן"):
                st.cache_data.clear()
                st.success("‏המידע עודכן בהצלחה")
    # Display the number of records
    
    if len(recent_df) > 0:
        st.markdown(f"<h3 style='text-align: center;'>התקבלו {len(recent_df)} בקשות ביומיים האחרונים</h3>", unsafe_allow_html=True)
        
# Display each record as text
        for i in range(len(recent_df)):
            record_id = recent_df.iloc[i]['Record ID']
            phone_number = str(int(recent_df.iloc[i]['Phone number'])).zfill(10)
            formatted_phone_number = f"{phone_number[:3]}-{phone_number[3:]}"
            st.markdown(f"""
<div style='text-align: right; padding: 20px; margin-bottom: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); background-color: white; border-radius: 10px;'>
    <p><b>שם:</b> {recent_df.iloc[i]['Full Name']}</p>
    <p><b>כלב:</b> {recent_df.iloc[i]['Which dog are you interested in?']}</p>
    <p><b>מידע נוסף:</b> {recent_df.iloc[i]['Additional information']}</p>
    <p><b>מספר הטלפון:</b> {formatted_phone_number}</p>
</div>
""", unsafe_allow_html=True)

    # Create a container with columns for button alignment
            col1, col2, col3 = st.columns([1, 0.2, 0.2])  # Adjust the ratios as needed
            with col1:
                if st.button(f"סמן כראיתי", key=f"seen_button_{i}"):  # Assign a unique key for each button
                    success = mark_as_seen(record_id)
                    if success:
                        st.session_state['seen_records'].append(record_id)
                        st.experimental_rerun()  # Rerun the app to reflect the updated seen state
                    else:
                        st.error("Could not update the record in Google Sheets.")
        st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center;'>אין עדכונים חדשים!</h2>", unsafe_allow_html=True)



# Check if the user is logged in
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Main routing logic
if st.session_state['logged_in']:
    if st.sidebar.button("Log Out"):
        st.session_state["step"] = 0
        st.session_state['logged_in'] = False
        st.experimental_rerun()  # Refresh the page to update the content
    else:
        show_home_page()
else:
    show_login_page()
