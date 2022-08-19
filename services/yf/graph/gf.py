import numpy as np
import pandas as pd
from pandas_datareader import data as pdr

# Market Data 
import yfinance as yf

#Graphing/Visualization
import datetime as dt 
import plotly.graph_objs as go 

# Override Yahoo Finance 
yf.pdr_override()

def graph(company_code, period, chat_id=None) -> str:

    # Create input field for our desired company_code 
    # company_code=input("Enter a company_code ticker symbol: ")

    # Retrieve company_code data frame (df) from yfinance API at an interval of 1m 
    # df = yf.download(tickers=company_code,period=period,interval='1m')
    period_check = period

    if period_check == '1d':
        df = yf.download(tickers=company_code, period= '1d', interval='5m')
    elif period_check == '1m':
        df = yf.download(tickers=company_code, period = '1mo', interval = '1d')
    elif period_check == '1y':
        df = yf.download(tickers=company_code, period = '1y', interval = '1wk')
    elif period_check == '5y':
        df = yf.download(tickers=company_code, period = '5y', interval = '1mo')
    # print(df)

    # Declare plotly figure (go)
    fig=go.Figure()

    fig.add_trace(go.Candlestick(x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'], name = 'market data'))

    fig.update_layout(
        title= str(company_code)+' Live Share Price:',
        yaxis_title='Stock Price (USD per Shares)')               

    fig.update_xaxes(
        rangeslider_visible=False,
    #     rangeselector=dict(
    #         buttons=list([
    #             dict(count=15, label="15m", step="minute", stepmode="backward"),
    #             dict(count=45, label="45m", step="minute", stepmode="backward"),
    #             dict(count=1, label="HTD", step="hour", stepmode="todate"),
    #             dict(count=3, label="3h", step="hour", stepmode="backward"),
    #             dict(step="all")
    #         ])
    #     )
    )

    # fig.show()
    file = f"static/{chat_id}.png"
    fig.write_image(file)
    return file

if __name__ == '__main__':
    graph('AMZN', '1m')