# Market Mentor: Indian Stock Market Research Assistant

Market Mentor is a real-time stock market research API and frontend designed for Indian investors. It provides:
- **Real-time stock information** (powered by yfinance)
- **AI-powered news summarization** (using Groq LLM and top Indian financial RSS feeds)
- **LLM-based Q&A** for any stock
- **Professional, user-friendly Gradio frontend**

---

## Features

- 📈 **Stock Info**: Get comprehensive, real-time data for any NSE/BSE stock (price, market cap, volume, ranges, financial metrics, sector, etc.)
- 📰 **News Summaries**: Aggregates and summarizes news from Economic Times, Moneycontrol, Business Standard, and Google News
- 🤖 **Q/A on Stock data**: Ask any question about a stock and get an LLM-powered answer
- 🖥️ **Gradio UI**: Clean, persistent, and responsive interface with side-by-side tables
- ⚡ **FastAPI Backend**: Modular, production-ready API
- 🗃️ **Planned Redis Integration**: Future-proofed for persistent, scalable caching

---

## Quick Start

### 1. Clone the Repository
```sh
git clone <your-repo-url>
cd market-mentor-api
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key
# (For future Redis integration)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_URL=redis://localhost:6379/0
```

### 4. Run the Backend (FastAPI)
```sh
uvicorn app.main:app --reload
```

### 5. Run the Frontend (Gradio)
```sh
python frontend/gradio_frontend.py
```
![image](https://github.com/user-attachments/assets/05d135f8-2551-4017-872d-6e15016e38da)

---

## Project Structure
```
market-mentor-api/
├── app/
│   ├── main.py            # FastAPI entrypoint
│   ├── configs.py         # Configuration & env
│   ├── models/            # Pydantic models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic (stock, news, LLM)
│   └── utils/             # Utilities (cache, etc.)
├── frontend/
│   └── gradio_frontend.py # Gradio UI
├── requirements.txt
├── .env
└── README.md
```

---

## API Overview

- `GET /api/stocks/{symbol}`: Real-time stock info
- `GET /api/news/{symbol}`: Summarized news for a stock
- `POST /api/llm-query`: Ask any question about a stock

---

## Redis Integration (in progress)
- The project is designed to support Redis for persistent, scalable caching of stock data, news, and LLM responses.
- The `app/utils/cache.py` utility is ready for Redis integration.
- To enable Redis, simply run a Redis server and update your `.env` file with the correct connection details.
