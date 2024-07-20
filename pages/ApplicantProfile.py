import streamlit as st
import pandas as pd

# Function to load application data
def load_application_data():
    applications_file_path = 'Data/AdoptionApplication.csv'
    applications_df = pd.read_csv(applications_file_path, encoding='utf-8')
    return applications_df

# Function to display applicant profile page
def show_applicant_profile_page():
    st.title("Applicant Profile")

    # Ensure selected_applicant_id is in session state
    if 'selected_applicant_id' not in st.session_state:
        st.error("No applicant selected. Please select an applicant from the previous page.")
        return

    # Retrieve selected applicant ID from session state
    selected_applicant_id = st.session_state['selected_applicant_id']

    # Load application data
    applications_df = load_application_data()

    # Get selected applicant data
    selected_applicant = applications_df[applications_df['ApplictionID'] == selected_applicant_id].iloc[0]

    # Display applicant data in a designed way
    st.subheader(f"Profile of {selected_applicant['ApplicantName']}")

    st.markdown("""
    <style>
    .applicant-profile-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .applicant-profile-item {
        margin: 10px;
        padding: 10px;
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        width: 45%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="applicant-profile-container">', unsafe_allow_html=True)

    profile_items = [
        f"**Application ID:** {selected_applicant['ApplictionID']}",
        f"**Dog ID:** {selected_applicant['dogID']}",
        f"**Adopter ID:** {selected_applicant['AdopterID']}",
        f"**Application Date:** {selected_applicant['applicationDate']}",
        f"**Applicant Name:** {selected_applicant['ApplicantName']}",
        f"**Message Content:** {selected_applicant['messageContect']}",
        f"**Source Platform:** {selected_applicant['SourcePlatform']}",
        f"**Large Dog Preference:** {selected_applicant['Large']}",
        f"**Small Dog Preference:** {selected_applicant['Small']}",
        f"**Medium Dog Preference:** {selected_applicant['Meduim']}",
        f"**Healthy:** {selected_applicant['Healthy ']}",
        f"**Need Attention:** {selected_applicant['Need Attention']}",
        f"**Active:** {selected_applicant['Active']}",
        f"**Calm:** {selected_applicant['Calm']}",
        f"**Animal Friendly:** {selected_applicant['Animal Friendly']}",
        f"**Gender:** {selected_applicant['Gender']}",
        f"**Spayed:** {selected_applicant['Spayed']}",
        f"**Neutered:** {selected_applicant['Neutered']}",
        f"**Children Friendly:** {selected_applicant['Children_Friendly ']}",
        f"**Phone:** {selected_applicant['Phone ']}",
    ]

    for item in profile_items:
        st.markdown(f'<div class="applicant-profile-item">{item}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("הוסף לסל תיאום"):
        st.session_state['cart_applicant'] = st.session_state['selected_applicant_id']

# Simulate selection of an applicant for demonstration purposes
# This would normally be set in the previous page where the applicant is selected

show_applicant_profile_page()

