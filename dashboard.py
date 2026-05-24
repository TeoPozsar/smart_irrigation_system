import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Irrigation",
    page_icon="🌱",
    layout="wide"
)

# ---------- FIREBASE ----------
try:
    firebase_admin.get_app()
except:
    cred = credentials.Certificate(
        "smart-irrigation-fd7ae-firebase-adminsdk-fbsvc-adbe6d3445.json"
    )
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------- GET DATA ----------
docs = db.collection("sensor_data").stream()

data = []

for doc in docs:
    data.append(doc.to_dict())

# ---------- TITLE ----------
st.markdown(
    """
    <h1 style='text-align: center; color: #7CFC00;'>
        🌱 Smart Irrigation Dashboard
    </h1>
    <hr>
    """,
    unsafe_allow_html=True
)

if data:

    latest = data[-1]

    moisture = latest["moisture"]
    pump = latest["pump"]

    # ---------- STATUS COLOR ----------
    if moisture < 30:
        status = "Dry Soil"
        color = "red"
    elif moisture < 60:
        status = "Normal"
        color = "orange"
    else:
        status = "Wet Soil"
        color = "green"

    # ---------- TOP CARDS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="💧 Moisture",
            value=f"{moisture}%"
        )

    with col2:
        st.metric(
            label="🚰 Pump",
            value="ON" if pump else "OFF"
        )

    with col3:
        st.markdown(
            f"""
            <h3 style='color:{color};'>
                {status}
            </h3>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # ---------- RECENT READINGS ----------
    st.subheader("📋 Recent Readings")

    for item in reversed(data[-10:]):

        moisture = item["moisture"]
        pump = item["pump"]

        if moisture < 30:
            emoji = "🔴"
        elif moisture < 60:
            emoji = "🟠"
        else:
            emoji = "🟢"

        st.markdown(
            f"""
            {emoji} **Moisture:** {moisture}%  
            🚰 **Pump:** {"ON" if pump else "OFF"}
            """
        )

        st.divider()

else:
    st.warning("No sensor data found.")
