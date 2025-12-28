# LLM Stock Agent (Real-time Market Tracker)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-orange)](https://docs.openwebui.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

> A robust, microservice-based LLM Agent capable of retrieving real-time stock market data via Finnhub API.

這是一個基於 **OpenWebUI** (前端/推理) 與 **FastAPI** (後端工具) 的智慧股市 Agent。透過串接 **Finnhub API**，讓 LLM 能夠即時查詢台美股（如 AAPL, 2330.TW）的最新價格，並具備自然語言代號轉換能力。

---

## Features (功能特色)

- **Real-time Data Fetching**: 使用 Finnhub 金融級 API，提供精確的即時股價、漲跌幅與幣別。
- **Smart Ticker Resolution**: 利用 LLM 的推理能力，自動將公司名稱（如 "台積電", "Tesla"）轉換為正確的股票代號（"2330.TW", "TSLA"）。
- **Microservice Architecture**: 工具端獨立為 Python FastAPI Server，透過 RESTful API 與 OpenWebUI 溝通，符合 Agent 設計模式。
- **Docker Compatibility**: 專為在 Docker 容器運行的 OpenWebUI 設計，支援 `host.docker.internal` 連線。

---

## Architecture & FSM (系統架構與狀態機)

本專案實作了典型的 Agent 狀態機邏輯 (Finite State Machine)，符合 TOC 課程專題要求：

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> ParseRequest: User Input
    ParseRequest --> IdentifyTicker: Mention Stock?
    IdentifyTicker --> CallTool: Found Ticker (e.g., AAPL)
    CallTool --> FetchAPI: GET /tool/stock_price
    FetchAPI --> CallTool: JSON Data (Finnhub)
    CallTool --> GenerateResponse: Pass Data to LLM
    GenerateResponse --> Idle: Reply to User
    ParseRequest --> GeneralChat: No Stock Mentioned
    GeneralChat --> Idle
Workflow:

User Request: User asks "How is Apple price?"

LLM Decision: Recognizes intent and translates "Apple" -> "AAPL".

Tool Execution: OpenWebUI calls the local FastAPI server (http://host.docker.internal:8787).

External API: FastAPI fetches live data from Finnhub.

Response: LLM formats the JSON result into a natural language response.

Installation (安裝教學)
Prerequisites (前置需求)
Python 3.9+

Finnhub API Key (Free tier is sufficient)

Docker (for OpenWebUI)

1. Clone the repository
Bash

git clone [https://github.com/YOUR_USERNAME/LLM-Stock-Agent.git](https://github.com/YOUR_USERNAME/LLM-Stock-Agent.git)
cd LLM-Stock-Agent
2. Install dependencies
Bash

pip install -r requirements.txt
3. Configure API Key
Open stock_server.py and replace the placeholder with your Finnhub API Key. (Security Note: For production, use environment variables.)

Python

# In stock_server.py
FINNHUB_API_KEY = "YOUR_FINNHUB_API_KEY_HERE"
4. Start the Tool Server
Bash

python stock_server.py
Expected output:

INFO: Uvicorn running on http://0.0.0.0:8787

OpenWebUI Setup (前端設定)
要讓 OpenWebUI 連接此工具，請依照以下步驟設定：

Go to Workspace -> Tools -> Create Tool (+)

Name: get_stock_price

Description:

Retrieves real-time stock quotes from Finnhub. Use this tool when the user asks for stock info. Requires a valid ticker (e.g. 'AAPL').

Tool Code: Copy and paste the following Python code into the OpenWebUI editor. This script acts as the bridge between OpenWebUI and your local FastAPI server.

Python

import requests
import json

class Tools:
    def __init__(self):
        pass

    def get_stock_price(self, ticker: str) -> str:
        """
        Get the real-time stock price for a given ticker.
        :param ticker: The stock ticker symbol (e.g. AAPL, NVDA, 2330.TW)
        """
        # Connect to the local FastAPI server
        # 'host.docker.internal' is required if OpenWebUI is running inside Docker
        url = f"[http://host.docker.internal:8787/tool/stock_price?ticker=](http://host.docker.internal:8787/tool/stock_price?ticker=){ticker}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return json.dumps(response.json(), ensure_ascii=False)
        except Exception as e:
            return f"Error: Unable to fetch data. Details: {str(e)}"
Usage Demo (使用範例)
System Prompt (Recommended):

You are a financial assistant. If the user mentions a company name, convert it to their stock ticker (e.g. Apple -> AAPL, TSMC -> 2330.TW) and use the get_stock_price tool.

Scenario:

User: "幫我看台積電現在多少錢"

Agent (Internal Thought): User mentioned '台積電', converting to '2330.TW'... Calling tool get_stock_price(ticker='2330.TW')

Tool Output:

JSON

{
  "result": "2330.TW 最新成交價: 1080.0 TWD (資料來源: Finnhub)",
  "price": 1080.0,
  "currency": "TWD",
  "change_percent": "1.5%"
}
Agent Response: "台積電 (2330.TW) 目前股價為 1080.0 TWD，今日漲幅約 1.5%。(資料來源: Finnhub)"

License
This project is created for the NCKU TOC 2025 Course.
