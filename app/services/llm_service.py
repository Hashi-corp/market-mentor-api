import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # Replace with actual endpoint if different

def chat_with_groq(messages, model="llama3-8b-8192"):
    """Send a chat request to Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def financial_prompt_template(symbol, question):
    """Template for financial questions about stocks"""
    return [
        {"role": "system", "content": "You are a financial assistant for Indian stock market investors. Provide concise, accurate information about stocks listed on Indian exchanges (NSE/BSE). For factual questions about companies (like CEO, founders, etc.), provide precise, up-to-date information with their full names and titles."},
        {"role": "user", "content": f"Stock: {symbol}\nQuestion: {question}"}
    ]

def get_stock_analysis(symbol, question):
    """Get LLM analysis for a stock question"""
    messages = financial_prompt_template(symbol, question)
    response = chat_with_groq(messages)
    
    if response and 'choices' in response:
        return response['choices'][0]['message']['content']
    return "Sorry, I couldn't analyze that stock at the moment."

# Additional financial prompt templates
def stock_recommendation_template(symbol):
    """Template for stock buy/hold/sell recommendations"""
    return [
        {"role": "system", "content": "You are a financial assistant for Indian stock market investors."},
        {"role": "user", "content": f"Provide a buy/hold/sell recommendation for {symbol} listed on NSE/BSE with brief reasoning."}
    ]

def sector_analysis_template(sector):
    """Template for sector analysis"""
    return [
        {"role": "system", "content": "You are a financial assistant for Indian stock market investors."},
        {"role": "user", "content": f"Provide a brief analysis of the {sector} sector in the Indian market. Include recent trends and outlook."}
    ]

# Example usage
if __name__ == "__main__":
    messages = financial_prompt_template("RELIANCE.NS", "Who is the CEO?")
    result = chat_with_groq(messages)
    print(result)