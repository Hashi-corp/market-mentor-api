import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"  # API endpoint for Groq
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
    """Universal template for any stock-related question"""
    return [
        {"role": "system", "content": (
            "You are a highly knowledgeable financial assistant for Indian stock market investors. "
            "Answer any question related to the given stock, including but not limited to company fundamentals, management, news, recommendations, price, sector, and general analysis. "
            "If the question is outside the scope of the stock or not answerable, politely say so. "
            "Always provide concise, accurate, and up-to-date information."
        )},
        {"role": "user", "content": f"Stock: {symbol}\nQuestion: {question}"}
    ]

def get_stock_analysis(symbol, question):
    """Get LLM analysis for any stock question"""
    messages = financial_prompt_template(symbol, question)
    response = chat_with_groq(messages)
    
    if response and 'choices' in response:
        return response['choices'][0]['message']['content']
    return "Sorry, I couldn't analyze that stock at the moment."