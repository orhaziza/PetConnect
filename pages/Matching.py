import streamlit as st
import pandas as pd



# Function to load dogs data
def load_dogs_data():
    dogs_file_path = 'Data/Dogs.csv'
    dogs_df = pd.read_csv(dogs_file_path, encoding='utf-8')
    return dogs_df

# Function to load applicants data
def load_applicants_data():
    applicants_file_path = 'Data/Applicants.csv'
    applicants_df = pd.read_csv(applicants_file_path, encoding='utf-8')
    return applicants_df



def show_matching_page():
    st.title("Matching Page")

    if 'Cart_dog' not in st.session_state or 'cart_applicant' not in st.session_state:
        st.error("No dog or applicant selected. Please select both a dog and an applicant.")
        return

    selected_dog_id = st.session_state['Cart_dog']
    selected_applicant_id = st.session_state['cart_applicant']

    dogs_df = load_dogs_data()
    applicants_df = load_applicants_data()

    selected_dog = dogs_df[dogs_df['DogID'] == selected_dog_id].iloc[0]
    selected_applicant = applicants_df[applicants_df['ApplictionID'] == selected_applicant_id].iloc[0]

    st.markdown("""
    <style>
    .matching-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .profile-container {
        background-color: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        width: 45%;
        margin: 10px;
    }
    .profile-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .profile-item {
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="matching-container">', unsafe_allow_html=True)

    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-header"><h3>Profile of {selected_dog["Name"]}</h3></div>', unsafe_allow_html=True)
    dog_profile_items = [
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
    for item in dog_profile_items:
        st.markdown(f'<div class="profile-item">{item}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="profile-header"><h3>Profile of {selected_applicant["ApplicantName"]}</h3></div>', unsafe_allow_html=True)
    applicant_profile_items = [
        f"**Application ID:** {selected_applicant['ApplictionID']}",
        f"**Dog ID:** {selected_applicant['dogID']}",
        f"**Adopter ID:** {selected_applicant['AdopterID']}",
        f"**Application Date:** {selected_applicant['applicationDate']}",
        f"**Applicant Name:** {selected_applicant['ApplicantName']}",
        f"**Message Content:** {selected_applicant['messageContect']}",
        f"**Source Platform:** {selected_applicant['SourcePlatform']}",
        f"**Prefers Large Dogs:** {selected_applicant['Large']}",
        f"**Prefers Small Dogs:** {selected_applicant['Small']}",
        f"**Prefers Medium Dogs:** {selected_applicant['Meduim']}",
        f"**Prefers Healthy Dogs:** {selected_applicant['Healthy']}",
        f"**Prefers Dogs Needing Attention:** {selected_applicant['Need Attention']}",
        f"**Prefers Active Dogs:** {selected_applicant['Active']}",
        f"**Prefers Calm Dogs:** {selected_applicant['Calm']}",
        f"**Prefers Animal Friendly Dogs:** {selected_applicant['Animal Friendly']}",
        f"**Preferred Gender:** {selected_applicant['Gender']}",
        f"**Prefers Spayed Dogs:** {selected_applicant['Spayed']}",
        f"**Prefers Neutered Dogs:** {selected_applicant['Neutered']}",
        f"**Children Friendly:** {selected_applicant['Children_Friendly']}",
        f"**Phone:** {selected_applicant['Phone']}",
    ]
    for item in applicant_profile_items:
        st.markdown(f'<div class="profile-item">{item}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


show_matching_page()
