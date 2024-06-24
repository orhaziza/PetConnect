import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Initialize the Streamlit app
st.set_page_config(page_title='PetConnect Management System', layout='wide')

# Initialize an empty dataframe for dogs data
dog_df = pd.read_csv("Dog.csv", encoding='Windows-1255')
adopters_df = pd.read_csv("adopter.csv", encoding='Windows-1255')
applications_df = pd.read_csv("AdoptionApplication.csv", encoding='Windows-1255')
dogsfosterhomes_df = pd.read_csv("DogFosterHome.csv", encoding='Windows-1255')
fosterhomes_df = pd.read_csv("FosterHome.csv", encoding='Windows-1255')
shopping_df = pd.read_csv("ShoppingList.csv", encoding='Windows-1255')
volunteers_df = pd.read_csv("volunteer.csv", encoding='Windows-1255')

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
    'healthStatus': 'מצב הכלב',
    'energylevel': 'רמת האנרגיה',
    'photographStatus': 'סטטוס הצילום',
    'adoptionStatus': 'סטטוס אימוץ',
    'adopterID': 'מזהה מאמץ',
    'pottyTrained': 'מחונך לצרכים',
    'animalFirendly': 'ידידותי לכלבים',
    # Add more column name translations as needed
}
images_folder = "DogsPhotos"
# Translate English column names to Hebrew
hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]

# Display DataFrame with Hebrew column names


# Sidebar navigation
st.sidebar.title('כלבים')
option = st.sidebar.radio("Go to", ["מצא כלב","הוסף כלב" ,"ערך תמונה"  , "מצא בית אומנה","כל הטבלה"])

# Page routing
if option == 'בית':
    st.header('PetConnect-ברוכים הבאים ל')

elif option == 'כל הטבלה':
    st.header('כל הטבלה')
    #
    #
    # def display_image(dog_id):
    #     image_path = os.path.join(images_folder, f"{dog_id}.png")
    #     if os.path.exists(image_path):
    #         st.image(image_path, caption=f"Dog ID: {dog_id}", use_column_width=False, width=256)
    #     else:
    #         st.write(f"No image found for Dog ID: {dog_id}")
    #
    #
    # # Add a new column to the DataFrame to display images
    #
    # # Rename columns
    # dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))
    #
    # # Display DataFrame with images
    # st.dataframe(dog_df_hebrew)
    # # Display individual image if selected
    # selected_dog_name = st.selectbox('בחר כלב', dog_df['name'].tolist())
    # selected_dog_id = dog_df[dog_df['name'] == selected_dog_name]['DogID'].iloc[0]
    # display_image(selected_dog_id)
    # Define the file path
    file_path = "Dog.csv"

    # Check if the file exists
    if not os.path.exists(file_path):
        st.error("The file does not exist.")
        st.stop()

    # Read CSV file
    dog_df = pd.read_csv(file_path, encoding='Windows-1255')
    hebrew_column_names = [hebrew_columns_dogs.get(col, col) for col in dog_df.columns]
    dog_df_hebrew = dog_df.rename(columns=dict(zip(dog_df.columns, hebrew_column_names)))

    # Display the editable table
    edited_df = st.data_editor(dog_df_hebrew, use_container_width=True, height=400)

    # Button to save changes
    if st.button("Save Changes"):
        # Rename columns back to English for saving
        edited_df.rename(columns={v: k for k, v in hebrew_columns_dogs.items()}, inplace=True)
        # Save the edited dataframe to the CSV file
        edited_df.to_csv(file_path, index=False, encoding='Windows-1255')
        st.success("Changes saved successfully!")

