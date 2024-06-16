# import streamlit as st
# import pandas as pd
# import os
# from streamlit_option_menu import option_menu
#
# # Set page configuration
# st.set_page_config(page_title='Dogs', layout='wide')
#
# # Load the dog data
# file_path = "Dog.csv"
# if not os.path.exists(file_path):
#     st.error("The file does not exist.")
#     st.stop()
#
# dog_df = pd.read_csv(file_path, encoding='Windows-1255')
#
# # Define Hebrew column names
# hebrew_columns_dogs = {
#     'DogID': 'מזהה כלב',
#     'name': 'שם',
#     'age': 'גיל',
#     'breed': 'זן',
#     'size': 'גודל',
#     'gender': 'מין',
#     'rescueDate': 'תאריך חילוץ',
#     'vaccine_1': 'חיסון כלבת',
#     'vaccine_2': 'חיסון משושה',
#     'isSpay': 'מעוקר',
#     'childrenFirendly': 'ידידותי לילדים',
#     'healthStatus': 'מצב הכלב',
#     'energylevel': 'רמת האנרגיה',
#     'photographStatus': 'סטטוס הצילום',
#     'adoptionStatus': 'סטטוס אימוץ',
#     'adopterID': 'מזהה מאמץ',
#     'pottyTrained': 'מחונך לצרכים',
#     'animalFirendly': 'ידידותי לכלבים',
# }
#
# # Translate English column names to Hebrew
# hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
# dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))
#
# # Define the menu options
# with st.sidebar:
#     selected = option_menu("Main Menu", ["Search Dogs", "Page 2", "Page 3", "Page 4"],
#                            icons=["search", "file", "file", "file"], menu_icon="menu", default_index=0)
#
# # Page 1: Search Dogs
# if selected == "Search Dogs":
#     st.title('Search Dogs')
#
#     # Display the editable table
#     edited_df = st.data_editor(dog_df_hebrew, use_container_width=True, height=400)
#
#     # Button to save changes
#     if st.button("Save Changes"):
#         # Rename columns back to English for saving
#         edited_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
#         # Save the edited dataframe to the CSV file
#         edited_df.to_csv(file_path, index=False, encoding='Windows-1255')
#         st.success("Changes saved successfully!")
#
#     # Search functionality
#     st.subheader('Search for a Dog')
#
#     # Create search filters
#     breed = st.selectbox('Breed', options=[''] + list(dog_df['breed'].unique()))
#     age = st.slider('Age', min_value=0, max_value=int(dog_df['age'].max()), value=(0, int(dog_df['age'].max())))
#     size = st.selectbox('Size', options=[''] + list(dog_df['size'].unique()))
#     gender = st.selectbox('Gender', options=[''] + list(dog_df['gender'].unique()))
#
#     # Apply search filters
#     filtered_df = dog_df_hebrew[
#         (dog_df['breed'].isin([breed]) if breed else True) &
#         (dog_df['age'] >= age[0]) & (dog_df['age'] <= age[1]) &
#         (dog_df['size'].isin([size]) if size else True) &
#         (dog_df['gender'].isin([gender]) if gender else True)
#         ]
#
#     st.write(filtered_df)
#
# # Page 2: Placeholder
# if selected == "Page 2":
#     st.title('Page 2')
#     st.write('This is page 2.')
#
# # Page 3: Placeholder
# if selected == "Page 3":
#     st.title('Page 3')
#     st.write('This is page 3.')
#
# # Page 4: Placeholder
# if selected == "Page 4":
#     st.title('Page 4')
#     st.write('This is page 4.')


import streamlit as st
import pandas as pd
import os

# Set page configuration
st.set_page_config(page_title='Dogs', layout='wide')

# Load the dog data
file_path = "Dog.csv"
if not os.path.exists(file_path):
    st.error("The file does not exist.")
    st.stop()

dog_df = pd.read_csv(file_path, encoding='Windows-1255')

# Define Hebrew column names
hebrew_columns_dogs = {
    'DogID': 'מזהה כלב',
    'name': 'שם',
    'age': 'גיל',
    'breed': 'זן',
    'size': 'גודל',
    'gender': 'מין',
    'rescueDate': 'תאריך חילוץ',
    'vaccine_1': 'חיסון כלבת',
    'vaccine_2': 'חיסון משושה',
    'isSpay': 'מעוקר',
    'childrenFirendly': 'ידידותי לילדים',
    'animalFirendly': 'ידידותי לכלבים',
    'healthStatus': 'מצב הכלב',
    'energylevel': 'רמת האנרגיה',
    'photographStatus': 'סטטוס הצילום',
    'adoptionStatus': 'סטטוס אימוץ',
    'adopterID': 'מזהה מאמץ',
    'pottyTrained': 'מחונך לצרכים',
}

