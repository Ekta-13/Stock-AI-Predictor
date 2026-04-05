import gradio as gr
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import joblib
import plotly.graph_objects as go
import feedparser

# Load the saved model
model = joblib.load('model.joblib')

def get_stock_news(ticker):
    """Fetch latest news headlines for the ticker with localized Indian support."""
    # Clean ticker for news search (remove .NS or .BO)
    search_term = ticker.replace(".NS", "").replace(".BO", "").strip()
    
    # Use Indian regional settings if it's an Indian ticker
    if ".NS" in ticker or ".BO" in ticker:
        feed_url = f"https://news.google.com/rss/search?q={search_term}+stock&hl=en-IN&gl=IN&ceid=IN:en"
    else:
        feed_url = f"https://news.google.com/rss/search?q={search_term}+stock&hl=en-US&gl=US&ceid=US:en"
        
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries[:5]: # Get top 5 headlines
        news_items.append(f"• {entry.title} ({entry.published[:16]})")
    return "\n\n".join(news_items) if news_items else "No recent news found."

def predict_stock(ticker):
    try:
        ticker = ticker.upper().strip()
        data = yf.download(ticker, period="6mo", interval="1d", progress=False)
        
        if data.empty: 
            return "❌ Not Found", None, "0", "0", "No News Found for this Ticker"
        
        # Flatten MultiIndex columns if present
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Feature Engineering (Ensuring match with your training set)
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['EMA_20'] = ta.ema(data['Close'], length=20)
        data['EMA_50'] = ta.ema(data['Close'], length=50)
        data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
        
        features = ['Close', 'RSI', 'EMA_20', 'EMA_50', 'ATR']
        
        # Drop rows with NaN values created by indicators
        data_clean = data.dropna(subset=features)
        if data_clean.empty:
            return "⚠️ Insufficient Data", None, "Error", "Error", "Not enough data to calculate indicators."

        latest_row = data_clean[features].tail(1)
        
        # Prediction Logic
        prediction = model.predict(latest_row)[0]
        prob = model.predict_proba(latest_row)[0]
        
        curr_price = data['Close'].iloc[-1]
        curr_rsi = round(data['RSI'].iloc[-1], 2)
        
        # Dynamic Currency Formatting
        currency_symbol = "₹" if (".NS" in ticker or ".BO" in ticker) else "$"
        formatted_price = f"{currency_symbol}{curr_price:,.2f}"
        
        res_text = "🚀 BULLISH" if prediction == 1 else "📉 BEARISH"
        conf_text = f"{res_text} ({max(prob)*100:.1f}% Confidence)"

        # Plotly Visualizations
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='#00d1ff')))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name='EMA 20', line=dict(dash='dot', color='#ff9900')))
        fig.update_layout(
            template="plotly_dark", 
            margin=dict(l=20, r=20, t=40, b=20), 
            height=350,
            xaxis_title="Date",
            yaxis_title=f"Price ({currency_symbol})"
        )

        # Fetch News
        news = get_stock_news(ticker)

        return conf_text, fig, formatted_price, f"RSI: {curr_rsi}", news
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}", None, "Error", "Error", "Error fetching news"

# UI Design with customized theme
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📈 AI Equity Intelligence Dashboard")
    gr.Markdown("### Live Predictive Analysis for NSE (.NS), BSE (.BO), and Global Markets")
    
    with gr.Row():
        with gr.Column(scale=1):
            ticker_input = gr.Textbox(label="Stock Ticker", placeholder="Ex: RELIANCE.NS, NVDA, 500325.BO")
            btn = gr.Button("Analyze Signal", variant="primary")
            
            out_text = gr.Label(label="Market Signal")
            
            with gr.Row():
                price_metric = gr.Textbox(label="Last Price", interactive=False)
                rsi_metric = gr.Textbox(label="Current RSI", interactive=False)
                
        with gr.Column(scale=2):
            out_plot = gr.Plot(label="Market Trend Analysis")
            
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📰 Recent Market Headlines")
            news_output = gr.Textbox(label="", lines=6, interactive=False)
            
    btn.click(predict_stock, inputs=ticker_input, outputs=[out_text, out_plot, price_metric, rsi_metric, news_output])

demo.launch()
