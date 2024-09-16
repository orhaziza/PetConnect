import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import io
import os
import background
import base64
from xhtml2pdf import pisa
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

# Directory for storing adopter files
items_url = "https://docs.google.com/spreadsheets/d/14e7lQDBov_c8iaRe7N5AXmMmAW5FzF2NilCTjq7LcAo/edit?usp=sharing"
dogs_url = "https://docs.google.com/spreadsheets/d/1USkylM0mrZMqs3unWUYCtabu-GgQn5HWxt1cIi2C-hw/edit?usp=sharing"

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
    sheet = client.open_by_key("14e7lQDBov_c8iaRe7N5AXmMmAW5FzF2NilCTjq7LcAo")
    worksheet = sheet.worksheet("Sheet1")  # Name of the sheet
    return worksheet
    
def update_google_sheet(edited_df):
    worksheet = open_google_sheet()

    # Replace NaN and infinite values before saving
    edited_df.replace([float('inf'), float('-inf')], '', inplace=True)
    edited_df.fillna('', inplace=True)

    # Option 1: Overwrite the entire sheet (simpler approach)
    worksheet.clear()  # Clear existing content
    worksheet.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())  # Update with new data

        
@st.cache_data()
def fetch_data(url):
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
    return conn.read(spreadsheet=url)
    


st.set_page_config(page_title='Shopping List', layout='wide')

items_df = fetch_data(items_url)
dog_df = fetch_data(dogs_url)
dog_df = dog_df[dog_df["סטטוס אימוץ"] == '0']
hebrew_columns_items = {
    'Product Category': 'קטגוריה',
    'Product ID': 'מזהה מוצר',
    'Product Name': 'שם מוצר',
    'Product Size': 'גודל',
    'Product Size Unit': 'יחידות מידה',
    'Age': 'גיל הכלב',
    'Breed': 'גזע הכלב',
    'Gender': 'מין הכלב',
    'Dog Size': 'גודל הכלב',
    'EnergyLevel': 'רמת האנרגיה',
    'PottyTrained': 'מחונך לצרכים',
    'Product Photo': 'תמונה',
    'Description': 'תיאור'}

items_df = items_df.rename(columns=dict(zip(items_df.columns, [hebrew_columns_items.get(col, col) for col in items_df.columns])))
items_df = items_df.iloc[:, ::-1]

def show_shopping_list_page():    
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()


    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    background.insert_logo("רשימת קניות")


    # Define the menu options
    selected = option_menu(
        menu_title="",  # Required
        options=["ערוך מוצר", "הוסף מוצר", "צור רשימה לכלב"],  # Added new option for the table with scores
        icons=["file", "file", "search"],  # Optional
        menu_icon="menu",  # Optional
        default_index=2,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
        )
    
    if selected == "צור רשימה לכלב":
        col1, col2, col4 = st.columns([4.5, 1, 0.5])
        with col1:
            st.session_state['dog'] = st.selectbox(label='',options=dog_df['שם'].unique(),index=None, placeholder = "בחר כלב")
        with col2:
            if st.button("צור רשימה"):
                st.session_state["shopping list"] = None
                st.session_state["short list"] = None
                if st.session_state['dog'] != None:
                    st.session_state["step"] = 1
                else:
                    st.session_state["step"] = -1
            
    elif selected == "הוסף מוצר" or selected == "ערוך מוצר":
        st.session_state["step"] = 0
        st.write("not yet")

def create_list(dog):
    df = dog_df.loc[dog_df['שם'] == dog].reset_index()
    categories = items_df['קטגוריה'].unique()
    sl = items_df.iloc[:0,:].copy()
    if not (df["גודל"][0]=='XS' or df["גודל"][0]=='S' or df["גודל"][0]=='M' or df["גודל"][0]=='L' or df["גודל"][0]=='XL'):
        st.warning('לא הוגדר גודל לכלב!')    
    for c in categories:
        if c=="גורים":
            if df["גיל"][0]<12:
                category_products = items_df[items_df['קטגוריה'] == c]
                sl = pd.concat([sl, category_products], ignore_index=True) 
        else:    
            category_products = items_df[items_df['קטגוריה'] == c]
            sl = pd.concat([sl, category_products[category_products['גודל הכלב'] == df["גודל"][0]]], ignore_index=True) 

    sl['שמור מוצר'] = True
    st.session_state["shopping list"] = sl
    st.session_state["step"] = 2


