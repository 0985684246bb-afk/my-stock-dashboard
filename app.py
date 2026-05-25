import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 網頁基本設定 (設定標題與寬度)
st.set_page_config(page_title="專屬自動化看盤室", layout="wide", page_icon="📈")

st.title("📊 自動化看盤儀表板")
st.write("即時追蹤核心觀測清單的價格與近期走勢。")
st.markdown("---")

# 2. 定義你要追蹤的標的清單
# 這裡使用的代號是 Yahoo Finance 上的標準代碼
tickers = {
    "📈 台股與美股 ETF": {
        "凱基台灣優選高股息 (009816)": "009816.TW",
        "嘉信美國大型成長股 ETF (SCHG)": "SCHG",
        "富邦台50 (006208)": "006208.TW",
        "國泰永續高股息 (00878)": "00878.TW",
        "元大高股息 (0056)": "0056.TW",
        "00403A": "00403A.TW",
        "VanEck Morningstar Wide Moat ETF": "MOAT"
    },
    "🪙 加密貨幣": {
        "RENDER": "RNDR-USD",
        "Chainlink": "LINK-USD",
        "Akash Network": "AKT-USD",
        "Bitcoin": "BTC-USD",
        "Ethereum": "ETH-USD",
        "Cardano": "ADA-USD"
    },
    "🔥 焦點個股": {  
        "華航 (2610)": "2610.TW",
        "台積電 (2330)": "2330.TW",
        "聯發科 (2454)": "2454.TW",
        "鴻海 (2317)": "2317.TW",
        "長榮航空 (2618)": "2618.TW",
        "NVIDIA": "NVDA",
        "Microsoft" : "MSFT",
    }
    "🛡️ 避險指標": {
        "黃金期貨 (Gold)": "GC=F",
        "恐慌指數 (VIX)": "^VIX",
        "美國10年期公債殖利率": "^TNX",
        "中華電信 (2412)": "2412.TW"
    }
}

# 3. 建立分類標籤頁 (Tabs)
tabs = st.tabs(list(tickers.keys()))

# 4. 抓取資料並繪製畫面的邏輯
for i, (category, assets) in enumerate(tickers.items()):
    with tabs[i]:
        # 根據標的數量自動分割欄位
        cols = st.columns(len(assets))
        
        for col, (name, symbol) in zip(cols, assets.items()):
            with col:
                st.subheader(name)
                try:
                    # 透過 yfinance 抓取過去 1 個月的歷史資料
                    ticker_info = yf.Ticker(symbol)
                    hist = ticker_info.history(period="1mo")
                    
                    if not hist.empty:
                        # 計算最新價格與漲跌
                        latest_price = hist['Close'].iloc[-1]
                        prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else latest_price
                        change = latest_price - prev_price
                        pct_change = (change / prev_price) * 100
                        
                        # 顯示大字體的數字儀表板
                        st.metric(
                            label="最新價格",
                            value=f"{latest_price:.2f}",
                            delta=f"{change:.2f} ({pct_change:.2f}%)"
                        )
                        
                        # 畫出折線圖
                        st.line_chart(hist['Close'])
                    else:
                        st.warning("目前無交易資料")
                        
                except Exception as e:
                    st.error("暫時無法取得資料，請稍後再試。")

st.markdown("---")
st.caption("資料來源：Yahoo Finance API | 此為自動化追蹤工具，非投資建議。")
