# 📈 Live AI Stock Market Dashboard
> **A Real-Time Predictive Engine for Global Equities**

**🔗 [Live Demo on Hugging Face](https://huggingface.co/spaces/Ekta-13/Stock-AI-Predictor)**

## 🎯 What it is
I built a smart **Stock Predictor** tool designed to simplify market analysis. Users can input any global ticker (e.g., Reliance, Apple, or Tata Motors), and the AI instantly analyzes historical data to generate a **Bullish** (Upward) or **Bearish** (Downward) signal.

## ⚙️ How it works
The "brain" of this dashboard is a **Machine Learning model** (Random Forest) trained on years of historical stock data. 
* **Pattern Recognition:** It analyzes complex indicators like moving averages and price momentum—performing calculations in milliseconds that would take a human hours.
* **Smart Validation:** To ensure the model is reliable, I used `TimeSeriesSplit` to prevent the AI from "cheating" by looking at future data during its training phase.

## 🚀 Key Features
* **🤖 AI Signal:** Generates directional predictions with a **Confidence Score** (e.g., 85% Bullish).
* **📊 Live Charts:** Creates an interactive **Plotly** graph so you can visualize price trends and technical overlays dynamically.
* **📰 Real-time News:** Automatically pulls the latest Google News headlines for the specific stock to provide fundamental context for price movements.
* **🌐 Cloud Deployed:** This is a fully functional web application hosted on **Hugging Face Spaces**, making it accessible to anyone, anywhere.

## 🛠️ Tech Stack
* **Language:** Python
* **Machine Learning:** Scikit-Learn (Random Forest)
* **Financial Logic:** Pandas-TA, YFinance
* **Interface:** Gradio & Plotly
* **Deployment:** Hugging Face Spaces

## 📸 Screenshots
![Dashboard Overview](https://github.com/user-attachments/assets/4fd74521-275c-46c3-a711-93f7b3016c8d)

## ⚡ Quick Start
```bash
# Clone the repository
git clone [https://github.com/Ekta-13/Stock-AI-Predictor.git](https://github.com/Ekta-13/Stock-AI-Predictor.git)

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
python app.py
  
