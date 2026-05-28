import streamlit as st
import pyrebase
import dashboard

# SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "home"

# FIREBASE CONFIG
firebaseConfig = {
    "apiKey": "AIzaSyCX9r2ACAptGG3JwFe3IXKU343pJZFSkL0",
    "authDomain": "smart-irrigation-fd7ae.firebaseapp.com",
    "projectId": "smart-irrigation-fd7ae",
    "storageBucket": "smart-irrigation-fd7ae.firebasestorage.app",
    "messagingSenderId": "762028408708",
    "appId": "1:762028408708:web:61923eea5290ec30b0a7d1",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# IF LOGGED IN -> DASHBOARD
if st.session_state.logged_in:

    dashboard.main()

# AUTH PAGES
else:

    st.markdown(
        """
        <h1 style='text-align:center;'>
            🌱 Smart Irrigation System
        </h1>

        <h3 style='text-align:center; color:gray;'>
            Authentication Page
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")
    st.write("")

    # HOME PAGE
    if st.session_state.page == "home":

        col1, col2, col3 = st.columns([1,1,1])

        with col2:

            if st.button("Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()

            st.write("")

            if st.button("Sign Up", use_container_width=True):
                st.session_state.page = "signup"
                st.rerun()

    # LOGIN PAGE
    elif st.session_state.page == "login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            try:
                auth.sign_in_with_email_and_password(
                    email,
                    password
                )

                st.session_state.logged_in = True
                st.rerun()

            except Exception as e:
                st.error("Invalid email or password")

        if st.button("Back"):
            st.session_state.page = "home"
            st.rerun()

    # SIGNUP PAGE
    elif st.session_state.page == "signup":

        st.subheader("Create Account")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Create Account"):

            try:
                auth.create_user_with_email_and_password(
                    email,
                    password
                )

                st.success("Account created successfully!")

            except Exception as e:
                st.error("Could not create account")

        if st.button("Back"):
            st.session_state.page = "home"
            st.rerun()
