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
            # Format market cap
            market_cap_str = "N/A"
            if data.get('market_cap'):
                market_cap = data['market_cap']
                if market_cap >= 1e12:
                    market_cap_str = f"₹{market_cap/1e12:.2f}T"
                elif market_cap >= 1e9:
                    market_cap_str = f"₹{market_cap/1e9:.2f}B"
                elif market_cap >= 1e7:
                    market_cap_str = f"₹{market_cap/1e7:.2f}Cr"
                else:
                    market_cap_str = f"₹{market_cap:,.0f}"
            
            # Format volume
            volume_str = f"{data.get('volume', 0):,}" if data.get('volume') else "N/A"
            avg_volume_str = f"{data.get('avg_volume', 0):,}" if data.get('avg_volume') else "N/A"
            
            # Format price change with color indication
            change = data.get('change', 0)
            percent_change = data.get('percent_change', 0)
            change_indicator = "🔺" if change > 0 else "🔻" if change < 0 else "➡️"
            
            # Format financial metrics
            pe_ratio = f"{data.get('pe_ratio', 0):.2f}" if data.get('pe_ratio') else "N/A"
            eps = f"{data.get('eps', 0):.2f}" if data.get('eps') else "N/A"
            dividend_yield = f"{data.get('dividend_yield', 0)*100:.2f}%" if data.get('dividend_yield') else "N/A"
            book_value = f"{data.get('book_value', 0):.2f}" if data.get('book_value') else "N/A"
            
            # Create three separate sections for side-by-side display
            price_info = f"""
## 💰 **Price Information**
| Metric | Value |
|--------|--------|
| **Current Price** | **{data['currency']} {data['price']:.2f}** |
| **Change** | {change_indicator} {change:.2f} ({percent_change:.2f}%) |
| **Exchange** | {data.get('exchange', 'N/A')} |
| **Market State** | {data.get('market_state', 'N/A')} |
            """
            
            market_data = f"""
## 📊 **Market Data**
| Metric | Value |
|--------|--------|
| **Market Cap** | {market_cap_str} |
| **Volume (Today)** | {volume_str} |
| **Avg Volume** | {avg_volume_str} |
| **Day Range** | {data.get('day_low', 'N/A')} - {data.get('day_high', 'N/A')} |
| **52 Week Range** | {data.get('week_52_low', 'N/A')} - {data.get('week_52_high', 'N/A')} |
            """
            
            financial_info = f"""
## 📈 **Financial Metrics**
| Metric | Value |
|--------|--------|
| **P/E Ratio** | {pe_ratio} |
| **EPS** | {eps} |
| **Dividend Yield** | {dividend_yield} |
| **Book Value** | {book_value} |
| **Sector** | {data.get('sector', 'N/A')} |
| **Industry** | {data.get('industry', 'N/A')} |
            """
            
            return {
                "company_name": f"# {data['name']} ({data['symbol']})",
                "price_info": price_info,
                "market_data": market_data, 
                "financial_info": financial_info,
                "last_updated": f"*📅 Last Updated: {data.get('last_updated', 'N/A')}*"
            }
            
        return {
            "company_name": "❌ Unable to fetch stock data",
            "price_info": "",
            "market_data": "",
            "financial_info": "",
            "last_updated": ""
        }
    except Exception as e:
        return {
            "company_name": f"❌ **Error:** {str(e)}",
            "price_info": "",
            "market_data": "",
            "financial_info": "",
            "last_updated": ""
        }

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
    gr.Markdown("# 📈 Market Mentor - Indian Stock Market Research Assistant")
    
    # State variables to persist data during the session
    stock_info_state = gr.State({})
    news_state = gr.State("")
    llm_answer_state = gr.State("")
    
    with gr.Tab("📊 Stock Info"):
        with gr.Row():
            with gr.Column(scale=3):
                stock_symbol_input = gr.Textbox(
                    label="Stock Symbol (e.g., RELIANCE.NS, TCS.NS, INFY.NS)",
                    placeholder="Enter stock symbol...",
                    value=""
                )
            with gr.Column(scale=1):
                get_info_btn = gr.Button("📈 Get Stock Info", variant="primary")
        
        # Company name header
        company_name_output = gr.Markdown(value="", visible=True)
        
        # Side-by-side layout for tables
        with gr.Row():
            with gr.Column(scale=1):
                price_info_output = gr.Markdown(value="", visible=True)
            with gr.Column(scale=1):
                market_data_output = gr.Markdown(value="", visible=True)
            with gr.Column(scale=1):
                financial_info_output = gr.Markdown(value="", visible=True)
        
        # Last updated footer
        last_updated_output = gr.Markdown(value="", visible=True)
        
        def update_stock_info(symbol):
            result = get_stock_info(symbol)
            return (
                result["company_name"], 
                result["price_info"], 
                result["market_data"], 
                result["financial_info"],
                result["last_updated"],
                result  # For state
            )
        
        get_info_btn.click(
            fn=update_stock_info,
            inputs=stock_symbol_input,
            outputs=[
                company_name_output,
                price_info_output, 
                market_data_output, 
                financial_info_output,
                last_updated_output,
                stock_info_state
            ],
            show_progress="full"
        )
        
        # Restore state on load
        def restore_stock_state(state):
            if state and isinstance(state, dict) and state.get("company_name"):
                return (
                    state.get("company_name", ""),
                    state.get("price_info", ""),
                    state.get("market_data", ""),
                    state.get("financial_info", ""),
                    state.get("last_updated", "")
                )
            return ("", "", "", "", "")
        
        # Load state when the interface loads
        demo.load(
            fn=restore_stock_state,
            inputs=stock_info_state,
            outputs=[
                company_name_output,
                price_info_output,
                market_data_output,
                financial_info_output,
                last_updated_output
            ]
        )
    
    with gr.Tab("📰 Stock News"):
        with gr.Row():
            with gr.Column(scale=3):
                news_symbol_input = gr.Textbox(
                    label="Stock Symbol (e.g., RELIANCE.NS, TCS.NS, INFY.NS)",
                    placeholder="Enter stock symbol...",
                    value=""
                )
            with gr.Column(scale=1):
                get_news_btn = gr.Button("📰 Get News", variant="primary")
        
        news_output = gr.Markdown(value="", visible=True)
        
        def update_news(symbol):
            result = get_stock_news(symbol)
            return result, result  # Return for both display and state
        
        get_news_btn.click(
            fn=update_news,
            inputs=news_symbol_input,
            outputs=[news_output, news_state],
            show_progress="full"
        )
        
        # Restore state on load  
        def restore_news_state(state):
            return state if state else ""
        
        demo.load(
            fn=restore_news_state,
            inputs=news_state,
            outputs=news_output
        )
    
    with gr.Tab("🤖 Ask About Stock"):
        with gr.Row():
            with gr.Column():
                ask_symbol_input = gr.Textbox(
                    label="Stock Symbol (e.g., RELIANCE.NS, TCS.NS, INFY.NS)",
                    placeholder="Enter stock symbol...",
                    value=""
                )
                ask_question_input = gr.Textbox(
                    label="Your Question",
                    placeholder="e.g., Who is the CEO? What's the business model? Should I invest?",
                    lines=2
                )
                ask_btn = gr.Button("🤖 Ask AI", variant="primary")
        
        ask_output = gr.Markdown(value="", visible=True)
        
        def update_llm_answer(symbol, question):
            result = ask_llm(symbol, question)
            return result, result  # Return for both display and state
        
        ask_btn.click(
            fn=update_llm_answer,
            inputs=[ask_symbol_input, ask_question_input],
            outputs=[ask_output, llm_answer_state],
            show_progress="full"
        )
        
        # Restore state on load
        def restore_llm_state(state):
            return state if state else ""
        
        demo.load(
            fn=restore_llm_state,
            inputs=llm_answer_state,
            outputs=ask_output
        )

# Launch the app
if __name__ == "__main__":
    demo.launch()
