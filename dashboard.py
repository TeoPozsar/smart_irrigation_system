
import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import plotly.express as px


def main():

    # PAGE CONFIG
    st.set_page_config(
        page_title="Smart Irrigation",
        page_icon="🌱",
        layout="wide"
    )

    # FIREBASE
    try:
        firebase_admin.get_app()

    except:
        cred = credentials.Certificate(
            "smart-irrigation-fd7ae-firebase-adminsdk-fbsvc-adbe6d3445.json"
        )

        firebase_admin.initialize_app(cred)

    db = firestore.client()

    # GET DATA
    docs = db.collection("sensor_data").stream()

    data = []

    for doc in docs:
        data.append(doc.to_dict())

    # TITLE
    st.title("🌱 Smart Irrigation Dashboard")
    
    

    # LATEST DATA
    if data:

        latest = data[-1]

        moisture = latest.get("moisture", 0)
        pump_status = latest.get("pump", "OFF")
        timestamp = latest.get("timestamp", "No timestamp")

        col1, col2, col3 = st.columns(3)

        col1.metric("Soil Moisture", f"{moisture}%")
        col2.metric("Pump Status", pump_status)
        col3.metric("Last Update", str(timestamp))

    else:
        st.warning("No data found in Firestore")

    #ANALYTICS
    st.subheader("Analytics")

    df = pd.DataFrame(data)

    if not df.empty:
       #STATS
        avg_moisture = df["moisture"].mean()
        min_moisture = df["moisture"].min()
        max_moisture = df["moisture"].max()
 
        watering_count = df["pump"].sum()
        col1,col2,col3,col4 = st.columns(4)
        
        col1.metric(
            "Average Moisture",
            f"{avg_moisture:.1f}%"
         )

        col2.metric(
            "Lowest Moisture",
            f"{min_moisture}%"
        )

        col3.metric(
            "Highest Moisture",
            f"{max_moisture}%"
        )

        col4.metric(
            "Pump Activations",
            watering_count
        )


        #GRAPH
        st.subheader(" Moisture Over Time")

        fig = px.line(
            df,
            y="moisture",
            title="soil moisture history"
        )

        st.plotly_chart(fig,use_container_width=True)


    # HISTORY
    st.subheader("Watering History")

    for item in reversed(data[-10:]):

        st.write(
            f"Moisture: {item.get('moisture')}% | "
            f"Pump: {item.get('pump')} | "
            f"Time: {item.get('timestamp')}"
        )

    st.divider()
    if st.button("LOGOUT"):
       st.session_state.logged_in=False
       st.rerun() 
