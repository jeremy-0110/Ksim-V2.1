# data_manager.py
# 負責獲取 Yahoo Finance 數據與計算技術指標

import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime
import random
import config  # 導入配置檔

# --- 技術指標計算 ---

def calculate_rsi(data: pd.DataFrame, window: int = 14) -> pd.Series:
    """計算 RSI (Wilder's Smoothing)"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0))
    loss = (-delta.where(delta < 0, 0))
    
    avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
    avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- 資料獲取與處理 (ETL) ---

@st.cache_data(ttl=3600, show_spinner="📈 正在載入並計算指標 (MA, RSI)...")
def fetch_historical_data(ticker: str = "TSLA") -> pd.DataFrame | None:
    """從 Yahoo Finance 下載歷史數據並進行預處理"""
    period = 'max'

    try:
        data = yf.download(ticker.upper(), period=period, interval='1d', progress=False)
        
        if data.empty:
            return None
            
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']].reset_index()
        data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data['Date'] = pd.to_datetime(data['Date'])
        
        for p in config.MA_PERIODS:
            data[f'MA{p}'] = data['Close'].rolling(window=p).mean()
            
        data['RSI'] = calculate_rsi(data, window=14)
        
        data.dropna(inplace=True) 
        data = data.reset_index(drop=True)
        return data

    except Exception as e:
        st.error(f"數據載入錯誤: {e}")
        return None
    
# --- 模擬輔助函式 ---

def select_random_start_index(data: pd.DataFrame) -> tuple[int, int] | None:
    """
    隨機挑選一段歷史區間
    """
    total_days = len(data)
    
    # 計算需要的最少總天數 = 觀察期 + 模擬期
    required_days = config.INITIAL_OBSERVATION_DAYS + config.MIN_SIMULATION_DAYS
    
    if total_days < config.INITIAL_OBSERVATION_DAYS:
         return None
         
    # 如果資料剛好只夠跑一點點
    if total_days < required_days:
        max_start_index = total_days - config.INITIAL_OBSERVATION_DAYS
        start_view_index = 0
        # 模擬起始點 = 起始索引 + 觀察期
        sim_start_index = start_view_index + config.INITIAL_OBSERVATION_DAYS
        
        return start_view_index, sim_start_index
    
    # 正常情況
    max_start_index = total_days - required_days
    
    start_view_index = random.randint(0, max_start_index)
    sim_start_index = start_view_index + config.INITIAL_OBSERVATION_DAYS
    
    return start_view_index, sim_start_index

def get_price_info_by_index(data: pd.DataFrame, index: int) -> tuple[datetime, float, float]:
    """根據索引取得某一天的價格資訊"""
    if data is not None and index < len(data):
        current_row = data.iloc[index]
        
        date_timestamp = current_row['Date']
        if isinstance(date_timestamp, pd.Series):
             date_timestamp = date_timestamp.iloc[0]
        
        date = pd.to_datetime(date_timestamp).to_pydatetime()
        
        open_price = current_row['Open'].item() if hasattr(current_row['Open'], 'item') else current_row['Open']
        close_price = current_row['Close'].item() if hasattr(current_row['Close'], 'item') else current_row['Close']
        
        return date, open_price, close_price

    return datetime.now(), 0.0, 0.0
