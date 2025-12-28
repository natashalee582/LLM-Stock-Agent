# LLM Stock Agent 📈

這是一個基於 OpenWebUI 與 FastAPI 的即時股價查詢 Agent。
透過整合 Finnhub API，讓 LLM 能夠即時獲取台美股（如 AAPL, 2330.TW）的最新價格資訊。

## 功能特色
- **即時數據**：串接 Finnhub API，不需依賴不穩定的爬蟲。
- **自動判斷**：LLM 自動將公司名稱（如「台積電」）轉換為代號（2330.TW）。
- **微服務架構**：工具端獨立為 FastAPI Server，符合 Agent 設計模式。

## 安裝與執行

### 1. 安裝套件
```bash
pip install -r requirements.txt
