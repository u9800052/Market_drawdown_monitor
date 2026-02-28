# Stock Price Drawdown Monitoring & Notification System (股價回撤監控通知系統）

## Project Overview (專案簡介)
This project is a scheduled stock price drawdown monitoring system deployed using GitHub Actions.

Every weekday (Monday–Friday) at 08:30 AM, the system:

* Retrieves the previous trading day's price data via yfinance

* Tracks the drawdown from the most recent relative high for the following assets:

  \- US Market: VT, VEA, GSPC (S&P 500 Index)

  \- Taiwan Market: 0050, 2330 (TSMC)

* Calculates the percentage drawdown from the latest peak

* Sends a LINE notification whenever the drawdown reaches a new 5% interval (e.g., -5%, -10%, -15%, etc.)
This allows systematic monitoring of market corrections without manual tracking.
>此專案部署於 GitHub Actions，每星期一到五早上 08:30 從 yfinance 抓取美股代號VT、VEA、GSPC及台股0050、2330的前一交易日價格資料，並追蹤各標的自前一相對高點的回撤幅度（drawdown），每下跌5%時，即自動透過 LINE Messaging API 發送通知到群組。
---
## System Workflow (系統流程)

GitHub Actions (Scheduled Trigger)
→ Python Script Execution
→ Fetch Stock Data from yfinance
→ Load Historical Records (Records.json)
→ Update Peak Price & Calculate Drawdown
→ Send LINE Notification (if threshold reached)
→ Write Updated Data Back to Records.json

>GitHub Actions 排程觸發 → Python 腳本執行 → 抓取 yfinance 股價資料 → 讀取 Records.json 歷史資料 → 更新高點並計算回撤 → (發送 LINE 通知) → (將需更新資料寫回 Records.json)
---
##  Project Structure (主要專案結構)
├── main.py: Main execution script:data fetch, calculation, notification logic (主程式)<br>
├── Records.json: Stores peak price, date, and notification thresholds for each asset (儲存各標的股價高點、日期與通知門檻)<br>
├── requirements.txt: Python dependency list (安裝套件清單)<br>
└── .github/workflows<br>
&emsp;&emsp;└── drawdown-alert.yml: GitHub Actions scheduling configuration (排程設定)

## Technologies Used (使用技術)
- Python: Core scripting language
- yfinance: Financial data retrieval
- LINE Messaging API: Notification delivery system
- GitHub Actions: CI/CD scheduling and automation
- JSON: Lightweight state storage for peak tracking
