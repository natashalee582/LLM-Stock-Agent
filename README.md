# 📈 LLM Stock Agent (Real-time Market Tracker)

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com/)
[![OpenWebUI](https://img.shields.io/badge/OpenWebUI-Compatible-orange)](https://docs.openwebui.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

> A robust, microservice-based LLM Agent capable of retrieving real-time stock market data via Finnhub API.

這是一個基於 **OpenWebUI**（前端 / 推理）與 **FastAPI**（後端工具）的智慧股市 Agent。  
透過串接 **Finnhub API**，讓 LLM 能夠即時查詢台美股（如 `AAPL`, `2330.TW`）的最新價格，並具備自然語言代號轉換能力。

---

## ✨ Features（功能特色）

- **Real-time Data Fetching**  
  使用 Finnhub 金融級 API，提供精確的即時股價、漲跌幅與幣別。

- **Smart Ticker Resolution**  
  利用 LLM 的推理能力，自動將公司名稱（如「台積電」、「Tesla」）轉換為正確的股票代號（`2330.TW`, `TSLA`）。

- **Microservice Architecture**  
  工具端獨立為 Python FastAPI Server，透過 RESTful API 與 OpenWebUI 溝通，符合 Agent 設計模式。

- **Docker Compatibility**  
  專為在 Docker 容器運行的 OpenWebUI 設計，支援 `host.docker.internal` 連線。

---

## 🏗️ Architecture & FSM（系統架構與狀態機）

本專案實作了典型的 **Agent 狀態機邏輯（Finite State Machine, FSM）**，符合 TOC 課程專題要求：

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
