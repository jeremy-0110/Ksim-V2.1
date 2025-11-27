# Ksim V2.1 - 智慧型多資產交易回測系統 (AI-Assisted Trading Simulator)

Ksim V2.1 是一個基於 **Python** 與 **Streamlit** 架構的互動式金融回測引擎。

本專案不僅是一個交易模擬器，更是一個展示軟體架構重構 (Refactoring) 與 AI 輔助開發 (AI-Assisted Development) 的實作案例。

> （連 README 也是 AI 輸出的，如果有相關回饋可以加我 DC）

---

## 🔗 線上體驗 Demo
https://ksimv2-1.streamlit.app

## 💬 加入討論 (Discord)
https://discord.gg/VZmRthTF

---

## 🚀 專案背景

Ksim 的初衷是建立一個能驗證交易邏輯的無風險沙盒，專注於雲端服務、金融市場與數據分析的實作應用。

---

## 🤖 AI 協作開發模式 (Human-AI Collaboration)

本專案採用 **「人類設計邏輯，AI 実作架構」** 的開發模式：

### Design (我)
- 定義金融交易規則（如保證金計算、強制平倉邏輯）
- 介面需求與系統變數設計（如觀測期與可視範圍分離）

### Implementation (Gemini)
- 協助撰寫 Python 程式碼
- 偵測邏輯漏洞（Debug）
- 優化數據處理效率
- 協助進行模組化拆分

---

## 🔄 架構重構 (Refactoring)

### V2 版本 (Legacy)

初期僅由 app.py (介面) 與 data_manager.py (資料) 組成。

**缺點：**
- 隨著功能增加（如槓桿、圖表），程式碼過於臃腫
- 邏輯與 UI 耦合度高
- 難以維護

### V2.1 版本 (Current)

為了提升系統的可維護性與擴充性，我將系統拆分為 **5 個獨立模組**。

採用類似 MVC (Model-View-Controller) 的設計思維，讓資料流更清晰。

---

## 📂 系統模組結構

**app.py (Frontend / Controller)**  
主程式入口。負責 UI 渲染、處理使用者互動 (按鈕/輸入)，並調用後端邏輯。

**logic.py (Backend Logic)**  
核心交易引擎。處理資金計算、訂單撮合、保證金維持率檢測、強制平倉 (Liquidation) 邏輯。

**charts.py (Visualization)**  
視覺化模組。使用 Plotly 製作 K 線、MA 均線、動態價格標籤與指標顯示。

**data_manager.py (Data / ETL)**  
資料處理層。負責串接 Yahoo Finance API，進行資料清洗與技術指標 (RSI, MA) 計算。

**config.py (Configuration)**  
全域配置檔。集中管理所有參數（手續費率、槓桿限制、MA 週期）方便一次性調整系統規則。

---

## ✨ 核心功能介紹

### 1. 多資產支援 (Multi-Asset Support)

支援三種截然不同的金融商品，並自動套用最小交易單位與代碼規則：

📈 **股票 (Stock)**：TSLA, NVDA（單位：股）  
💱 **外匯 (Forex)**：JPY=X, EURUSD=X（單位：點）  
₿ **加密貨幣 (Crypto)**：BTC-USD, ETH-USD（單位：顆）

---

### 2. 進階模擬機制 (Advanced Simulation)

#### 觀測期與視野分離
- **初始觀測期 (Observation)**：預跑 250 天確保長天期均線如 MA120 正確  
- **圖表可視範圍 (View)**：僅展示最近 100 天，避免 K 線壓縮、提升視覺品質

#### 保證金交易 (Margin Trading)
- 槓桿範圍 **1x ~ 20x**
- 內建 **做空 (Shorting)** 支援

#### 風險控管
- 即時計算維持保證金  
- 低於條件自動觸發 **強制平倉**

---

### 3. 視覺化互動圖表

使用 Plotly 製作專業互動圖表，支援：
- 持倉成本線
- 止損 (SL) / 止盈 (TP) 線
- 優化標籤位置與動態顯示

---

## 🛠️ 本地安裝與執行 (Local Installation)

### 1. 環境需求
- Python **3.10 或以上**（建議 3.13）

### 2. 安裝依賴套件

```
pip install streamlit pandas numpy yfinance plotly
```

### 3. 執行程式

```
streamlit run app.py
```

執行後瀏覽器將自動開啟介面（預設網址）：

```
http://localhost:8501
```

---

**Powered by Python & Gemini AI**
