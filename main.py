import yfinance as yf
from datetime import datetime
import json
import os
import sys
from linebot import LineBotApi
from linebot.models import TextSendMessage

CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')

#傳送錯誤訊息給管理者
def send_error_message(msg):
    try:
        USER_ID = os.getenv('USER_ID')
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        message = TextSendMessage(text=msg)
        line_bot_api.push_message(USER_ID, message)
    except Exception as e:
        print(f"Failed to send error message: {e}")

#通知下跌訊息給所有成員    
def send_line_message(msg):
    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        message = TextSendMessage(text=msg)
        line_bot_api.broadcast(message)
    except Exception as e:
        print(f"Failed to send line message: {e}")
        send_error_message(f"Failed to send line message: {e}")

tickers = ["VT", "^GSPC", "0050.TW", "2330.TW", "VEA"] #注意須和json記錄檔中代號一樣
try:
    df = yf.download(tickers, period="5d", auto_adjust=True, group_by='column')  
    if df.empty:
        raise ValueError("YFinance returned empty dataframe")
        
except Exception as e:
    send_error_message(f"無法抓取YFinance股價資料: {e}")
    sys.exit(1)

try:
    with open('Records.json', 'r+', encoding='utf-8') as f:
        recs = json.load(f)
        data_changed = False

        for ticker in tickers:
            stock = recs[ticker] #讀取json紀錄檔中各個Tickers的資料
            daily_high = float(df['High'][ticker].dropna().tail(1).iloc[0])            

            #更新股價高點
            if daily_high > stock['High']:
                stock['Date'] = df['High'][ticker].dropna().tail(1).index[-1].strftime("%Y-%m-%d") #更新高點日期
                stock['High'] = daily_high
                stock['Threshold'] = -0.05 #重置通知門檻
                data_changed = True
            
            daily_low = float(df['Low'][ticker].dropna().tail(1).iloc[0])    
            drawdown = (daily_low - stock['High']) / stock['High']
            
            #判斷有無低於所設定的通知門檻
            if drawdown <= stock['Threshold']:
                send_line_message(f"前一交易日「{ticker}」自高點回撤「{drawdown*100:.2f}%」，下跌超過{stock['Threshold']*100:.0f}%，準備買進！")
                stock['Threshold'] -= 0.05 #下修下一次通知的門檻
                data_changed = True
            
        # 寫入json檔-
        if data_changed:
            f.seek(0)
            json.dump(recs, f, ensure_ascii=False, indent=4)
            f.truncate()
except Exception as e:
    print(f"Script Error: {e}")
    send_error_message(f'Github Actions 執行發生錯誤:\n{str(e)}')
    sys.exit(1)