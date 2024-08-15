import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
import background

FILES_DIR = 'Data/FosterHomes/'

    # Ensure the directory exists
if not os.path.exists(FILES_DIR):
    os.makedirs(FILES_DIR)
        
def save_file(foster_home_id, uploaded_file):
    with open(os.path.join(FILES_DIR, f'{foster_home_id}_{uploaded_file.name}'), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f'קובץ {uploaded_file.name} נשמר בהצלחה!')

def save_foster_home_to_csv(foster_home_df_hebrew, new_foster_home_df, csv_file_path):
    # Append the new data to the existing DataFrame
    updated_df = pd.concat([foster_home_df_hebrew, new_foster_home_df], ignore_index=True)

    # Save to CSV or the desired file
    updated_df.to_csv(csv_file_path, index=False, encoding='utf-8')

    return updated_df

def delete_file(file_name):
    os.remove(os.path.join(FILES_DIR, file_name))
    st.success(f'קובץ {file_name} נמחק בהצלחה!')

def show_foster_homes_page():
    st.set_page_config(page_title='Foster Homes', layout='wide')
    background.add_bg_from_local('./static/background3.png')
    background.load_css('styles.css')
    
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()

    background.insert_logo("בתי אומנה")

    url = "https://docs.google.com/spreadsheets/d/1u37tuMp9TI2QT6yyT0fjpgn7wEGlXvYYKakARSGRqs4/edit?usp=sharing"
        
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
    #     selected = option_menu("בתים לבית אומנה", ["כל הטבלה", "מצא בית אומנה", "הוסף בית אומנה", "מסמכים"], icons=["file", "search", "file", "upload"], menu_icon="menu", default_index=0)

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
        menu_title="",  # Required
        options=["ערוך מסמך","הוסף בית אומנה","מצא בית אומנה","כל הטבלה"],  # Required
        icons=["upload", "file", "search", "file"],  # Optional
        menu_icon="menu",  # Optional
        default_index=3,  # Optional
        orientation="horizontal",  # To place the menu in the center horizontally
        styles=background.styles,
    )

    # Translate column names
    foster_home_df_hebrew = foster_home_df.rename(columns=dict(
        zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))

    # Display different pages based on selected option
    if selected == "כל הטבלה":
        st.dataframe(foster_home_df_hebrew)
        st.write(foster_home_df_hebrew.dtypes)


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
        # Input fields with matching data types
        foster_home_id = st.number_input('מזהה בית אומנה', min_value=0, format="%d")  # int64
        foster_name = st.text_input('שם בית אומנה')  # object
        address = st.text_area('כתובת')  # object
    
        house_size_options = ['גדול', 'בינוני'] + list(foster_home_df_hebrew['גודל הבית'].unique()) if 'גודל הבית' in foster_home_df_hebrew.columns else []
        house_size = st.selectbox('גודל הבית', house_size_options)  # object
    
        contact_info = st.number_input('פרטי קשר', min_value=0, format="%d")  # int64
    
        backyard = st.checkbox('חצר', value=False)  # bool
        near_dog_park = st.checkbox('קרוב לגן כלבים', value=False)  # bool
    
        house_members = st.number_input('חברי בית', min_value=0, format="%d")  # int64
    
        availability_at_home_options = [''] + list(foster_home_df_hebrew['זמינות בבית'].unique()) if 'זמינות בבית' in foster_home_df_hebrew.columns else []
        availability_at_home = st.selectbox('זמינות בבית', availability_at_home_options)  # object
    
        children_friendly = st.checkbox('ידידותי לילדים', value=False)  # bool
        animal_friendly = st.checkbox('ידידותי לכלבים', value=False)  # bool
    
        max_capacity = st.number_input('קיבולת מקסימלית', min_value=0, format="%d")  # int64
    
        allowed_at_property = st.checkbox('מותר בנכס', value=False)  # bool
        
        allergies = st.checkbox('אלרגיות', value=False)  # bool
    
        is_mobile = st.checkbox('נייד', value=False)  # bool
    
        energy_level = st.slider('רמת אנרגיה', min_value=1, max_value=5)  # object but needs conversion to int
    
        past_fosters = st.checkbox('אומנויות קודמות', value=False)  # bool
        past_experience = st.checkbox('ניסיון קודם', value=False)  # bool
    
        documents = st.text_area('מסמכים')  # float64, consider changing to object

        # When the user clicks save, store the data in the DataFrame
        if st.button('שמור בית אומנה'):
            new_foster_home = {
                'מזהה בית אומנה': foster_home_id,
                'שם בית אומנה': foster_name,
                'כתובת': address,
                'גודל הבית': house_size,
                'פרטי קשר': contact_info,
                'חצר': backyard,
                'NearDogPark': near_dog_park,
                'חברי בית': house_members,
                'זמינות בבית': availability_at_home,
                'ידידותי לילדים': children_friendly,
                'ידידותי לכלבים': animal_friendly,
                'קיבולת מקסימלית': max_capacity,
                'AllowedAtProperty': allowed_at_property,
                'Allergies': allergies,
                'נייד': is_mobile,
                'רמת אנרגיה': str(energy_level),  # Convert to string if kept as object
                'PastFosters': past_fosters,
                'PastExperience': past_experience,
                'Documents': documents  # May need conversion depending on original data type
            }

            # Create a new DataFrame from the input
            new_foster_home_df = pd.DataFrame([new_foster_home])

            # Define the CSV file path (modify this path as needed)
            csv_file_path = 'Data/FosterHome.csv'

            # Save the new foster home to the CSV
            try:
                foster_home_df_hebrew = save_foster_home_to_csv(foster_home_df_hebrew, new_foster_home_df, csv_file_path)
                st.success('בית אומנה חדש נשמר בהצלחה!')
                st.balloons()
                st.print("XXXX")
                # Ensure the file is added to Git
                os.system(f'git add {csv_file_path}')
                os.system('git commit -m "Update foster home data with a new entry"')
                os.system('git push')
                
            except Exception as e:
                st.error(f"Error saving data: {e}")



    elif selected == "ערוך מסמך":
        st.title('מסמכים')

        foster_home_id = st.selectbox('Select Foster Home ID', foster_home_df_hebrew['מזהה בית אומנה'])

        if foster_home_id:
            st.subheader(f'מסמכים של {foster_home_id}')

            files = [f for f in os.listdir(FILES_DIR) if f.startswith(f'{foster_home_id}_')]
            if files:
                st.write('קבצים שיש במערכת ')
                for file_name in files:
                    st.write(file_name)
                    with open(os.path.join(FILES_DIR, file_name), "rb") as file:
                        btn = st.download_button(
                            label=f"הורד {file_name}",
                            data=file,
                            file_name=file_name,
                            mime='application/octet-stream'
                        )
                    if st.button(f'מחק {file_name}', key=f'מחק_{file_name}'):
                        delete_file(file_name)

            uploaded_file = st.file_uploader('העלאת קובץ', type='pdf')
            if uploaded_file is not None:
                if uploaded_file.name:
                    save_file(foster_home_id, uploaded_file)
                else:
                    st.error('אין שם לקובץ ')

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

show_foster_homes_page()

