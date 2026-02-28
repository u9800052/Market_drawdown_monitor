#股價回撤監控通知系統（GitHub Actions + LINE Messaging API）

##專案簡介
部署於 GitHub Actions，每周一到五早上08:30於yfinance抓取美股代號VT、VEA、GSPC及台股0050、2330前一日的價格資料，並追蹤各標的自前相對高點的回撤幅度（drawdown），每下跌5%時，即自動透過LINE Messaging API發送通知到群組。

##系統流程
GitHub Actions排程觸發 → Python腳本執行 → 抓取yfinance股價資料 → 讀取Records.json歷史資料 → 更新高點並計算回撤 → (發送LINE通知) → (將需更新資料寫回Records.json)

##專案結構
├── main.py: 主程式
├── Records.json: 儲存各標股價高點、日期與通知門檻
├── requirements.txt: 安裝套件清單
└── .github/workflows
    └── drawdown-alert.yml: GitHub Actions排程設定

##使用技術
Python
yfinance
LINE Messaging API
GitHub Actions
JSON
