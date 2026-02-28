# 股價回撤監控通知系統（GitHub Actions + LINE Messaging API）

## 專案簡介
部署於 GitHub Actions，每星期一到五早上 08:30 從 yfinance 抓取美股代號VT、VEA、GSPC及台股0050、2330的前一交易日價格資料，並追蹤各標的自前一相對高點的回撤幅度（drawdown），每下跌5%時，即自動透過 LINE Messaging API 發送通知到群組。

## 系統流程
GitHub Actions 排程觸發 → Python 腳本執行 → 抓取 yfinance 股價資料 → 讀取 Records.json 歷史資料 → 更新高點並計算回撤 → (發送 LINE 通知) → (將需更新資料寫回 Records.json)

## 主要專案結構
├── main.py: 主程式<br>
├── Records.json: 儲存各標股價高點、日期與通知門檻<br>
├── requirements.txt: 安裝套件清單<br>
└── .github/workflows<br>
&emsp;&emsp;└── drawdown-alert.yml: GitHub Actions排程設定

## 使用技術
- Python
- yfinance
- LINE Messaging API
- GitHub Actions
- JSON
