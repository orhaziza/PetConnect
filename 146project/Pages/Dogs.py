# Pages/Dogs.py
import streamlit as st
import pandas as pd
import os

def main():
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'
        st.experimental_rerun()
    st.title("Manage Dogs")
    # Path to the CSV files
    dogs_file_path = "146project/Data/Dogs.csv"
    images_folder = "DogsPhotos"
    
    # Load data
    if not os.path.exists(dogs_file_path):
        st.error("The dogs data file does not exist.")
        return
    
    dog_df = pd.read_csv(dogs_file_path, encoding='Windows-1255')

    # Hebrew column translations
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
        'healthStatus': 'מצב הכלב',
        'energylevel': 'רמת האנרגיה',
        'photographStatus': 'סטטוס הצילום',
        'adoptionStatus': 'סטטוס אימוץ',
        'adopterID': 'מזהה מאמץ',
        'pottyTrained': 'מחונך לצרכים',
        'animalFirendly': 'ידידותי לכלבים',
    }

    # Translate English column names to Hebrew
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
    dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))
    # Display the editable table
    edited_df = st.data_editor(dog_df_hebrew, use_container_width=True, height=400)
    
    # Button to save changes
    if st.button("Save Changes"):
        # Rename columns back to English for saving
        edited_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
        # Save the edited dataframe to the CSV file
        edited_df.to_csv(dogs_file_path, index=False, encoding='Windows-1255')
        st.success("Changes saved successfully!")

    # Define the menu options
    with st.sidebar:
        selected = st.selectbox("Select an option", ["All Dogs", "Find a Dog", "Add a Dog", "Edit Image"])

    # Display based on menu selection
    if selected == "All Dogs":
        if st.button("Save Changes"):
            # Rename columns back to English for saving
            dog_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
            dog_df.to_csv(dogs_file_path, index=False, encoding='Windows-1255')
            st.success("Changes saved successfully!")

    elif selected == "Find a Dog":
        st.subheader('Find a Dog')
        # Add search logic
        breed = st.selectbox('Breed', options=[''] + list(dog_df['breed'].unique()))
        age = st.slider('Age', min_value=0, max_value=int(dog_df['age'].max()), value=(0, int(dog_df['age'].max())))
        size = st.selectbox('Size', options=[''] + list(dog_df['size'].unique()))
        gender = st.selectbox('Gender', options=[''] + list(dog_df['gender'].unique()))

        # Apply search filters
        filtered_df = dog_df_hebrew[
            (dog_df['breed'].isin([breed]) if breed else True) &
            (dog_df['age'] >= age[0]) & (dog_df['age'] <= age[1]) &
            (dog_df['size'].isin([size]) if size else True) &
            (dog_df['gender'].isin([gender]) if gender else True)
        ]
        st.write(filtered_df)

    elif selected == "Add a Dog":
        st.subheader('Add a New Dog')
        with st.form(key='insert_form'):
            DogID = st.text_input('Dog ID')
            name = st.text_input('Name')
            age = st.number_input('Age', min_value=0, max_value=100, step=1)
            breed = st.text_input('Breed')
            size = st.selectbox('Size', ['Small', 'Medium', 'Large'])
            gender = st.selectbox('Gender', ['Male', 'Female'])
            rescueDate = st.date_input('Rescue Date')
            vaccine_1 = st.checkbox('Rabies Vaccine')
            vaccine_2 = st.checkbox('Hexavalent Vaccine')
            isSpay = st.checkbox('Spayed/Neutered')
            childrenFirendly = st.checkbox('Friendly to Children')
            animalFirendly = st.checkbox('Friendly to Other Animals')
            healthStatus = st.text_input('Health Status')
            energylevel = st.selectbox('Energy Level', ['Low', 'Medium', 'High'])
            photographStatus = st.selectbox('Photograph Status', ['Pending', 'Completed'])
            adoptionStatus = st.selectbox('Adoption Status', ['Available', 'Adopted'])
            adopterID = st.text_input('Adopter ID')
            pottyTrained = st.checkbox('Potty Trained')

            submit_button = st.form_submit_button(label='Add Dog')

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
            dog_df.to_csv(dogs_file_path, index=False, encoding='Windows-1255')
            st.success('The dog has been added successfully!')

    elif selected == "Edit Image":
        st.subheader('Edit Dog Image')
        dogs_without_images = dog_df[~dog_df['DogID'].astype(str).apply(lambda x: os.path.exists(os.path.join(images_folder, f"{x}.png")))]
        if not dogs_without_images.empty:
            st.write('Dogs without images:')
            st.dataframe(dogs_without_images.rename(columns=dict(zip(dogs_without_images.columns, hebrew_column_names))))
            selected_dog_name_for_image = st.selectbox('Select Dog to Add Image', dogs_without_images['name'].tolist())
            selected_dog_id_for_image = dogs_without_images[dogs_without_images['name'] == selected_dog_name_for_image]['DogID'].iloc[0]
            uploaded_file_for_dog = st.file_uploader("Upload Dog Image (.png)", type="png")
            if st.button('Add Image'):
                if uploaded_file_for_dog is not None:
                    image_path_for_dog = os.path.join(images_folder, f"{selected_dog_id_for_image}.png")
                    with open(image_path_for_dog, "wb") as f:
                        f.write(uploaded_file_for_dog.getvalue())
                    st.success(f'Image for {selected_dog_name_for_image} added successfully!')
        else:
            st.write('All dogs in the database have images')