# Translate English column names to Hebrew
hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

# CSS for horizontal menu
st.markdown("""
    <style>
    .nav-menu {
        display: flex;
        justify-content: space-around;
        background-color: #f1f1f1;
        padding: 10px;
    }
    .nav-menu a {
        text-decoration: none;
        color: black;
        font-size: 20px;
        padding: 10px;
    }
    .nav-menu a:hover {
        background-color: #ddd;
    }
    .nav-menu a.active {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Navigation menu
menu = st.markdown("""
    <div class="nav-menu">
        <a href="#home" class="active" id="home-link">Search Dogs</a>
        <a href="#page2" id="page2-link">Page 2</a>
        <a href="#page3" id="page3-link">Insert Dog</a>
        <a href="#page4" id="page4-link">Page 4</a>
    </div>
""", unsafe_allow_html=True)

# Define pages
def home():
    st.title('Search Dogs')

    # Display the editable table
    edited_df = st.experimental_data_editor(dog_df_hebrew, use_container_width=True, height=400)

    # Button to save changes
    if st.button("Save Changes"):
        # Rename columns back to English for saving
        edited_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
        # Save the edited dataframe to the CSV file
        edited_df.to_csv(file_path, index=False, encoding='Windows-1255')
        st.success("Changes saved successfully!")

    # Search functionality
    st.subheader('Search for a Dog')

    # Create search filters in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        breed = st.selectbox('Breed', options=[''] + list(dog_df['breed'].unique()))
    with col2:
        age = st.slider('Age', min_value=0, max_value=int(dog_df['age'].max()), value=(0, int(dog_df['age'].max())))
    with col3:
        size = st.selectbox('Size', options=[''] + list(dog_df['size'].unique()))
    with col4:
        gender = st.selectbox('Gender', options=[''] + list(dog_df['gender'].unique()))

    # Apply search filters
    filtered_df = dog_df_hebrew[
        (dog_df['breed'].isin([breed]) if breed else True) &
        (dog_df['age'] >= age[0]) & (dog_df['age'] <= age[1]) &
        (dog_df['size'].isin([size]) if size else True) &
        (dog_df['gender'].isin([gender]) if gender else True)
    ]

    st.write(filtered_df)

def page2():
    st.title('Page 2')
    st.write('This is page 2.')

def page3():
    st.title('Insert Dog')

    with st.form(key='insert_form'):
        DogID = st.text_input('Dog ID')
        name = st.text_input('Name')
        age = st.number_input('Age', min_value=0, max_value=100, step=1)
        breed = st.text_input('Breed')
        size = st.selectbox('Size', ['Small', 'Medium', 'Large'])
        gender = st.selectbox('Gender', ['Male', 'Female'])
        rescueDate = st.date_input('Rescue Date')
        vaccine_1 = st.checkbox('Vaccine 1')
        vaccine_2 = st.checkbox('Vaccine 2')
        isSpay = st.checkbox('Is Spayed/Neutered')
        childrenFirendly = st.checkbox('Children Friendly')
        animalFirendly = st.checkbox('Animal Friendly')
        healthStatus = st.text_input('Health Status')
        energylevel = st.selectbox('Energy Level', ['Low', 'Medium', 'High'])
        photographStatus = st.selectbox('Photograph Status', ['Pending', 'Completed'])
        adoptionStatus = st.selectbox('Adoption Status', ['Available', 'Adopted'])
        adopterID = st.text_input('Adopter ID')
        pottyTrained = st.checkbox('Potty Trained')

        submit_button = st.form_submit_button(label='Insert Dog')

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
        st.success('Dog added successfully!')

def page4():
    st.title('Page 4')
    st.write('This is page 4.')

# Define navigation
pages = {
    "home": home,
    "page2": page2,
    "page3": page3,
    "page4": page4
}

# Select the active page
query_params = st.experimental_get_query_params() if hasattr(st, 'experimental_get_query_params') else st.query_params()
if "page" in query_params:
    active_page = query_params["page"][0]
else:
    active_page = "home"

# Run the active page
if active_page in pages:
    pages[active_page]()

# Update the active link
st.markdown(f"""
    <script>
    document.getElementById("{active_page}-link").classList.add("active");
    </script>
""", unsafe_allow_html=True)
