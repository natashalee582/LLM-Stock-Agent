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
4.  **K-Line Chart Integration**: 
    * 自動生成 **TradingView K 線圖**連結，點擊即可查看專業技術線圖。
5.  **Smart Fallback Mechanism**: 
    * 內建 Mock 救援機制，當 API 額度耗盡或查詢非美股數據不穩時，自動切換至模擬模式，確保 Demo 流程 100% 穩定。

---

## Architecture & FSM（系統架構與狀態機）

本專案實作了典型的 **Agent 狀態機邏輯（Finite State Machine, FSM）**：

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
