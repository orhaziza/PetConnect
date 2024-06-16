import streamlit as st
import pandas as pd
import os
from datetime import datetime


if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.error("לא ניתן לגשת לעמוד ללא התחברות")
    st.stop()
st.set_page_config(page_title='Foster Homes', layout='wide')

# Load foster home data
foster_home_file_path = "Data/FosterHome.csv"
if not os.path.exists(foster_home_file_path):
    st.error("The foster home file does not exist.")
    st.stop()

foster_home_df = pd.read_csv(foster_home_file_path, encoding='Windows-1255')

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
with st.sidebar:
    selected = option_menu("בתים לבית אומנה", ["כל הטבלה", "מצא בית אומנה", "הוסף בית אומנה", "ערוך מסמך"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)

# Translate column names
foster_home_df_hebrew = foster_home_df.rename(columns=dict(zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))

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

    # Add foster home form or input fields here
    foster_home_id = st.text_input('מזהה בית אומנה')
    foster_name = st.text_input('שם בית אומנה')
    address = st.text_area('כתובת')
    house_size = st.selectbox('גודל הבית', [''] + list(foster_home_df['HouseSize'].unique()))
    contact_info = st.text_input('פרטי קשר')
    backyard = st.selectbox('חצר', [''] + list(foster_home_df['Backyard'].unique()))
    near_dog_park = st.selectbox('קרוב לגן כלבים', [''] + list(foster_home_df['nearDogPark'].unique()))
    house_members = st.text_input('חברי בית')
    availability_at_home = st.selectbox('זמינות בבית', [''] + list(foster_home_df['AvailabilityAtHome'].unique()))
    children_friendly = st.selectbox('ידידותי לילדים', [''] + list(foster_home_df['ChildrenFriendly'].unique()))
    animal_friendly = st.selectbox('ידידותי לכלבים', [''] + list(foster_home_df['AnimalFriendly'].unique()))
    max_capacity = st.number_input('קיבולת מקסימלית', min_value=0)
    allowed_at_property = st.selectbox('מותר בנכס', [''] + list(foster_home_df['allowedAtProperty'].unique()))
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
        foster_home_df.to_csv(foster_home_file_path, index=False, encoding='Windows-1255')
        st.success('הבית אומנה נשמר בהצלחה!')


# Sidebar logout button
if st.sidebar.button("Log Out"):
    st.session_state['logged_in'] = False
    st.experimental_rerun()



