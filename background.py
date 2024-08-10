import streamlit as st
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* This targets the main block and removes padding and margin */
        .main {{
            padding: 0 !important;
            margin: 0 !important;
        }}
        /* This targets the viewer-toolbar section and removes its background color and margin */
        [data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0);
            margin: 0;
        }}
        /* This targets the footer to remove any unwanted padding or margin */
        footer {{
            visibility: hidden;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def insert_logo(txt):
    with st.container():
        col4, col1, col2 = st.columns([1, 10, 1])
        with col1:
            st.markdown(f"<h1 style='text-align: center;'>{txt}</h1>", unsafe_allow_html=True)
        with col2:
            st.image("Data/Logo.png", width=100)

styles = {
    "container": {"b": "0px !important", "padding": "0!important", "align-items": "stretch", "background-color": "#fafafa"},
    "icon": {"color": "black"}, 
    "nav-link": {"text-align": "right", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"background-color": "#d1d8e6", "font-weight": "normal", "color": "black", },
}