elif option == 'הוסף כלב':
    st.header('הזן נתוני כלב')
    new_dog_name = st.text_input('הכנס שם כלב')
    new_dog_age = st.number_input('הכנס גיל כלב בחודשים', min_value=0)
    new_dog_breed = st.text_input('הכנס זן כלב')
    new_dog_size = st.selectbox('הכנס את גודל הכלב', ['קטן', 'בינוני', 'גדול'])
    new_dog_gender = st.selectbox('הכנס את מין הכלב', ['זכר', 'נקבה'])
    new_dog_energy = st.selectbox('מהי רמת האנרגיה של הכלב', ['גבוהה', 'בינונית', 'נמוכה'])
    new_dog_health = st.selectbox('מהו מצבו הבריאותי של הכלב', ['בריא', 'מחכה לוטרינר', 'חולה'])
    new_dog_photo = st.selectbox('סטטוס התמונות של הכלב', ['צריך לתאם צילום', 'תואם צילום', 'צולם'])
    has_vaccine_2 = st.number_input('כמה חיסוני משושה קיבל הכלב', min_value=0)
    has_vaccine_1 = st.checkbox('האם קיבל חיסון כלבת')
    new_is_spay = st.checkbox('האם הכלב מסורס')
    is_child_friendly = st.checkbox('האם הכלב ידידותי לילדים')
    is_animal_friendly = st.checkbox('האם הכלב ידידותי לחיות אחרות')
    is_potty_trained = st.checkbox('האם הכלב מחונך לצרכים')
    uploaded_file = st.file_uploader("png הכנס תמונה של הכלב עם סיומת", type="png")

    if st.button('Submit'):
        # Generate a new DogID
        new_dog_id = dog_df['DogID'].max() + 1
        current_date = datetime.now().strftime('%d.%m.%Y')
        if uploaded_file is not None:
            image_path = os.path.join(images_folder, f"{new_dog_id}.png")
            with open(image_path, "wb") as f:
                f.write(uploaded_file.getvalue())
        new_dog_data = pd.DataFrame({
            'DogID': [new_dog_id],
            'name': [new_dog_name],
            'age': [new_dog_age],
            'breed': [new_dog_breed],
            'size': [new_dog_size],
            'gender': [new_dog_gender],
            'vaccine_1': [has_vaccine_1],
            'vaccine_2': [has_vaccine_2],
            'adoptionStatus': ['לא אומץ'],
            'adopterID': [None],
            'rescueDate': [current_date],
            'isSpay': [new_is_spay],
            'childrenFirendly': [is_child_friendly],
            'healthStatus': [new_dog_health],
            'energylevel': [new_dog_energy],
            'photographStatus': [new_dog_photo],
            'pottyTrained': [is_potty_trained],
            'animalFirendly': [is_animal_friendly],
        })
        dog_df = pd.concat([dog_df, new_dog_data], ignore_index=True)

        # Save the updated DataFrame back to the Dog.csv file
        dog_df.to_csv("Dog.csv", index=False, encoding='Windows-1255')

        st.success('New dog added successfully!')


elif option == 'ערך תמונה':
    st.header('הוספת תמונה לכלבים ללא תמונה')

    # Filter dogs without images
    dogs_without_images = dog_df[~dog_df['DogID'].astype(str).apply(lambda x: os.path.exists(os.path.join(images_folder, f"{x}.png")))]

    if not dogs_without_images.empty:
        st.write('כלבים ללא תמונות:')
        st.dataframe(dogs_without_images.rename(columns=dict(zip(dogs_without_images.columns, hebrew_column_names))))

        # Dropdown menu to select a dog to upload an image for
        selected_dog_name_for_image = st.selectbox('בחר כלב להוספת תמונה', dogs_without_images['name'].tolist())
        selected_dog_id_for_image = dogs_without_images[dogs_without_images['name'] == selected_dog_name_for_image]['DogID'].iloc[0]

        uploaded_file_for_dog = st.file_uploader("png הכנס תמונה של הכלב עם סיומת", type="png")

        if st.button('הוסף תמונה'):
            if uploaded_file_for_dog is not None:
                image_path_for_dog = os.path.join(images_folder, f"{selected_dog_id_for_image}.png")
                with open(image_path_for_dog, "wb") as f:
                    f.write(uploaded_file_for_dog.getvalue())

                st.success(f'תמונה לכלב {selected_dog_name_for_image} הוספה בהצלחה!')
    else:
        st.write('לכל הכלבים במסד הנתונים קיימת תמונה')

