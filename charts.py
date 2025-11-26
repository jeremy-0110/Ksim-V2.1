# charts.py
# 負責繪製 Plotly 圖表 (K線、MA、Volume、RSI)

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config
import numpy as np
import pandas as pd

def render_main_chart(ticker, core_data, current_idx, positions, end_sim_index_on_settle, saved_layout=None):
    """
    繪製主圖表
    """
    display_start_idx = 0 
    display_end_idx = current_idx + 1
    
    data_to_display = core_data.iloc[display_start_idx : display_end_idx].copy()
    data_to_display['DateStr'] = data_to_display['Date'].dt.strftime('%Y-%m-%d')
    x_axis_data = data_to_display['DateStr']

    last_visible_date = x_axis_data.iloc[-1]

    # --- Y 軸動態範圍計算 (Visual Scaling) ---
    view_window_data = data_to_display.iloc[-config.VIEW_DAYS:] if len(data_to_display) > config.VIEW_DAYS else data_to_display
    
    if not view_window_data.empty:
        price_min = view_window_data['Low'].min()
        price_max = view_window_data['High'].max()
        padding = (price_max - price_min) * 0.1 
        y_range_min = max(0.0001, price_min - padding)
        y_range_max = price_max + padding
        if y_range_max <= y_range_min: y_range_max = y_range_min * 1.1
    else:
        y_range_min, y_range_max = 1, 100

    # 建立子圖
    fig = make_subplots(
        rows=3, cols=1, 
        row_heights=[0.6, 0.2, 0.2], 
        shared_xaxes=True, 
        vertical_spacing=0.03,
        subplot_titles=(f"{ticker} 日線 (Log)", "成交量", "RSI(14)") 
    )

    # 1. K線圖
    fig.add_trace(go.Candlestick(
        x=x_axis_data, 
        open=data_to_display['Open'], high=data_to_display['High'],
        low=data_to_display['Low'], close=data_to_display['Close'], 
        name='K-Line'
    ), row=1, col=1)

    # 2. MA 線
    for p_ma in config.MA_PERIODS:
        if f'MA{p_ma}' in data_to_display.columns:
            fig.add_trace(go.Scatter(
                x=x_axis_data, y=data_to_display[f'MA{p_ma}'], mode='lines', 
                name=f'MA{p_ma}', line=dict(color=config.MA_COLORS.get(p_ma, 'gray'), width=1)
            ), row=1, col=1) 
        
    # --- 繪製輔助線與標籤 ---
    for pos in positions:
        is_spot = (pos['display_name'] == '現貨')
        has_sl_tp = (pos['sl'] > 0 or pos['tp'] > 0)
        if is_spot and not has_sl_tp: continue

        lines_to_plot = {'開倉': {'price': pos['cost'], 'color': 'yellow', 'dash': 'dot'}}
        
        is_long = pos['display_name'] in config.LONG_MODES
        dir_str = '多' if is_long else '空'
        
        if pos.get('liquidation_price', 0) > 0:
            lines_to_plot['強平'] = {'price': pos['liquidation_price'], 'color': 'red', 'dash': 'dash'}
        if pos['sl'] > 0:
            lines_to_plot['止損'] = {'price': pos['sl'], 'color': 'red', 'dash': 'dot'}
        if pos['tp'] > 0:
            lines_to_plot['止盈'] = {'price': pos['tp'], 'color': 'green', 'dash': 'dot'}

        for name, info in lines_to_plot.items():
            price = info['price']
            if price <= 0: continue
            
            fig.add_hline(y=price, line_width=1, line_dash=info['dash'], line_color=info['color'], row=1, col=1)
            
            label_text = f"  {dir_str}{name} {price:,.2f}"
            fig.add_trace(go.Scatter(
                x=[last_visible_date], y=[price], text=[label_text], mode="text",
                textposition="middle right", textfont=dict(color=info['color'], size=12, family="Roboto, Arial, sans-serif"),
                cliponaxis=False, showlegend=False, hoverinfo='skip'
            ), row=1, col=1)

    # 3. Volume & RSI
    fig.add_trace(go.Bar(x=x_axis_data, y=data_to_display['Volume'], marker_color='grey', name='Volume'), row=2, col=1)
    fig.add_trace(go.Scatter(x=x_axis_data, y=data_to_display['RSI'], line=dict(color='orange'), name='RSI'), row=3, col=1)
    
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    # 垂直線 (模擬起點與終點)
    if end_sim_index_on_settle:
        try:
            start_abs_idx = config.INITIAL_OBSERVATION_DAYS
            end_abs_idx = end_sim_index_on_settle
            if start_abs_idx < len(x_axis_data):
                fig.add_vline(x=x_axis_data.iloc[start_abs_idx], line_dash="dot", line_color="green", row=1, col=1)
            if end_abs_idx < len(x_axis_data):
                fig.add_vline(x=x_axis_data.iloc[end_abs_idx], line_dash="dot", line_color="white", row=1, col=1)
        except:
            pass

    # --- 視角層 (View Range) ---
    # 這裡定義了使用者一開始看到的圖表「寬度」
    initial_range = None
    if end_sim_index_on_settle is not None:
        initial_range = None 
    else:
        total_len = len(x_axis_data)
        end_idx = total_len - 1
        start_idx = max(0, end_idx - config.VIEW_DAYS)
        initial_range = [start_idx - 0.5, end_idx + 0.5]

    common_font = "Roboto, Arial, sans-serif"
    invisible_text = '\u200b' 

    fig.update_xaxes(
        type='category', showticklabels=False, range=initial_range, rangeslider=dict(visible=False) 
    )
    
    fig.update_layout(
        template="plotly_dark", height=700, showlegend=False, dragmode='pan', hovermode='x unified', 
        font=dict(family=common_font),
        margin=dict(t=30, b=30, l=50, r=120), 
        xaxis=dict(unifiedhovertitle=dict(text=invisible_text)),
        xaxis2=dict(unifiedhovertitle=dict(text=invisible_text)),
        xaxis3=dict(unifiedhovertitle=dict(text=invisible_text)),
        yaxis=dict(side='right', type='log', range=[np.log10(y_range_min), np.log10(y_range_max)], fixedrange=False),
        yaxis2=dict(side='right'),
        yaxis3=dict(side='right')
    )
    
    return fig