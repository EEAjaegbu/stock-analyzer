#!/usr/bin/env python
# coding: utf-8

# In[109]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
import yfinance as yf
import scipy.stats as stats
import datetime
from datetime import date
import streamlit as st
import statsmodels.api as sm
from statsmodels import regression
from PIL import Image

# In[6]:
image= Image.open("banner.jpg")
st.image(image,use_column_width=True)
st.write("""
This web app analyzes the risk and returns of any partuculat stocks in the database used. it visually analyze the time plot of the stock
,the volatility clustering, descrption of the return, Beta , Value at Risk and Alpha of the Stock.

Database: Yahoo Finance
""")
plt.style.use("bmh")


# In[31]:

## Loading dataset

#### Image ---------
## Enter Ticker
st.sidebar.subheader("Company")
ticker = st.sidebar.text_input("Ticker","AMZN")

## Select Period
st.sidebar.subheader(" Period")
st.sidebar.write("Enter Start and End Date")
start_date= st.sidebar.date_input("Start date", datetime.date(2017,1,1))
end_date= st.sidebar.date_input("End date", date.today())

## Loading dataset
stock = yf.download(ticker,start =start_date,end=end_date)
stockinfo = yf.Ticker(ticker)
share = YahooFinancials('AAPL')

# Benchmark index is S&P 500
benchmark = yf.download("SPY",start =start_date,end=end_date)

## Company _Name
company_name =stockinfo.info["longName"]
st.header(company_name)
if st.button("About"):
    info = stockinfo.info['longBusinessSummary']
    st.write(info)

# View the dataset
st.subheader("The Stock Information")
st.write("The Open price is the first price traded in a given time period and the last price traded is the Close Price. The High and Low can happen any time in-between these two extremes.")
st.write("OHLC for the past 5 days") 
st.dataframe(stock.tail(5).sort_index(ascending=False))


### Time plot
st.subheader("Time plot")
st.write(" A display of closing stock price over a given time period")
            
st.line_chart(stock["Close"])

    ## volatility clustering plot
st.subheader(" Daily returns of the Closing Price")
st.write("The price return is the rate of return on an investment portfolio, where the return measure takes into account only the capital appreciation of the portfolio, while the income generated by the assets in the portfolio, in the form of interest and dividends, is ignored.") 
returns = stock['Close'].pct_change().dropna()
st.line_chart(returns)

st.subheader("Descriptive Summary of the daily returns ")
summ_return =pd.DataFrame({"Minimum":returns.min(),"Maximum":returns.max(),"Average":returns.mean(),"Variance":returns.var(),
                          "Kurtosis":returns.kurtosis(),"Skewness": returns.skew(),"Volatility(%)":(returns.std()*100)},index=["Value"])

st.dataframe(summ_return)
# Benchmark retuns
benchmark_returns = benchmark["Close"].pct_change().dropna()

## The Density Distribution of Daily Returns
fig, ax = plt.subplots(figsize=(8,3))
plt.title("Histogram of returns")
plt.xlabel("daily returns")
plt.ylabel("Frequncy")
ax.hist(returns, bins =100,histtype='stepfilled')
st.pyplot(fig)

### Performance Metrics 
## Calculate Beta Value
# Regression Method.
X = benchmark_returns.values
Y = returns.values

def linreg(x,y):
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y,x).fit()
    
    # remove the constant
    x=x[:,1]
    return model.params[0],model.params[1]
        
alpha, beta = linreg(X,Y)
        
#beta = stockinfo.info['beta']

## Value at Risk Using Variance - Covaraince method
mean = returns.mean()
sigma = returns.std()
VaR= (-1 *stats.norm.ppf(0.05,mean,sigma))*100

#risk = pd.DataFrame({"Beta":beta,"Value at Risk":VaR},index=['Value'])
#st.dataframe(risk)

st.subheader("Beta")
st.write("""
Beta is a relative volatility measure that estimate the movements of the changes in prices(Volatility)of a particular security /assets to the overall stock market. It measures the exposure of an assets to the general markets movements. 

The benchmark index used is the S&P 500
""")
st.dataframe(pd.DataFrame({"Beta":beta},index=['Value']))
             
st.subheader("Value at Risk")
st.write("""
Value at Risk(VaR) is a statistical tool that measures the maximum potential loss of an investment over a given period of time, a 95% VaR is calculated uin this program. 

A 95% VaR   implies that, at 95% confidence level there is a chance that our portfolio will loss some var% or more  of it portfolio value in a single day. 
""")
st.dataframe(pd.DataFrame({"Value at Risk":VaR},index=['Value']))

st.subheader("Alpha")
st.write("""
Alpha measures the amount that the investment has returned in comparison to the market index or other broad benchmark that it is compared against.It measures the performance of an index against a benchmark
""")
st.dataframe(pd.DataFrame({"Alpha":alpha},index=['Value']))


# In[107]:

#fig1,ax1 = plt.subplots(figsize=(8,4))
#ax1.plot(stock.Close,label=ticker)
#ax1.plot(benchmark.Close,label="S&P500")
#plt.legend()
#st.pyplot(fig1)

if st.sidebar.button("Developer"):
    st.sidebar.write("""
    Name:E E Ajaegbu
    """)
    st.sidebar.write("""
    gmail: ajaegbu35@gmail.com
    """)
    st.sidebar.write("""
    github: https://github.com/EEAjaegbu
    """)

