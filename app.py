import pandas as pd
import numpy as np
import os
import google.generativeai as genai
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, jsonify, send_file
from io import BytesIO
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from prophet import Prophet  # ✅ Facebook Prophet for Forecasting

# Step 1: Configure Gemini API (Direct API Key)
GOOGLE_API_KEY = "AIzaSyD1FqKfI8azMkycqPuIOcevT1RW9K9RcsY"  # 🔥 Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Step 2: Load and Clean the Dataset
def load_data():
    df = pd.read_csv("hotel_bookings.csv")
    df.fillna(0, inplace=True)
    df["reservation_status_date"] = pd.to_datetime(df["reservation_status_date"])
    return df

df = load_data()

# Step 3: Analytics & Reporting
df["total_revenue"] = df["adr"] * (df["stays_in_week_nights"] + df["stays_in_weekend_nights"])
df["month"] = df["reservation_status_date"].dt.strftime("%Y-%m")

monthly_revenue = df.groupby("month")["total_revenue"].sum()
cancellation_rate = df["is_canceled"].mean() * 100
country_counts = df["country"].value_counts().head(10)
lead_time_distribution = df["lead_time"]

# Step 4: Advanced Time-Series Forecasting using Facebook Prophet
df_prophet = pd.DataFrame({"ds": pd.to_datetime(monthly_revenue.index), "y": monthly_revenue.values})

model = Prophet()
model.fit(df_prophet)
future = model.make_future_dataframe(periods=12, freq='ME')  # ✅ Fixed Frequency Warning
forecast = model.predict(future)

# Step 5: Flask API Setup
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "🔥 Advanced Hotel Booking Analysis API is Running!"

@app.route('/analytics', methods=['GET'])
def get_analytics():
    """Returns analytics from the dataset."""
    return jsonify({
        "revenue_trends": {str(k): v for k, v in monthly_revenue.items()},
        "cancellation_rate": f"{cancellation_rate:.2f}%",
        "top_countries": country_counts.to_dict(),
        "lead_time_distribution": lead_time_distribution.describe().to_dict()
    })

@app.route('/predict_revenue', methods=['GET'])
def predict_revenue():
    """Predicts next 12 months of revenue using Facebook Prophet."""
    future_forecast = forecast[['ds', 'yhat']].tail(12)
    predictions = {str(row['ds'].date()): round(row['yhat'], 2) for _, row in future_forecast.iterrows()}
    
    return jsonify({"predicted_revenue": predictions})

@app.route('/plot_revenue', methods=['GET'])
def plot_revenue():
    """Generates advanced revenue trend graph with cancellations."""
    plt.figure(figsize=(12, 6))

    # Plot Revenue Trends
    sns.lineplot(x=monthly_revenue.index.astype(str), y=monthly_revenue.values, marker='o', label="Revenue")

    # Overlay Cancellation Rates
    cancellation_trends = df.groupby("month")["is_canceled"].mean() * 100
    sns.lineplot(x=cancellation_trends.index.astype(str), y=cancellation_trends.values, marker='s', color='red', label="Cancellation Rate (%)")

    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trends & Cancellation Rates")
    plt.xlabel("Month")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)

    # Save plot to memory buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Allows users to upload a new CSV file for analysis."""
    file = request.files['file']
    if file:
        file.save("hotel_bookings.csv")
        global df, monthly_revenue, country_counts, lead_time_distribution
        df = load_data()
        monthly_revenue = df.groupby("month")["total_revenue"].sum()
        country_counts = df["country"].value_counts().head(10)
        lead_time_distribution = df["lead_time"]
        return jsonify({"message": "Dataset updated successfully!"})
    return jsonify({"error": "File upload failed"}), 400

@app.route('/ask', methods=['POST'])
def ask_question():
    """Handles user queries using Gemini AI."""
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "Invalid request. Please provide a query."}), 400  # ✅ Handle missing query

    query = data.get("query").strip()

    if not query:
        return jsonify({"error": "Query cannot be empty."}), 400  # ✅ Handle empty query

    # Advanced AI Prompt
    prompt = f"""
    You are an AI assistant analyzing hotel booking data.
    Answer the query using this dataset:

    - Latest Revenue Trends: {list(monthly_revenue.keys())[-5:]}
    - Cancellation Rate: {cancellation_rate:.2f}%
    - Top Booking Countries: {country_counts.to_dict()}
    
    Now, answer this question: {query}
    """

    try:
        gemini_model = genai.GenerativeModel("models/gemini-1.5-pro")
        response = gemini_model.generate_content(prompt)

        if not response or not hasattr(response, "text"):
            return jsonify({"error": "AI response is empty."}), 500  # ✅ Handle AI failure

        return jsonify({"answer": response.text.strip()})  # ✅ Return clean response

    except Exception as e:
        return jsonify({"error": f"AI processing failed: {str(e)}"}), 500  # ✅ Handle API errors

if __name__ == '__main__':
    print("🚀 Starting Flask API at http://127.0.0.1:5000/")
    app.run(debug=True)
