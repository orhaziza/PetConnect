import matplotlib.pyplot as plt
import io
from io import BytesIO
import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import background
import base64


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
        st.write("not yet")

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
                st.write(st.session_state["short list"].to_html(escape=False), unsafe_allow_html=True)
                # image_bytes = html_to_image(st.session_state["short list"].to_html(escape=False))
                # st.image(image_bytes)
                # st.download_button(
                #     "Download Shopping List as Image",
                #     data=image_bytes,
                #     file_name="shopping_list.png",
                #     mime="image/png"
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


def html_to_image(html_content, output_file="output.png"):
    fig, ax = plt.subplots(figsize=(2, 2))  # Adjust figsize as needed
    ax.axis('off')
    ax.text(0.5, 0.5, html_content, va='center', ha='center', wrap=True)
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return buf


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
