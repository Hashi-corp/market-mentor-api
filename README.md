# Market Mentor API

A FastAPI-based API for Indian stock market research and analysis with LLM integration.

## Project Structure
```
MARKET-MENTOR-API
├── app
│   ├── models
│   │   ├── news_models.py
│   │   ├── response_models.py
│   │   └── stock_models.py
│   ├── routes
│   │   ├── llm.py
│   │   ├── news.py
│   │   └── stock.py
│   ├── services
│   │   ├── news_service.py
│   │   ├── llm_service.py
│   │   └── stock_service.py
│   ├── utils
│   │   ├── cache.py
│   │   └── scraper.py
│   ├── configs.py
│   └── main.py
├── frontend
│   └── gradio_frontend.py
├── .env
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Features

- Stock information for Indian stocks (NSE/BSE)
- Stock news aggregation
- LLM-powered stock analysis and research

## Installation

1. Clone the repository:
```
git clone https://github.com/Hashi-corp/market-mentor-api.git
cd market-mentor-api
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
GROQ_API_KEY=your_groq_api_key
```

## Usage

### Running the API

```
uvicorn app.main:app --reload
```

Access the API documentation at http://localhost:8000/docs

### Running the Gradio Frontend

```
python frontend/gradio_frontend.py
```

Access the Gradio UI at http://localhost:7860

## API Endpoints

- `/api/stocks/{symbol}` - Get stock information
- `/api/news/{symbol}` - Get news for a stock
- `/api/llm-query` - Query the LLM about a stock