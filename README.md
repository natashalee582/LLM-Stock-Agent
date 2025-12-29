# LLM Stock Agent (Real-time Market Tracker)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-orange)](https://docs.openwebui.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

> A robust, microservice-based LLM Agent capable of retrieving real-time stock data, analyzing news sentiment, and providing technical chart links.

這是一個基於 **OpenWebUI** (前端/推理) 與 **FastAPI** (後端工具) 的智慧股市 Agent。整合 **Finnhub API** 與 **TradingView**，具備即時報價、多股比較、新聞情緒分析與技術線圖導引功能。

---

## Key Features (功能亮點)

1.  **Real-time Data & News**: 
    * 串接 Finnhub 金融級 API，提供即時股價 (Price) 與即時新聞 (News)。
2.  **AI Sentiment Analysis**: 
    * LLM 會自動閱讀最新財經新聞，分析並判斷市場情緒為 **Bullish (利多)** 或 **Bearish (利空)**。
3.  **Multi-Stock Comparison**: 
    * 支援一次比較多檔股票（例如："Compare NVDA and AMD"），自動生成比較表格。
4.  **Smart Fallback Mechanism**: 
    * 內建 Mock 救援機制，當 API 額度耗盡或查詢非美股數據不穩時，自動切換至模擬模式，確保 Demo 流程 100% 穩定。

---

## Installation

1. Prerequisites
   **Python 3.9+**
   **Finnhub API Key (Free tier)**
   **Docker (for OpenWebUI)**

2. Clone the repository
   ```bash
   git clone https://github.com/natashalee582/LLM-Stock-Agent.git
   cd LLM-Stock-Agent
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Configure API Key
   Open stock_server.py and replace the placeholder with your Finnhub API Key.           (Security Note: For production, use environment variables.)
   ```bash
   FINNHUB_API_KEY = "YOUR_FINNHUB_API_KEY_HERE"
   ```

7. Start the Tool Server
   ```bash
   python stock_server.py
   ```
   Server will start at http://0.0.0.0:8787
   
---

## OpenWebUI Setup (前端設定)

1. Create Tool
   * Go to Workspace -> Tools -> Create Tool (+).
   * Name: get_stock_price
   * Description: Retrieves real-time stock data, news, and chart links.
   * Code: (Paste the code below)
     ```python
      import requests
      import json
      
      class Tools:
          def __init__(self):
              pass
      
          def get_stock_price(self, ticker: str) -> str:
              """
              Get stock price, news, and chart link. Supports multiple tickers separated by comma.
              :param ticker: The stock ticker symbol(s) (e.g. 'AAPL' or 'NVDA, AMD')
              """
              # Connect to the local FastAPI server
              # 'host.docker.internal' is used to access the host machine from inside the Docker container
              url = f"http://host.docker.internal:8787/tool/stock_price?ticker={ticker}"
              
              try:
                  response = requests.get(url, timeout=10)
                  response.raise_for_status()
                  return json.dumps(response.json(), ensure_ascii=False)
              except Exception as e:
                  return f"Error: {str(e)}"
      ```
  
2. System Prompt
   You are a professional financial analyst.

   **Tool Usage:**
   1. Use `get_stock_price` to fetch data.
   2. If comparing multiple stocks, pass them as a comma-separated list (e.g., `ticker='NVDA, AMD'`).
   
   **Response Format:**
   
   ### Stock Analysis
   (If multiple stocks, use a comparison table. If single, use a standard table.)
   
   | Feature | {Stock A} | ... |
   | :--- | :--- | :--- |
   | **Price** | **{price}** | ... |
   | Change | {change} 📈 | ... |
   | Sentiment | 🟢 Bullish | ... |
   
   **Analysis:**
   * Briefly summarize the news and your verdict.

---

## Usage Examples
1. 基礎查詢 (Basic Inquiry)

   User: "How is Nvidia doing?" Agent: Shows NVDA price table, bullish sentiment analysis, and a link to the K-line chart.

2. 多股比較 (Comparison)

   User: "Compare Tesla and Ford." Agent: Generates a comparison table showing TSLA vs. F, contrasting their market performance.

3. 台股救援模式 (Fallback Demo)

   User: "幫我看台積電 (2330)" Agent: Activates simulated data mode (due to API limits), presenting a realistic analysis of TSMC.

---

## Architecture (系統架構)

本專案實作了具備 **Complex Task Decomposition** 能力的 Agent：

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> ParseRequest: User Input
    ParseRequest --> IdentifyIntent: Stock Analysis?
    IdentifyIntent --> SingleStock: "Check Apple"
    IdentifyIntent --> MultiStock: "Compare NVDA & AMD"
    
    SingleStock --> CallTool: GET /tool/stock_price (ticker='AAPL')
    MultiStock --> CallTool: GET /tool/stock_price (ticker='NVDA,AMD')
    
    CallTool --> FetchAPI: Finnhub API / TradingView Link
    FetchAPI --> CallTool: JSON Data (Price + News + Chart)
    
    CallTool --> Analysis: LLM Analyzes Sentiment
    Analysis --> GenerateTable: Create Markdown Table
    GenerateTable --> Idle: Response with Chart Link
