# 📈 AI Equity Intelligence Dashboard
**A Live Predictive Analysis Tool for Stock Market Movement**

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://huggingface.co/spaces/Ekta-13/Stock-AI-Predictor)

## 🎯 Overview
This project is a real-time Financial Intelligence dashboard that uses Machine Learning (Random Forest) to predict the next-day price direction of US equities. It combines technical analysis (indicators) with real-time market news to provide a holistic view for traders.

## 🚀 Features
* **Directional Prediction:** Forecasts "BULLISH" or "BEARISH" signals with confidence scores.
* **Technical Dashboard:** Visualizes Price vs. EMA trends using interactive Plotly charts.
* **Real-time News:** Fetches the latest Google News headlines for the analyzed ticker.
* **MLOps:** Fully deployed as a microservice on Hugging Face Spaces.

## 🛠️ Tech Stack
* **Language:** Python 3.13
* **Libraries:** Scikit-Learn, Pandas-TA, YFinance, Plotly, Gradio
* **Model:** Random Forest Classifier (Optimized via TimeSeriesSplit)
* **Deployment:** Hugging Face Spaces (Cloud-native)

## 🧠 Technical Challenges Solved
* **Data Leakage:** Implemented TimeSeriesSplit to ensure the model never "sees" the future during training.
* **Build Optimization:** Resolved environment-specific dependency conflicts (Python 3.13/NumPy 2.0) during cloud deployment.
* **Feature Engineering:** Calculated RSI, EMA, and ATR on-the-fly for real-time inference.

## 📸 Screenshots
![Dashboard Overview](<img width="1355" height="834" alt="Screenshot 2026-03-21 at 10 21 37 PM" src="https://github.com/user-attachments/assets/4fd74521-275c-46c3-a711-93f7b3016c8d" />
)
