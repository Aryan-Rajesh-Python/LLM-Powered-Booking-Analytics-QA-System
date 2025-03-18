import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from io import BytesIO

st.title("🏨 Advanced Hotel Booking Analysis")

# Upload CSV Button
st.sidebar.subheader("📤 Upload New Dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:5000/upload_csv", files=files)
    st.sidebar.success("Dataset Updated!")

# Fetch analytics data
st.subheader("📊 Revenue Trends & Analytics")
analytics_response = requests.get("http://127.0.0.1:5000/analytics").json()
st.metric("Cancellation Rate", analytics_response["cancellation_rate"])

# Show top booking countries
st.subheader("🌍 Top Booking Countries")
st.json(analytics_response["top_countries"])

# Show lead time distribution stats
st.subheader("📈 Lead Time Distribution")
st.json(analytics_response["lead_time_distribution"])

# Fetch revenue trend plot
st.subheader("📉 Revenue Trends Graph")
response = requests.get("http://127.0.0.1:5000/plot_revenue")

if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="Monthly Revenue Trends", use_column_width=True)
else:
    st.error("Failed to load revenue trends graph. Please make sure Flask is running.")

# Forecasting Graph
st.subheader("🔮 Forecasted Revenue Trends (Next 12 Months)")
predictions = requests.get("http://127.0.0.1:5000/predict_revenue").json()
st.json(predictions["predicted_revenue"])

# AI Chatbot
st.subheader("🤖 Ask AI about Bookings")
user_query = st.text_input("Enter your query:")
if user_query:
    try:
        response = requests.post("http://127.0.0.1:5000/ask", json={"query": user_query})
        
        if response.status_code == 400:
            st.error("⚠️ Invalid request: Make sure to enter a valid query.")
        elif response.status_code == 500:
            st.error("❌ AI processing error. Try again later.")
        else:
            ai_response = response.json()
            if "answer" in ai_response:
                st.write("🧠 AI Response:", ai_response["answer"])
            else:
                st.error("⚠️ AI returned an empty response. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Connection error: {e}")