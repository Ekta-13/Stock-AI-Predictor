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
    """Fetch latest news headlines for the ticker."""
    feed_url = f"https://news.google.com/rss/search?q={ticker}+stock+when:7d&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(feed_url)
    news_items = []
    for entry in feed.entries[:5]: # Get top 5 headlines
        news_items.append(f"• {entry.title} ({entry.published[:16]})")
    return "\n\n".join(news_items) if news_items else "No recent news found."

def predict_stock(ticker):
    try:
        ticker = ticker.upper().strip()
        data = yf.download(ticker, period="6mo", interval="1d", progress=False)
        if data.empty: return "❌ Not Found", None, "0", "0", "No News"
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        # Indicators
        data['RSI'] = ta.rsi(data['Close'], length=14)
        data['EMA_20'] = ta.ema(data['Close'], length=20)
        
        features = ['Close', 'RSI', 'EMA_20', 'EMA_50', 'ATR'] # Note: Ensure these were in your Colab training
        # For this demo, let's assume the model needs the 5 features we used before:
        data['EMA_50'] = ta.ema(data['Close'], length=50)
        data['ATR'] = ta.atr(data['High'], data['Low'], data['Close'], length=14)
        
        latest_row = data[features].tail(1)
        
        # Prediction
        prediction = model.predict(latest_row)[0]
        prob = model.predict_proba(latest_row)[0]
        curr_price = round(data['Close'].iloc[-1], 2)
        curr_rsi = round(data['RSI'].iloc[-1], 2)
        
        res_text = "🚀 BULLISH" if prediction == 1 else "📉 BEARISH"
        conf_text = f"{res_text} ({max(prob)*100:.1f}% Confidence)"

        # Plotly Graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Price', line=dict(color='#00d1ff')))
        fig.add_trace(go.Scatter(x=data.index, y=data['EMA_20'], name='EMA 20', line=dict(dash='dot', color='#ff9900')))
        fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20), height=350)

        # Fetch News
        news = get_stock_news(ticker)

        return conf_text, fig, f"${curr_price}", f"RSI: {curr_rsi}", news
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}", None, "Error", "Error", "Error fetching news"

# UI Design
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📈 AI Equity Intelligence Dashboard")
    
    with gr.Row():
        with gr.Column(scale=1):
            ticker_input = gr.Textbox(label="Stock Ticker", placeholder="NVDA, TSLA, AAPL...")
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