import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import io
import os
import background
import base64
from io import BytesIO
import weasyprint
from xhtml2pdf import pisa
import background
import gspread
from google.oauth2.service_account import Credentials
from streamlit_gsheets import GSheetsConnection

# Directory for storing adopter files
url = "https://docs.google.com/spreadsheets/d/14e7lQDBov_c8iaRe7N5AXmMmAW5FzF2NilCTjq7LcAo/edit?usp=sharing"

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
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection, ttl=0.5)
    return conn.read(spreadsheet=url)
    



st.set_page_config(page_title='Shopping List', layout='wide')

items_file_path = "Data/Shopping List.csv"
items_df = pd.read_csv(items_file_path, encoding='utf-8')
dogs_file_path = "Data/Dogs.csv"
dog_df = pd.read_csv(dogs_file_path, encoding='utf-8')
dog_df = dog_df[dog_df['AdoptionStatus'] == 0]
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


def add_product_to_google_sheet(new_product):
    worksheet = open_google_sheet()

    # Replace NaN and infinite values before saving
    def sanitize_value(value):
        if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
            return ''
        return value

    # Append the new product data as a new row in the sheet
    worksheet.append_row([
        sanitize_value(new_product['ProductCategory']),
        sanitize_value(new_product['ProductID']),
        sanitize_value(new_product['ProductName']),
        sanitize_value(new_product['ProductSize']),
        sanitize_value(new_product['ProductSizeUnit']),
        sanitize_value(new_product['Age']),
        sanitize_value(new_product['Breed']),
        sanitize_value(new_product['Gender']),
        sanitize_value(new_product['DogSize']),
        sanitize_value(new_product['EnergyLevel']),
        sanitize_value(new_product['PottyTrained']),
        sanitize_value(new_product['ProductPhoto']),
        sanitize_value(new_product['Description']),
    ])  # Add the new product's data

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
        options=["הוסף מוצר", "צור רשימה לכלב"],  # Added new option for the table with scores
        icons=["file", "search"],  # Optional
        menu_icon="menu",  # Optional
        default_index=1,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
        )
    
    if selected == "צור רשימה לכלב":
        col3, col1, col2, col4 = st.columns([0.5, 4.5, 1, 0.5])
        
        with col1:
            st.session_state['dog'] = st.selectbox(label='',options=dog_df['Name'].unique(),index=None, placeholder = "בחר כלב")
        with col2:
            if st.button("צור רשימה"):
                if st.session_state['dog'] != None:
                    st.session_state["step"] = 1
                    st.session_state["shopping list"] = None
                    st.session_state["short list"] = None
                else:
                    st.session_state["step"] = -1
                    st.session_state["shopping list"] = None
                    st.session_state["short list"] = None
                    
            
    elif selected == "הוסף מוצר":
        st.session_state["step"] = 0
        st.subheader('הוסף מוצר חדש')

        # Input fields for the product form
        product_category = st.text_input('קטגוריה מוצר')
        product_id = st.text_input('מזהה מוצר')
        product_name = st.text_input('שם מוצר')
        product_size = st.text_input('גודל מוצר')
        product_size_unit = st.text_input('יחידות מידה')
        age = st.number_input('גיל', min_value=0, step=1)
        breed = st.text_input('גזע')
        gender = st.selectbox('מין', ['זכר', 'נקבה'])
        dog_size = st.selectbox('גודל כלב', ['XS', 'S', 'M', 'L', 'XL'])
        energy_level = st.selectbox('רמת אנרגיה', ['נמוכה', 'בינונית', 'גבוהה'])
        potty_trained = st.checkbox('מחונך לצרכים')
        product_photo = st.file_uploader('תמונה מוצר', type=['jpg''])
        description = st.text_area('תיאור')

    # Save the new product data
        if st.button('שמור מוצר'):
            new_product = {
            'ProductCategory': product_category,
            'ProductID': product_id,
            'ProductName': product_name,
            'ProductSize': product_size,
            'ProductSizeUnit': product_size_unit,
            'Age': age,
            'Breed': breed,
            'Gender': gender,
            'DogSize': dog_size,
            'EnergyLevel': energy_level,
            'PottyTrained': potty_trained,
            'ProductPhoto': product_photo.name if product_photo else '',
            'Description': description,
            }

            try:
                # Add the new product record to the Google Sheet
                add_product_to_google_sheet(new_product)
                st.success('מוצר חדש נשמר בהצלחה!')
                st.balloons()  # Show the balloons animation for success
            except Exception as e:
                st.error(f'Error saving product: {e}')
        
def create_list(dog):
    df = dog_df.loc[dog_df['Name'] == dog].reset_index()
    categories = items_df['קטגוריה'].unique()
    sl = items_df.iloc[:0,:].copy()
    if not (df["Size"][0]=='XS' or df["Size"][0]=='S' or df["Size"][0]=='M' or df["Size"][0]=='L' or df["Size"][0]=='XL'):
        st.warning('Dog has NO size!')    
    for c in categories:
        if c=="גורים":
            if df["Age"][0]<12:
                category_products = items_df[items_df['קטגוריה'] == c]
                sl = pd.concat([sl, category_products], ignore_index=True) 
        else:    
            category_products = items_df[items_df['קטגוריה'] == c]
            sl = pd.concat([sl, category_products[category_products['גודל הכלב'] == df["Size"][0]]], ignore_index=True) 

    sl['סמן'] = True
    st.session_state["shopping list"] = sl
    st.session_state["step"] = 2

def html_to_pdf_stream(html_content):
    # Convert HTML to PDF and return as a byte stream
    pdf = weasyprint.HTML(string=html_content).write_pdf()
    return io.BytesIO(pdf)


def convert_html_to_pdf(html_content):
    pdf_buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.StringIO(html_content), dest=pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer, pisa_status.err


def present_list():
    sl = st.data_editor(st.session_state["shopping list"])
    st.session_state["download"] = False

    col1, col2 ,col3, col4=  st.columns([1, 2, 8, 2])
    if not st.session_state["shopping list"].empty:
        with col1:
            if st.button("שמור"):
                st.session_state["short list"] = (
                    sl[sl['סמן'] == True]
                    .loc[:, ["שם מוצר", "תיאור"]]
                    .assign(**{'Product Image': add_image_paths(sl[sl['סמן'] == True], "Data/Products")})
                )
                # Display HTML table
                html_table = st.session_state["short list"].to_html(escape=False)
                st.write(html_table, unsafe_allow_html=True)                
                
                html_style = """
                    <style>
                    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap');
                    body { font-family: 'Rubik', sans-serif; direction: rtl; }
                    table { width: 100%; border-collapse: collapse; }
                    th, td { border: 1px solid black; padding: 10px; text-align: right; }
                    img { width: 100px; }
                </style>
                """
                
                html_file_path = "shopping_list.html"
                html_content = f"<html><head>{html_style}</head><body>{html_table}</body></html>"
                
                with open(html_file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                

                pdf_buffer, error = convert_html_to_pdf(html_content)

                if not error:
                    # Allow the user to download the PDF
                    st.download_button(
                        label="Download PDF",
                        data=pdf_buffer,
                        file_name="shopping_list.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Failed to generate PDF.")


                # pdf_stream = html_to_pdf_stream(html_content)

                # st.markdown(weasyprint.__version__)
                # st.download_button(
                #     label="Download PDF",
                #     data=pdf_stream,
                #     file_name='shopping_list.pdf',
                #     mime="application/pdf"
                # )

        with col4:
            if st.button("נקה"):
                st.session_state["step"] = 0
                st.session_state["shopping list"] = None
                st.session_state["short list"] = None
                st.session_state["dog"] = None
                placeholder3.empty()
    

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


###############################################################################

if "step" not in st.session_state:
    st.session_state["step"] = 0

show_shopping_list_page()    
placeholder1 = st.empty()
placeholder2 = st.empty()
placeholder3 = st.empty()


if st.session_state['step'] == -1 :
    st.session_state["step"] = 0
    st.warning("לא נבחר כלב!")

if st.session_state['step'] == 1 :
    with placeholder2.container():
        create_list(st.session_state['dog'])

if st.session_state['step'] == 2 :
    with placeholder3.container():
        present_list()

if st.session_state['step'] == 0:
    placeholder1.empty()
    placeholder2.empty()
    placeholder3.empty()
