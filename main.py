import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
import json
import os
import sys
from linebot import LineBotApi
from linebot.models import TextSendMessage

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
USER_ID = os.getenv('USER_ID')

def send_line_message(msg):
    try:
        # 確保 Token 存在才執行，避免 NoneType 錯誤
        if not CHANNEL_ACCESS_TOKEN or not USER_ID:
            print("Error: LINE Environment variables not set.")
            return
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        message = TextSendMessage(text=msg)
        line_bot_api.push_message(USER_ID, message)
    except Exception as e:
        print(f"LINE Message Error: {e}")

tickers = ["VT", "^GSPC", "0050.TW", "2330.TW", "CIBR"]
try:
    df = yf.download(tickers, period="5d", auto_adjust=True, group_by='column')  
    if df.empty:
        raise ValueError("YFinance returned empty dataframe")
        
except Exception as e:
    send_line_message(f"無法抓取股價資料: {e}")
    sys.exit(1)

try:
    with open('Records.json', 'r+', encoding='utf-8') as f:
        recs = json.load(f)
        data_changed = False

        for ticker in tickers:
            stock = recs[ticker]
            daily_high = float(df['High'][ticker].dropna().tail(1).iloc[0])
            daily_low = float(df['Low'][ticker].dropna().tail(1).iloc[0])
            drawdown = (daily_low - stock['High']) / stock['High']

            if daily_high >= stock['High']:
                now = datetime.now()
                stock['Date'] = df['High'][ticker].dropna().tail(1).index[-1].strftime("%Y-%m-%d")

                stock['High'] = daily_high
                stock['Threshold'] = -0.05
                stock['Notified'] = False
                data_changed = True

            if drawdown <= stock['Threshold']:
                send_line_message(f"前一交易日「{ticker}」自前高點回撤「{drawdown*100:.2f}%」，下跌超過{stock['Threshold']:.2f}%，考慮買進！")
                stock['Notified'] = True
                stock['Threshold'] -= 0.05
                data_changed = True
            
        # 寫入json檔
        if data_changed:
            f.seek(0)
            json.dump(recs, f, ensure_ascii=False, indent=4)
            f.truncate()
except Exception as e:
    print(f"Script Error: {e}")
    send_line_message(f'Github Actions 執行發生錯誤:\n{str(e)}')
    sys.exit(1)