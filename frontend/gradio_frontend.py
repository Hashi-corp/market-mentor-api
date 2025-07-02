import gradio as gr
import requests
import json
import time

# API URL - update this to the actual deployed URL when available
API_URL = "http://localhost:8000/api"

def get_stock_info(symbol):
    """Fetch stock information from the API"""
    time.sleep(0.1)  # Small delay to ensure loading indicator appears
    try:
        response = requests.get(f"{API_URL}/stocks/{symbol}")
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict) and "price" in data:
            return f"""
            **{data['name']} ({data['symbol']})**
            
            Price: {data['currency']} {data['price']}
            Change: {data['change']} ({data['percent_change']}%)
            Exchange: {data['exchange']}
            """
        return "Unable to fetch stock data"
    except Exception as e:
        return f"Error: {str(e)}"

def get_stock_news(symbol):
    """Fetch news for a stock from the API"""
    time.sleep(0.1)  # Small delay to ensure loading indicator appears
    try:
        response = requests.get(f"{API_URL}/news/{symbol}")
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict) and "articles" in data:
            news_text = f"**Recent News for {data['symbol']}**\n\n"
            for article in data['articles']:
                news_text += f"- [{article['title']}]({article['url']})\n"
                news_text += f"  Source: {article['source']}, Date: {article['published_at']}\n"
                if article['summary']:
                    news_text += f"\n  Summary: {article['summary']}\n"
                news_text += "\n"
            return news_text
        return "No news found"
    except Exception as e:
        return f"Error: {str(e)}"

def ask_llm(symbol, question):
    """Ask a question about a stock to the LLM"""
    time.sleep(0.1)  # Small delay to ensure loading indicator appears
    try:
        response = requests.post(
            f"{API_URL}/llm-query",
            json={"symbol": symbol, "question": question}
        )
        response.raise_for_status()
        data = response.json()
        
        if data["success"] and "data" in data and "answer" in data["data"]:
            return data["data"]["answer"]
        return "No answer available"
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(title="Market Mentor") as demo:
    gr.Markdown("# Market Mentor - Indian Stock Market Research")
    
    with gr.Tab("Stock Info"):
        with gr.Row():
            stock_symbol_input = gr.Textbox(label="Stock Symbol (e.g., RELIANCE.NS)")
            get_info_btn = gr.Button("Get Stock Info")
        stock_info_output = gr.Markdown()
        get_info_btn.click(
            fn=get_stock_info, 
            inputs=stock_symbol_input, 
            outputs=stock_info_output,
            show_progress="full"
        )
    
    with gr.Tab("Stock News"):
        with gr.Row():
            news_symbol_input = gr.Textbox(label="Stock Symbol (e.g., RELIANCE.NS)")
            get_news_btn = gr.Button("Get News")
        news_output = gr.Markdown()
        get_news_btn.click(
            fn=get_stock_news, 
            inputs=news_symbol_input, 
            outputs=news_output,
            show_progress="full"
        )
    
    with gr.Tab("Ask About Stock"):
        with gr.Row():
            ask_symbol_input = gr.Textbox(label="Stock Symbol (e.g., RELIANCE.NS)")
            ask_question_input = gr.Textbox(label="Your Question")
        ask_btn = gr.Button("Ask")
        ask_output = gr.Markdown()
        ask_btn.click(
            fn=ask_llm,
            inputs=[ask_symbol_input, ask_question_input],
            outputs=ask_output,
            show_progress="full"
        )

# Launch the app
if __name__ == "__main__":
    demo.launch()
