import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu
        
def show_dogs_page():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error('<div style="direction: rtl;">לא ניתן לגשת לעמוד ללא התחברות</div>', unsafe_allow_html=True)
        st.stop()

    st.set_page_config(page_title='Dogs', layout='wide')
    # Container for the logo and title
    con1 = st.container()
    with con1:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.title("Dogs Page")
        with col2:
            st.image("Data/Logo.png", width=120)


    # Creating Dataframe from csv
    dogs_file_path = "Data/Dogs.csv"
    dog_df = pd.read_csv(dogs_file_path, encoding='utf-8')


    foster_home_file_path = "Data/FosterHome.csv"
    if not os.path.exists(foster_home_file_path):
        st.error("The foster home file does not exist.")
        st.stop()

    foster_home_df = pd.read_csv(foster_home_file_path, encoding='utf-8')

    # Load the foster home data
    foster_home_file_path = "Data/FosterHome.csv"
    if not os.path.exists(foster_home_file_path):
        st.error("The foster home file does not exist.")
        st.stop()

    foster_home_df = pd.read_csv(foster_home_file_path, encoding='utf-8')

    # Defining Hebrew names
    # Define Hebrew column names
    hebrew_columns_dogs = {
    'DogID': 'מזהה כלב',
    'Name': 'שם',
    'DateOfBirth': 'תאריך לידה',
    'Age': 'גיל',
    'Breed': 'זן',
    'Weight': 'משקל',
    'Size': 'גודל',
    'Gender': 'מין',
    'RescueDate': 'תאריך חילוץ',
    'Rabies_Done': 'חיסון כלבת',
    'Hexagonal_1': 'חיסון משושה 1',
    'Hexagonal_2': 'חיסון משושה 2',
    'Hexagonal_3': 'חיסון משושה 3',
    'Hexagonal_Done': 'חיסון משושה',
    'Spayed': 'מעוקר',
    'De-worm': 'טיפול נגד תולעים',
    'Children_Friendly': 'ידידותי לילדים',
    'AnimalFriendly': 'ידידותי לכלבים',
    'HealthStatus': 'מצב הכלב',
    'EnergyLevel': 'רמת האנרגיה',
    'PhotographStatus': 'סטטוס הצילום',
    'AdoptionStatus': 'סטטוס אימוץ',
    'AdopterID': 'מזהה מאמץ',
    'PottyTrained': 'מחונך לצרכים',
    'AdoptionName': 'שם המאומץ'
    # Add more column name translations as needed
}

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
        'allowedAtProperty': 'מורשה ברחם',
        'allergies': 'אלרגיות',
        'IsMobile': 'ניידות',
        'EnergyLevel': 'רמת אנרגיה',
        'pastFosters': 'כולל אמנה קודמת',
        'pastExperience': 'ניסיון קודם',
        'documents': 'מסמכים',
    }

    foster_home_df_hebrew = foster_home_df.rename(columns=dict(
        zip(foster_home_df.columns, [hebrew_columns_foster_homes.get(col, col) for col in foster_home_df.columns])))

    
    selected = option_menu(
        menu_title='<div style="direction: rtl;">כלבים</div>',  # Required
        options=["כל הטבלה", "מצא כלב", "הוסף כלב", "ערוך תמונה", "מצא בית אומנה"],  # Required
        icons=["file", "search", "file", "upload", "search"],  # Optional
        menu_icon="menu",  # Optional
        default_index=0,  # Optional
        orientation="horizontal"  # To place the menu in the center horizontally
    )

    images_folder = "DogsPhotos"
    # Translate English column names to Hebrew
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]

    # Display DataFrame with Hebrew column names
    file_path = "Data/Dogs.csv"

    # Check if the file exists
    if not os.path.exists(file_path):
        st.error("The file does not exist.")
        st.stop()

        # Read CSV file
    dog_df = pd.read_csv(file_path, encoding='utf-8')
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
    dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

    # Display the editable table

    # Button to save changes

    if selected == "כל הטבלה":
        edited_df = st.data_editor(dog_df_hebrew, use_container_width=True, height=400)
        if st.button("Save Changes"):
            # Rename columns back to English for saving
            edited_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
            # Save the edited dataframe to the CSV file
            edited_df.to_csv(file_path, index=False, encoding='utf-8')
            st.success("Changes saved successfully!")

    if selected == "מצא כלב":
        st.subheader('<div style="direction: rtl;">מצא כלב</div>', unsafe_allow_html=True)



        # Create search filters in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            breed = st.selectbox('גזע', options=[''] + list(dog_df['breed'].unique()))
        with col2:
            age = st.slider('גיל', min_value=0, max_value=int(dog_df['age'].max()), value=(0, int(dog_df['age'].max())))
        with col3:
            size = st.selectbox('גודל', options=[''] + list(dog_df['size'].unique()))
        with col4:
            gender = st.selectbox('מין', options=[''] + list(dog_df['gender'].unique()))

        # Apply search filters
        filtered_df = dog_df_hebrew[
            (dog_df['breed'].isin([breed]) if breed else True) &
            (dog_df['age'] >= age[0]) & (dog_df['age'] <= age[1]) &
            (dog_df['size'].isin([size]) if size else True) &
            (dog_df['gender'].isin([gender]) if gender else True)
            ]

        st.write(filtered_df)

    if selected == "הוסף כלב":
        st.subheader('הוסף כלב חדש')

        with st.form(key='insert_form'):
            DogID = st.text_input('מזהה כלב')
            name = st.text_input('שם')
            age = st.number_input('גיל', min_value=0, max_value=100, step=1)
            breed = st.text_input('גזע')
            size = st.selectbox('גודל', ['קטן', 'בינוני', 'גדול'])
            gender = st.selectbox('מין', ['זכר', 'נקבה'])
            rescueDate = st.date_input('תאריך חילוץ')
            vaccine_1 = st.checkbox('חיסון כלבת')
            vaccine_2 = st.checkbox('חיסון משושה')
            isSpay = st.checkbox('מעוקר')
            childrenFirendly = st.checkbox('ידידותי לילדים')
            animalFirendly = st.checkbox('ידידותי לכלבים')
            healthStatus = st.text_input('מצב הכלב')
            energylevel = st.selectbox('רמת האנרגיה', ['נמוכה', 'בינונית', 'גבוהה'])
            photographStatus = st.selectbox('סטטוס הצילום', ['ממתין לצילום', 'צילום הושלם'])
            adoptionStatus = st.selectbox('סטטוס אימוץ', ['זמין לאימוץ', 'נאסף'])
            adopterID = st.text_input('מזהה מאמץ')
            pottyTrained = st.checkbox('מחונך לצרכים')

            submit_button = st.form_submit_button(label='הוסף כלב')

        if submit_button:
            new_dog = {
                'DogID': DogID,
                'name': name,
                'age': age,
                'breed': breed,
                'size': size,
                'gender': gender,
                'rescueDate': rescueDate.strftime('%Y-%m-%d'),
                'vaccine_1': vaccine_1,
                'vaccine_2': vaccine_2,
                'isSpay': isSpay,
                'childrenFirendly': childrenFirendly,
                'animalFirendly': animalFirendly,
                'healthStatus': healthStatus,
                'energylevel': energylevel,
                'photographStatus': photographStatus,
                'adoptionStatus': adoptionStatus,
                'adopterID': adopterID,
                'pottyTrained': pottyTrained,
            }
            dog_df = dog_df.append(new_dog, ignore_index=True)
            dog_df.to_csv(file_path, index=False, encoding='Windows-1255')
            st.success('הכלב הוסף בהצלחה!')

    if selected == "ערוך תמונה":
        st.header('הוספת תמונה לכלבים ללא תמונה')

        # Filter dogs without images
        dogs_without_images = dog_df[
            ~dog_df['DogID'].astype(str).apply(lambda x: os.path.exists(os.path.join(images_folder, f"{x}.png")))]

        if not dogs_without_images.empty:
            st.write('כלבים ללא תמונות:')
            st.dataframe(
                dogs_without_images.rename(columns=dict(zip(dogs_without_images.columns, hebrew_column_names))))

            # Dropdown menu to select a dog to upload an image for
            selected_dog_name_for_image = st.selectbox('בחר כלב להוספת תמונה', dogs_without_images['name'].tolist())
            selected_dog_id_for_image = \
            dogs_without_images[dogs_without_images['name'] == selected_dog_name_for_image]['DogID'].iloc[0]

            uploaded_file_for_dog = st.file_uploader("png הכנס תמונה של הכלב עם סיומת", type="png")

            if st.button('הוסף תמונה'):
                if uploaded_file_for_dog is not None:
                    image_path_for_dog = os.path.join(images_folder, f"{selected_dog_id_for_image}.png")
                    with open(image_path_for_dog, "wb") as f:
                        f.write(uploaded_file_for_dog.getvalue())

                    st.success(f'תמונה לכלב {selected_dog_name_for_image} הוספה בהצלחה!')
        else:
            st.write('לכל הכלבים במסד הנתונים קיימת תמונה')


    elif selected == "מצא בית אומנה":
        # Search functionality for foster homes
        st.subheader('מצא בית אומנה')

        # Create search filters for foster homes
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            foster_name = st.text_input('שם בית אומנה')
            children_friendly = st.checkbox('ידידותי לילדים')
            animal_friendly = st.checkbox('ידידותי לכלבים')
        with col2:
            house_size = st.selectbox('גודל הבית', ['קטן', 'בינוני', 'גדול'])
            backyard = st.selectbox('חצר', ['כן', 'לא'])
            near_dog_park = st.selectbox('קרוב לגן כלבים', ['כן', 'לא'])
        with col3:
            house_members = st.slider('חברי בית', min_value=1, max_value=10, step=1)
            availability_at_home = st.selectbox('זמינות בבית', ['מלאה', 'חלקית'])
        with col4:
            maximum_capacity = st.number_input('קיבולת מקסימלית', min_value=1, max_value=100, step=1)
            allergies = st.text_input('אלרגיות')

        # Apply search filters for foster homes
        # Apply search filters for foster homes
        filtered_foster_homes = foster_home_df_hebrew[
            (foster_home_df_hebrew['שם בית אומנה'].str.contains(foster_name, na=False, case=False)) &
            (foster_home_df_hebrew['ידידותי לילדים'] == children_friendly) &
            (foster_home_df_hebrew['ידידותי לכלבים'] == animal_friendly) &
            (foster_home_df_hebrew['גודל הבית'] == house_size) &
            (foster_home_df_hebrew['חצר'] == backyard) &
            (foster_home_df_hebrew['קרוב לגן כלבים'] == near_dog_park) &
            (foster_home_df_hebrew['חברי בית'] == house_members) &
            (foster_home_df_hebrew['זמינות בבית'] == availability_at_home) &
            (foster_home_df_hebrew['קיבולת מקסימלית'] >= maximum_capacity) &
            (foster_home_df_hebrew['אלרגיות'].str.contains(allergies, na=False, case=False))
            ]

        st.dataframe(filtered_foster_homes)

    # Sidebar logout button
    if st.sidebar.button("Log Out"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

# Call the function to display the dogs page
show_dogs_page()
