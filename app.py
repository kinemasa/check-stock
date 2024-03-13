import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import streamlit as st
import altair as alt


st.title('株価可視化アプリ')

st.sidebar.write("""
# 株価可視化ツール

株価を可視化ツールです.
表示日数を選択できます
""")

st.sidebar.write("""
## 表示日数
""")

days = st.sidebar.slider('日数',1,50,20)


st.write(f"""
### 過去**{days}日間**の株価
""")


@ st.cache_data ## キャッシュを用いた処理を行う前につける
def get_data(days,companies):
  df =pd.DataFrame()
  
  for company in companies.keys():
    company_df = yf.Ticker(companies[company])
    history = company_df.history(period =f'{days}d')
    history = history[['Close']]
    history.columns =[company]
    history = history.T
    history.index.name ="Name"
    df = pd.concat([df,history])
  return df
try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)

    ymin ,ymax = st.sidebar.slider('範囲を指定してね',0.0,3500.0,(0.0,3500.0))


    companies = {
        'apple':'AAPL',
        'google':'GOOGL',
        'amazon':'AMZN',
        'netflix':'NFLX'
        }

    df =get_data(days,companies)
    chosenCompanies =st.multiselect(
        '会社名を選択してください',
        list(df.index),
        ['apple','google']
    )

    if not chosenCompanies:
        st.error('少なくとも一社は選んでください')
    else:
        data =df.loc[chosenCompanies]
        st.write('### 株価（USD）',data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data,id_vars=['Date']).rename(
        columns ={'value':'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8,clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q",stack =None,scale=alt.Scale(domain=[ymin,ymax])),
                color ="Name:N"
            )
        )
    st.altair_chart(chart,use_container_width=True)
except :
    st.error("範囲指定エラーが起きています")