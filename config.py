# config.py
# 用於存放全域常數、交易規則與設定

# --- 回測參數 (Backtest Parameters) ---
VIEW_DAYS = 100                # 圖表可視範圍 (天)：決定圖表預設顯示多寬，設 100 讓 K 線比較清楚
INITIAL_OBSERVATION_DAYS = 250 # 初始觀察期 (天)：模擬開始前保留的天數 (為了讓 MA120 等長天期指標能算出來)

MIN_SIMULATION_DAYS = 720      # 最少需要多少天數據才能跑模擬
MA_PERIODS = [5, 10, 20, 60, 120]  # 移動平均線週期

# --- 預設值 (Defaults) ---
DEFAULT_TICKER = "TSLA"      # 預設載入的股票代號
INITIAL_CAPITAL = 100000.0   # 初始本金 (USD)

# --- 圖表顏色配置 (Moving Average Colors) ---
MA_COLORS = {
    5: 'lightgray', 
    10: 'gray', 
    20: 'red',      
    60: 'blue',     
    120: 'white'    
}

# --- 交易費率設定 (Transaction Fees) ---
FEE_RATE = 0.005           # 現貨手續費 (0.5%)
LEVERAGE_FEE_RATE = 0.01   # 槓桿手續費 (1%)
MIN_MARGIN_RATE = 0.05     # 最小保證金比例 (5%)

# --- 資產類型配置 (Asset Configurations) ---
ASSET_CONFIGS = {
    'Stock': {
        'unit': '股', 
        'mode_spot': '現貨',          
        'mode_margin_long': '融資',   
        'mode_margin_short': '融券',  
        'default_qty': 1000.0, 
        'min_qty': 1.0
    }, 
    'Forex': {
        'unit': '點', 
        'mode_spot': '現貨',          
        'mode_margin_long': '做多',   
        'mode_margin_short': '做空',  
        'default_qty': 100.0, 
        'min_qty': 100.0
    }, 
    'Crypto': {
        'unit': '顆', 
        'mode_spot': '現貨',          
        'mode_margin_long': '合約做多', 
        'mode_margin_short': '合約做空', 
        'default_qty': 1.0, 
        'min_qty': 0.001
    }
}

# --- 輔助集合：用於邏輯判斷 ---
LONG_MODES = {'現貨', '融資', '做多', '合約做多'}
SHORT_MODES = {'融券', '做空', '合約做空'}
LEVERAGE_MODES = {'融資', '融券', '做多', '做空', '合約做多', '合約做空'}

# --- 交易模式映射表 ---
TRADE_MODE_MAP = {
    'Spot_Buy': {
        'type': 'Spot', 
        'direction': 'Long'
    },
    'Margin_Long': {
        'type': 'Margin', 
        'direction': 'Long'
    },
    'Margin_Short': {
        'type': 'Margin', 
        'direction': 'Short'
    },
}