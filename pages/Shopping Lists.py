# ID,ItemName,category,quantity,Unit,DogSize,Desctiption

import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_option_menu import option_menu

def show_shopping_list_page():
    st.set_page_config(page_title='ShoppingList', layout='wide')

    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("לא ניתן לגשת לעמוד ללא התחברות")
        st.stop()


