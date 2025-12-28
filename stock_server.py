# 檔案名稱：stock_server.py
import requests
from fastapi import FastAPI
import uvicorn

app = FastAPI()

# 【請將這裡換成你剛剛申請到的 Key】
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "YOUR_FINNHUB_API_KEY_HERE")

@app.get("/tool/stock_price")
def get_stock_price(ticker: str):
    # 1. 處理代號
    ticker_clean = ticker.upper().strip()
    
    # 針對台股做特殊處理：Finnhub 的台股代號格式是 "2330.TW"
    # 如果使用者輸入 "2330"，我們幫他補上 ".TW"
    if ticker_clean.isdigit() or (ticker_clean.startswith("2") and len(ticker_clean) == 4):
         if not ticker_clean.endswith(".TW"):
             ticker_clean += ".TW"
    
    print(f"收到查詢請求: {ticker_clean}")

    try:
        # 2. 呼叫 Finnhub API (這是真正的即時數據)
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker_clean}&token={FINNHUB_API_KEY}"
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # Finnhub 回傳格式: {"c": 現價, "d": 漲跌, "dp": 漲跌幅, ...}
        # 如果代號錯誤，它通常會回傳 c: 0
        current_price = data.get("c", 0)
        
        if current_price == 0:
             return {"error": f"找不到 {ticker_clean} 的股價，請確認代號是否正確。"}

        # 3. 判斷幣別 (Finnhub 不直接回傳幣別，我們用代號判斷)
        currency = "TWD" if ".TW" in ticker_clean else "USD"

        return {
            "result": f"{ticker_clean} 即時現價: {current_price} {currency} (來源: Finnhub)",
            "price": current_price,
            "currency": currency,
            "change_percent": f"{data.get('dp', 0)}%"
        }

    except Exception as e:
        print(f"API 錯誤: {e}")
        return {"error": "無法連線到金融數據中心"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8787)