def present_list():
    sl = st.data_editor(st.session_state["shopping list"])

    with st.container():
        col1, col2 ,col3, col4=  st.columns([1, 2, 8, 2])        
        if not st.session_state["shopping list"].empty:
            with col1:
                if st.button("שמור"):
                    st.session_state["short list"] = (
                        sl[sl['שמור מוצר'] == True]
                        .loc[:, ["מזהה מוצר", "שם מוצר","גודל", "תיאור"]]
                        .assign(**{'תמונה': add_image_paths(sl[sl['שמור מוצר'] == True], "Data/Products")})
                    )
                    st.session_state["step"] = 3           

def add_image_paths(df, images_path):
    width=100
    height=None
    image_column = []
    for product in df['שם מוצר']:
        image_filename = f"{product}.jpg"
        image_filepath = os.path.join(images_path, image_filename)
        
        if os.path.exists(image_filepath):
            # Construct the img tag with specified width and/or height
            image_html = f'<img src="data:image/jpg;base64,{base64.b64encode(open(image_filepath, "rb").read()).decode()}"'
            if width:
                image_html += f' width="{width}"'
            if height:
                image_html += f' height="{height}"'
            image_html += '>'
            image_column.append(image_html)
        else:
            image_column.append('No Image')  # Handle missing images

    return image_column

def download_list():
    # Display HTML table
    html_table = st.session_state["short list"].to_html(index=False,escape=False)
    st.write(html_table, unsafe_allow_html=True) 
    
    html_content = create_print_df()
    html_file_path = "shopping_list.html"

    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    pdf_buffer, error = convert_html_to_pdf(html_content)

    if not error:
        # Allow the user to download the PDF
        if st.download_button(label="הורד רשימה",data=pdf_buffer,file_name="shopping_list.pdf",mime="application/pdf"):
            st.session_state["step"] = 2
    else:
        st.error("Failed to generate PDF.")

def create_print_df():
    print_df = st.session_state["short list"].copy()
    print_df["שם מוצר"] = print_df["שם מוצר"].apply(reverse_text)
    print_df["תיאור"] = print_df["תיאור"].apply(reverse_text)
    print_df.columns = [col[::-1] for col in print_df.columns]
    print_df.fillna('', inplace=True)
    print_df = print_df[print_df.columns[::-1]]  # This reverses the column order

    print_table = print_df.to_html(index=False, escape=False)

    html_style = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap');
        body { font-family: 'Rubik', sans-serif!important; direction: rtl!important;}
        table { width: 100% ; border-collapse: collapse; }
        th, td {text-align: center; }
        img { width: 100px; }
    </style>
    """
    
    html_content = f"<html><head>{html_style}</head><body>{print_table}</body></html>"

    return html_content


def convert_html_to_pdf(html_content):
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer, pisa_status.err

def reverse_text(text):
    if isinstance(text, str):  # Check if the cell contains text
        return text[::-1]  # Reverse the text
    return text

###############################################################################


st.write(st.session_state["step"])

show_shopping_list_page()    
placeholder1 = st.container()
placeholder2 = st.container()
placeholder3 = st.container()
placeholder4 = st.container()

with placeholder4:
    if st.session_state['step'] > 0:
        if st.button("נקה הכל"):
            st.session_state["step"] = 0
            st.session_state["shopping list"] = None
            st.session_state["short list"] = None
            st.session_state["dog"] = None  
            placeholder1.empty()
            placeholder2.empty()
            placeholder3.empty()
            placeholder4.empty()

# if st.session_state['step'] == 0:
#     # placeholder1.empty()
#     # placeholder2.empty()
#     # placeholder3.empty()

if st.session_state['step'] == -1 :
    st.session_state["step"] = 0
    st.warning("לא נבחר כלב!")

if st.session_state['step'] == 1 :
    with placeholder1:
        create_list(st.session_state['dog'])

if st.session_state['step'] == 2 :
    with placeholder2: 
        present_list()

if st.session_state['step'] == 3 :
    with placeholder3: 
        download_list()
