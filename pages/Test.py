import streamlit as st
#
# st.image("Data/Logo.png", width=100)  # Adjust width as needed
#
#
# def add_logo():
#     st.sidebar.image('Data/Logo.png', use_column_width=True)
#     st.sidebar.write(
#         """
#         <style>
#             .sidebar-logo {
#                 position: absolute;
#                 top: 0;
#                 left: 0;
#                 width: 80px; /* Adjust width as needed */
#                 cursor: pointer;
#             }
#         </style>
#         <a href="/">
#             <img src="Data/Logo.png" class="sidebar-logo" alt="Logo">
#         </a>
#         """,
#         unsafe_allow_html=True,
#     )
#
# import streamlit as st
# from streamlit_option_menu import option_menu
#
# # Create two separate containers with unique keys for the option menus
# with st.container():
#     st.write("### Upper Container")
#     selected1 = option_menu(
#         menu_title="Menu 1",
#         options=["Dog Option", "Option 2", "Option 3"],
#         icons=["dog", "gear", "person"],  # Using 'dog' icon for the first option
#         menu_icon="cast",
#         default_index=0,
#         key="option_menu_1"  # Unique key for the first option menu
#     )
#     st.write(f"Selected from Menu 1: {selected1}")
#
# with st.container():
#     st.write("### Lower Container")
#     selected2 = option_menu(
#         menu_title="Menu 2",
#         options=["Option A", "Option B", "Option C"],
#         icons=["house", "gear", "person"],
#         menu_icon="cast",
#         default_index=0,
#         key="option_menu_2"  # Unique key for the second option menu
#     )
#     st.write(f"Selected from Menu 2: {selected2}")


st.title("Image in the Upper Center")

# Center align the image using CSS
# st.markdown(
#     """
#     <style>
#     .centered {
#         display: block;
#         margin-left: auto;
#         margin-right: auto;
#         padding-top: 5px; /* Adjust as needed */
#         max-width: 20%; /* Adjust as needed */
#
#
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
#
# # Load and display your image
# st.image('Data/Logo.png', use_column_width=True, caption='Your Image Caption')

st.title("Custom Logo Display")

# Load and display your logo image
# st.image('Data/Logo.png', width=200, )  # Adjust width as needed
# Center align the image using CSS
st.markdown(
    """
    <style>
    .centered-image {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and display your logo image with custom CSS class
st.image('Data/Logo.png', width=200, className="centered-image")

# Example content below the logo
st.write("This is your Streamlit application with a custom logo.")

# Use st.columns to create four equally sized columns
col1, col2, col3, col4 = st.columns(4)

# Button 1 in the first column
with col1:
    if st.button("כלבים"):
        st.switch_page("pages/Dogs.py")

# Button 2 in the second column
with col2:
    if st.button("בתי אומנה"):
        st.switch_page("pages/FosterHome.py")

# Button 3 in the third column
with col3:
    if st.button("אומצים"):
        st.switch_page("pages/adopters.py")

# Button 4 in the fourth column
with col4:
    if st.button("בקשות"):
        st.switch_page("pages/Applications.py")
