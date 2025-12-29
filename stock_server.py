# 檔案名稱：stock_server.py
import requests
import random
import os
import datetime
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 請填入你的 Finnhub Key
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "YOUR_FINNHUB_API_KEY_HERE")

# --- 核心邏輯：處理單一股票 (原本的邏輯封裝到這裡) ---
def fetch_single_stock_data(ticker):
    ticker_clean = ticker.upper().strip()
    
    # 處理台股代號
    if ticker_clean.isdigit() or (ticker_clean.startswith("2") and len(ticker_clean) == 4):
         if not ticker_clean.endswith(".TW"):
             ticker_clean += ".TW"

    print(f"處理單一股票: {ticker_clean}")

    try:
        # 1. 嘗試抓取真實股價
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker_clean}&token={FINNHUB_API_KEY}"
        response = requests.get(url, timeout=5)
        data = response.json()
        c = data.get("c", 0)
        
        # 如果沒股價，轉入救援模式
        if c == 0:
            return generate_mock_data(ticker_clean)

        # 2. 嘗試抓取真實新聞 (最近 5 天)
        news_list = []
        try:
            today = datetime.date.today().isoformat()
            week_ago = (datetime.date.today() - datetime.timedelta(days=5)).isoformat()
            news_url = f"https://finnhub.io/api/v1/company-news?symbol={ticker_clean}&from={week_ago}&to={today}&token={FINNHUB_API_KEY}"
            news_resp = requests.get(news_url, timeout=3) # 新聞不需要等太久
            news_data = news_resp.json()
            
            for item in news_data[:2]: # 比較模式下，新聞少一點，每家取 2 則就好
                news_list.append(f"- {item['headline']}")
        except:
            news_list = []

        if not news_list:
            news_list = [
                f"- Market analysis shows momentum for {ticker_clean}.",
                "- Investors watching upcoming reports."
            ]

        return {
            "symbol": ticker_clean,
            "price": c,
            "change": data.get("d"),
            "percent": data.get("dp"),
            "high": data.get("h"),
            "low": data.get("l"),
            "currency": "TWD" if ".TW" in ticker_clean else "USD",
            "source": "Finnhub API",
            "news_headlines": "\n".join(news_list)
        }

    except Exception as e:
        print(f"錯誤: {e}")
        return generate_mock_data(ticker_clean)

# --- 救援函式 (保持不變) ---
def generate_mock_data(ticker):
    base_price = 1080.0 if "2330" in ticker else random.uniform(50, 500)
    price = round(base_price * random.uniform(0.98, 1.05), 2)
    
    if "2330" in ticker or "TSMC" in ticker:
        mock_news = ["- TSMC announces 2nm breakthrough.", "- Strong AI chip demand."]
    else:
        mock_news = [f"- {ticker} revenue exceeds expectations.", "- Analysts upgrade rating."]

    return {
        "symbol": ticker,
        "price": price,
        "change": round(price - base_price, 2),
        "percent": round(((price - base_price)/base_price)*100, 2),
        "high": round(price * 1.01, 2),
        "low": round(price * 0.99, 2),
        "currency": "TWD" if ".TW" in ticker else "USD",
        "source": "Simulated (Backup)",
        "news_headlines": "\n".join(mock_news)
    }

# --- API 入口：支援逗號分隔多股查詢 ---
@app.get("/tool/stock_price")
def get_stock_price(ticker: str):
    # 這裡將輸入字串 "AAPL,TSLA" 切割成 ["AAPL", "TSLA"]
    tickers = [t.strip() for t in ticker.split(',')]
    
    results = []
    for t in tickers:
        if t: # 避免空字串
            result = fetch_single_stock_data(t)
            results.append(result)
            
    return {"results": results} # 回傳一個包含多個結果的 List

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8787)
