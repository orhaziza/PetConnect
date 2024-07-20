import streamlit as st
import pandas as pd

# Function to load dogs data
def load_dogs_data():
    dogs_file_path = 'Data/Dogs.csv'
    dogs_df = pd.read_csv(dogs_file_path, encoding='utf-8')
    return dogs_df

# Function to display dog profile page
def show_dog_profile_page():
    st.title("Dog Profile")

    if st.button("הוסף לסל התיאום"):
        st.session_state['Cart_dog'] = selected_dog_id
        

    # Ensure selected_dog_id is in session state
    if 'selected_dog_id' not in st.session_state:
        st.error("No dog selected. Please select a dog from the previous page.")
        return

    # Retrieve selected dog ID and scores DataFrame from session state
    selected_dog_id = st.session_state['selected_dog_id']
    scores_df = st.session_state.get('scores_df', pd.DataFrame())

    # Load dogs data
    dogs_df = load_dogs_data()

    # Get selected dog data
    selected_dog = dogs_df[dogs_df['DogID'] == selected_dog_id].iloc[0]

    # Display dog data in a designed way
    st.subheader(f"Profile of {selected_dog['Name']}")

    st.markdown("""
    <style>
    .dog-profile-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .dog-profile-item {
        margin: 10px;
        padding: 10px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        width: 45%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="dog-profile-container">', unsafe_allow_html=True)

    profile_items = [
        f"**Name:** {selected_dog['Name']}",
        f"**Date of Birth:** {selected_dog['DateOfBirth']}",
        f"**Age:** {selected_dog['Age']}",
        f"**Breed:** {selected_dog['Breed']}",
        f"**Weight:** {selected_dog['Weight']}",
        f"**Size:** {selected_dog['Size']}",
        f"**Gender:** {selected_dog['Gender']}",
        f"**Rescue Date:** {selected_dog['RescueDate']}",
        f"**Rabies Done:** {selected_dog['Rabies_Done']}",
        f"**Hexagonal 1:** {selected_dog['Hexagonal_1']}",
        f"**Hexagonal 2:** {selected_dog['Hexagonal_2']}",
        f"**Hexagonal 3:** {selected_dog['Hexagonal_3']}",
        f"**Hexagonal Done:** {selected_dog['Hexagonal_Done']}",
        f"**Spayed:** {selected_dog['Spayed']}",
        f"**De-worm:** {selected_dog['De-worm']}",
        f"**Children Friendly:** {selected_dog['Children_Friendly']}",
        f"**Animal Friendly:** {selected_dog['AnimalFriendly']}",
        f"**Health Status:** {selected_dog['HealthStatus']}",
        f"**Energy Level:** {selected_dog['EnergyLevel']}",
        f"**Photograph Status:** {selected_dog['PhotographStatus']}",
        f"**Adoption Status:** {selected_dog['AdoptionStatus']}",
        f"**Adopter ID:** {selected_dog['AdopterID']}",
        f"**Potty Trained:** {selected_dog['PottyTrained']}",
        f"**Adoption Name:** {selected_dog['AdoptionName']}",
    ]

    for item in profile_items:
        st.markdown(f'<div class="dog-profile-item">{item}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # # Display the scores DataFrame
    # if not scores_df.empty:
    #     st.subheader('Adopter Scores for This Dog')
    #     st.dataframe(scores_df)
  # Display the scores DataFrame with buttons to view applicant profiles
    # Display the scores DataFrame with buttons to view applicant profiles

    # Display the scores DataFrame with buttons to view applicant profiles in a table
    if not scores_df.empty:
        st.subheader('Adopter Scores for This Dog')

        st.markdown('<table class="applicant-table">', unsafe_allow_html=True)
        st.markdown("""
        <thead>
            <tr>
                <th>Application ID</th>
                <th>Applicant Name</th>
                <th>Score</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
        """, unsafe_allow_html=True)

        for index, row in scores_df.iterrows():
            st.markdown(f"""
            <tr>
                <td>{row['Application ID']}</td>
                <td>{row['Applicant Name']}</td>
                <td>{row['Score']}</td>
                <td><button class="view-profile-button" onClick="window.location.href='#'">View Profile of {row['Applicant Name']}</button></td>
            </tr>
            """, unsafe_allow_html=True)

            if st.button(f"View Profile of {row['Applicant Name']}", key=index):
                st.session_state['selected_applicant_id'] = row['Application ID']
                st.switch_page("pages/ApplicantProfile.py")

                st.experimental_rerun()  # Navigate to the applicant profile page

        st.markdown('</tbody></table>', unsafe_allow_html=True)


        




show_dog_profile_page()
