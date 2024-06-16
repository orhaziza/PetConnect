# Pages/FosterHome.py
import streamlit as st
import pandas as pd
import os

def show_foster_homes_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("Cannot access the page without logging in.")
        st.stop()

    st.title("Manage Foster Homes")

    # Load foster home data
    foster_home_file_path = "Data/FosterHome.csv"
    if not os.path.exists(foster_home_file_path):
        st.error("The foster home data file does not exist.")
        return

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

    # Translate column names
    foster_home_df_hebrew = foster_home_df.rename(columns=dict(zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))

    # Define the menu options
    with st.sidebar:
        selected = st.selectbox("Select an option", ["All Foster Homes", "Find a Foster Home", "Add a Foster Home", "Edit Document"])

    # Display different pages based on selected option
    if selected == "All Foster Homes":
        st.dataframe(foster_home_df_hebrew)

    elif selected == "Find a Foster Home":
        st.subheader('Find a Foster Home')

        # Create search filters for foster homes
        col1, col2, col3 = st.columns(3)

        with col1:
            foster_name = st.text_input('Foster Home Name')
        with col2:
            house_size = st.selectbox('House Size', [''] + list(foster_home_df['HouseSize'].unique()))
        with col3:
            children_friendly = st.selectbox('Children Friendly', [''] + list(foster_home_df['ChildrenFriendly'].unique()))

        # Apply search filters
        filtered_foster_homes = foster_home_df_hebrew[
            (foster_home_df_hebrew['שם בית אומנה'].str.contains(foster_name, na=False, case=False)) &
            (foster_home_df_hebrew['גודל הבית'].isin([house_size]) if house_size else True) &
            (foster_home_df_hebrew['ידידותי לילדים'].isin([children_friendly]) if children_friendly else True)
        ]

        st.dataframe(filtered_foster_homes)

    elif selected == "Add a Foster Home":
        st.subheader('Add a New Foster Home')

        # Add foster home form or input fields here
        with st.form(key='foster_home_form'):
            foster_home_id = st.text_input('Foster Home ID')
            foster_name = st.text_input('Foster Home Name')
            address = st.text_area('Address')
            house_size = st.selectbox('House Size', list(foster_home_df['HouseSize'].unique()))
            contact_info = st.text_input('Contact Information')
            backyard = st.selectbox('Backyard', list(foster_home_df['Backyard'].unique()))
            near_dog_park = st.selectbox('Near Dog Park', list(foster_home_df['nearDogPark'].unique()))
            house_members = st.text_input('House Members')
            availability_at_home = st.selectbox('Availability at Home', list(foster_home_df['AvailabilityAtHome'].unique()))
            children_friendly = st.selectbox('Children Friendly', list(foster_home_df['ChildrenFriendly'].unique()))
            animal_friendly = st.selectbox('Animal Friendly', list(foster_home_df['AnimalFriendly'].unique()))
            max_capacity = st.number_input('Maximum Capacity', min_value=0)
            allowed_at_property = st.selectbox('Allowed at Property', list(foster_home_df['allowedAtProperty'].unique()))
            allergies = st.text_area('Allergies')
            is_mobile = st.checkbox('Is Mobile')
            energy_level = st.slider('Energy Level', min_value=1, max_value=5)
            past_fosters = st.text_area('Past Fosters')
            past_experience = st.text_area('Past Experience')
            documents = st.text_area('Documents')

            submit_button = st.form_submit_button(label='Save Foster Home')

        if submit_button:
            new_foster_home = {
                'FosterHomeID': foster_home_id,
                'FosterName': foster_name,
                'Address': address,
                'HouseSize': house_size,
                'Contactinfomation': contact_info,
                'Backyard': backyard,
                'nearDogPark': near_dog_park,
                'HouseMembers': house_members,
                'AvailabilityAtHome': availability_at_home,
                'ChildrenFriendly': children_friendly,
                'AnimalFriendly': animal_friendly,
                'MaximumCapacity': max_capacity,
                'allowedAtProperty': allowed_at_property,
                'allergies': allergies,
                'IsMobile': is_mobile,
                'EnergyLevel': energy_level,
                'pastFosters': past_fosters,
                'pastExperience': past_experience,
                'documents': documents,
            }
            foster_home_df = foster_home_df.append(new_foster_home, ignore_index=True)
            foster_home_df.to_csv(foster_home_file_path, index=False, encoding='Windows-1255')
            st.success('Foster home saved successfully!')

    elif selected == "Edit Document":
        st.subheader('Edit Document')
        # Implement document editing logic here
