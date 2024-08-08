import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

def show_foster_homes_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()
    st.set_page_config(page_title='Foster Homes', layout='wide')
    con1 = st.container()
    with con1:
        col1, col2 = st.columns([4, 1])  # Adjust column ratios as needed
        with col1:
            st.markdown('<h1 class="rtl">Foster Homes</h1>', unsafe_allow_html=True)
        with col2:
            st.image("Data/Logo.png", width=100)



    # Load foster home data
    foster_home_file_path = "Data/FosterHome.csv"
    if not os.path.exists(foster_home_file_path):
        st.error("The foster home file does not exist.")
        st.stop()

    foster_home_df = pd.read_csv(foster_home_file_path, encoding='utf-8')


    # Define Hebrew column names for foster homes
    hebrew_columns_foster_homes = {
        'FosterHomeID': 'מזהה בית אומנה',
        'FosterName': 'שם בית אומנה',
        'Address': 'כתובת',
        'HouseSize': 'גודל הבית',
        'Contactinfomation': 'פרטי קשר',
        'Backyard': 'חצר',
        'nearDogPark': 'קרוב לגן כלבים',
        'HouseMembers': 'חברי בית',
        'AvailabilityAtHome': 'זמינות בבית',
        'ChildrenFriendly': 'ידידותי לילדים',
        'AnimalFriendly': 'ידידותי לכלבים',
        'MaximumCapacity': 'קיבולת מקסימלית',
        'allowedAtProperty': 'מותר בנכס',
        'allergies': 'אלרגיות',
        'IsMobile': 'נייד',
        'EnergyLevel': 'רמת אנרגיה',
        'pastFosters': 'אומנויות קודמות',
        'pastExperience': 'ניסיון קודם',
        'documents': 'מסמכים',
    }

    # Define the menu options
    # with st.sidebar:
    #     selected = option_menu("בתים לבית אומנה", ["כל הטבלה", "מצא בית אומנה", "הוסף בית אומנה", "ערוך מסמך"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)

    st.markdown(
        """
        <style>
        .option-menu-container {
            display: flex;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # # Use st.columns to create four equally sized columns
    # col1, col2, col3, col4 = st.columns(4)

    # # Button 1 in the first column
    # with col1:
    #     if st.button("כלבים 🐶"):
    #         st.switch_page("pages/Dogs.py")

    # # Button 2 in the second column
    # with col2:
    #     if st.button("בתי אומנה 🏠"):
    #         st.switch_page("pages/FosterHome.py")

    # # Button 3 in the third column
    # with col3:
    #     if st.button("אומצים 👤"):
    #         st.switch_page("pages/adopters.py")

    # # Button 4 in the fourth column
    # with col4:
    #     if st.button("בקשות 📁"):
    #         st.switch_page("pages/Applications.py")

    # Create the option menu inside a div with the custom class
    selected = option_menu(
        menu_title="בתים לאומנה",  # Required
        options=["כל הטבלה", "מצא בית אומנה", "הוסף בית אומנה", "ערוך מסמך"],  # Required
        icons=["file", "search", "file", "upload"],  # Optional
        menu_icon="menu",  # Optional
        default_index=0,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles={
            "container": {"class": "option-menu-container"}
        }
    )

    # Translate column names
    foster_home_df_hebrew = foster_home_df.rename(columns=dict(
        zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))

    # Display different pages based on selected option
    if selected == "כל הטבלה":
        st.dataframe(foster_home_df_hebrew)

    elif selected == "מצא בית אומנה":
        st.subheader('מצא בית אומנה')

        # Create search filters for foster homes
        col1, col2, col3 = st.columns(3)

        with col1:
            foster_name = st.text_input('שם בית אומנה')
        with col2:
            house_size = st.selectbox('גודל הבית', [''] + list(foster_home_df['HouseSize'].unique()))
        with col3:
            children_friendly = st.selectbox('ידידותי לילדים', [''] + list(foster_home_df['ChildrenFriendly'].unique()))

        # Apply search filters
        filtered_foster_homes = foster_home_df_hebrew[
            (foster_home_df_hebrew['שם בית אומנה'].str.contains(foster_name, na=False, case=False)) &
            (foster_home_df_hebrew['גודל הבית'].isin([house_size]) if house_size else True) &
            (foster_home_df_hebrew['ידידותי לילדים'].isin([children_friendly]) if children_friendly else True)
            ]

        st.dataframe(filtered_foster_homes)

    elif selected == "הוסף בית אומנה":
        st.subheader('הוסף בית אומנה')

        foster_home_id = st.text_input('מזהה בית אומנה')
        foster_name = st.text_input('שם בית אומנה')
        address = st.text_area('כתובת')
        house_size = st.selectbox('גודל הבית', ['גדול', 'בינוני'] + list(foster_home_df_hebrew['גודל הבית'].unique()) if 'גודל הבית' in foster_home_df_hebrew.columns else [])
        contact_info = st.text_input('פרטי קשר')
        backyard = st.selectbox('חצר', ['True', 'False'] + list(foster_home_df_hebrew['חצר'].unique()) if 'חצר' in foster_home_df_hebrew.columns else [])
        near_dog_park = st.selectbox('קרוב לגן כלבים', ['True', 'False'] + list(foster_home_df_hebrew['קרוב לגן כלבים'].unique()) if 'קרוב לגן כלבים' in foster_home_df_hebrew.columns else [])
        house_members = st.text_input('חברי בית')
        availability_at_home = st.selectbox('זמינות בבית', [''] + list(foster_home_df_hebrew['זמינות בבית'].unique()) if 'זמינות בבית' in foster_home_df_hebrew.columns else [])
        children_friendly = st.selectbox('ידידותי לילדים', ['True', 'False'] + list(foster_home_df_hebrew['ידידותי לילדים'].unique()) if 'ידידותי לילדים' in foster_home_df_hebrew.columns else [])
        animal_friendly = st.selectbox('ידידותי לכלבים', ['True', 'False'] + list(foster_home_df_hebrew['ידידותי לכלבים'].unique()) if 'ידידותי לכלבים' in foster_home_df_hebrew.columns else [])
        max_capacity = st.number_input('קיבולת מקסימלית', min_value=0)
        allowed_at_property = st.selectbox('מותר בנכס', ['True', 'False'] + list(foster_home_df_hebrew['מותר בנכס'].unique()) if 'מותר בנכס' in foster_home_df_hebrew.columns else [])
        allergies = st.text_area('אלרגיות')
        is_mobile = st.checkbox('נייד')
        energy_level = st.slider('רמת אנרגיה', min_value=1, max_value=5)
        past_fosters = st.text_area('אומנויות קודמות')
        past_experience = st.text_area('ניסיון קודם')
        documents = st.text_area('מסמכים')

        if st.button('שמור בית אומנה'):
            # Save foster home data to CSV or database
            new_foster_home = {
                'מזהה בית אומנה': foster_home_id,
                'שם בית אומנה': foster_name,
                'כתובת': address,
                'גודל הבית': house_size,
                'פרטי קשר': contact_info,
                'חצר': backyard,
                'קרוב לגן כלבים': near_dog_park,
                'חברי בית': house_members,
                'זמינות בבית': availability_at_home,
                'ידידותי לילדים': children_friendly,
                'ידידותי לכלבים': animal_friendly,
                'קיבולת מקסימלית': max_capacity,
                'מותר בנכס': allowed_at_property,
                'אלרגיות': allergies,
                'נייד': is_mobile,
                'רמת אנרגיה': energy_level,
                'אומנויות קודמות': past_fosters,
                'ניסיון קודם': past_experience,
                'מסמכים': documents
            }
            foster_home_df = foster_home_df.append(new_foster_home, ignore_index=True)
            foster_home_df.to_csv(foster_home_file_path, index=False, encoding='utf-8')
            st.success('הבית אומנה נשמר בהצלחה!')

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

show_foster_homes_page()

