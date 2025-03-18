# 🏨 LLM-Powered Booking Analytics & QA System 🚀

## 🔥 Overview
This is an **AI-powered hotel booking analytics & chatbot** application.  
It provides **interactive insights, revenue predictions, and an AI assistant** using **Flask, Streamlit, and Gemini AI**.

### 🌟 **Key Features**
✅ **Real-Time Hotel Analytics** (Revenue, Cancellations, Top Countries)  
✅ **AI Chatbot** (Ask booking-related questions using Gemini AI 🤖)  
✅ **Revenue Forecasting** (Facebook Prophet predicts future revenue 📊)  
✅ **Interactive Dashboard** (Streamlit-based UI for easy data visualization)  
✅ **CSV Upload Support** (Update dataset dynamically in real-time 📂)  

---

## ⚙️ Tech Stack
🔹 **Backend**: Flask (API)  
🔹 **Frontend**: Streamlit (UI)  
🔹 **AI Model**: Google Gemini 1.5 Pro  
🔹 **Data Processing**: Pandas, NumPy  
🔹 **Visualization**: Matplotlib, Seaborn  
🔹 **Machine Learning**: Facebook Prophet  

---

## **📂 Project Structure**
```
📂 hotel_booking_analysis_project/
│── 📄 app.py                 # Flask API (Backend)
│── 📄 dashboard.py           # Streamlit UI (Frontend)             
│── 📄 hotel_bookings.csv      # Hotel Bookings Dataset
│── 📄 requirements.txt        # List of Dependencies
│── 📄 README.md               # Project Documentation
```

---

## **⚙️ Installation & Setup**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Aryan-Rajesh-Python/LLM-Powered-Booking-Analytics-QA-System.git
cd LLM-Powered-Booking-Analytics-QA-System
```

### **2️⃣ Create & Activate Virtual Environment (Optional)**
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate   # Mac/Linux
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Google Gemini API Key**
1. Go to [Google AI Console](https://ai.google.dev/)  
2. Generate an API key  
3. Open `app.py` and **replace**:
```python
GOOGLE_API_KEY = "your-gemini-api-key-here"
```
4. **OR** create a `.env` file and store it securely.

---

## **🚀 Running the Project**
### **1️⃣ Start Flask API (Backend)**
```bash
python app.py
```
📌 **Flask will run at** → `http://127.0.0.1:5000/`

### **2️⃣ Start Streamlit UI (Frontend)**
```bash
streamlit run dashboard.py
```
📌 **Streamlit UI will run at** → `http://localhost:8501/`

---

## **🔮 Sample AI Questions**
You can ask the chatbot **business-related questions**, such as:
1️⃣ *What is the average cancellation rate?*  
2️⃣ *Which month generates the highest revenue?*  
3️⃣ *Predict hotel revenue for the next 3 months.*  
4️⃣ *Which countries have the most hotel bookings?*  
5️⃣ *How can hotels reduce cancellations?*  

---

## **📊 API Endpoints**
| Endpoint             | Method | Description |
|----------------------|--------|-------------|
| `/analytics`        | GET    | Fetch revenue trends, cancellation rate, top countries |
| `/predict_revenue`  | GET    | Predicts revenue for the next 12 months |
| `/upload_csv`       | POST   | Uploads a new dataset for analysis |
| `/ask`             | POST   | AI chatbot for hotel-related questions |

---

## **🤝 Contributing**
Feel free to **fork the repo**, make improvements, and submit a pull request!  

---

🔥 **Enjoy your AI-powered hotel analytics system!** 🚀💪  
Let me know if you need any more updates! 😎
