import streamlit as st
from Fix.BNI import run_app as run_bni_app
from Fix.BRI import run_app as run_bri_app
from Fix.BTN import run_app as run_btn_app
from Fix.home import run_app as run_home_app

def main():
    # Tambahkan sidebar
    st.sidebar.title("Menu")

    menu_options = ["BNI", "BRI", "BTN"]
    selected_menu = st.sidebar.selectbox("", menu_options)

    if selected_menu == "BNI":
        run_bni_app()
    elif selected_menu == "BRI":
        run_bri_app()
    elif selected_menu == "BTN":
        run_btn_app()

if __name__ == "__main__":
    main()
