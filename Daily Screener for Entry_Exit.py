import numpy as np
import pandas as pd
import pandas_datareader as pdr
import datetime
from datetime import date
import requests
import math
import yfinance as yf

#Create a list of the tickers that need to be run for analysing any short term trends in the market
tickers = ['AAPL','AMZN','ARKG','ARKK','ARKF','BLK','GOOGL','GOOG','ICLN','MSFT','SPXU','SQ','SQQQ','UVXY','VOO','TQQQ','UPRO','QQQ','SPY','VXX','IOZ.AX','A200.AX','STW.AX',
           'CBA.AX','ANZ.AX','NAB.AX','WBC.AX','FMG.AX','BHP.AX','RIO.AX','VHY.AX','ETHI.AX','VEU.AX','VDHG.AX','TWE.AX','TLS.AX','ORG.AX','IAG.AX','WOW.AX','WES.AX']

#This is the function that creates the buy and sell signals
def TradingAlgo(selected_dropdown_value):
    CompanyCode = selected_dropdown_value
    stock = pdr.get_data_yahoo(CompanyCode,start=datetime.datetime(2018,2,2), end=date.today())
    days = stock['Close'].count()
    df1 = pd.DataFrame(stock, columns=['Close','Open','High','Low','Volume'])
    df1['26 EMA'] = df1.ewm(span = 26, min_periods = 26).mean()['Close']
    df1['12 EMA'] = df1.ewm(span = 12, min_periods = 12).mean()['Close']
    df1['MACD'] = df1['12 EMA'] - df1['26 EMA']
    df1['MACD Ave'] = df1['MACD'].mean()
    df1['Signal Line'] = df1.ewm(span = 9, min_periods = 9).mean()['MACD']
    AbsTP = []
    x = 0
    y = 0
    z = 0
    w = 0
    PosRatio = 0
    NegRatio = 0
    Positive = []
    Negative = []
    MFR = []
    Equat = 0
    MFI = [50,50,50,50,50,50,50,50,50,50,50,50,50,50]
    df1['Typical Price'] = (df1['Close'] + df1['High'] + df1['Low'])/3
    AbsTP.append(df1['Typical Price'].iloc[x])
    while x < (days - 1):
        if df1['Typical Price'].iloc[(x+1)] > df1['Typical Price'].iloc[x]:
            AbsTP.append(df1['Typical Price'].iloc[(x+1)])
        else:
            AbsTP.append((df1['Typical Price'].iloc[(x+1)])*(-1))
        x = x + 1
    df1['Abs TP'] = AbsTP
    df1['Raw Money'] = df1['Abs TP'] * df1['Volume']
    while y < days:
        if df1['Raw Money'].iloc[y] > 0:
            Positive.append(df1['Raw Money'].iloc[y])
            Negative.append(0)
        else:
            Negative.append(df1['Raw Money'].iloc[y])
            Positive.append(0)
        y = y + 1
    while z < 14:
        PosRatio = PosRatio + Positive[z]
        NegRatio = NegRatio + Negative[z]
        z = z + 1
    while z < days:
        MFR.append((PosRatio/(-1*NegRatio)))
        PosRatio = PosRatio - Positive[(z - 14)] + Positive[z]
        NegRatio = NegRatio - Negative[(z - 14)] + Negative[z]
        z = z + 1
    while w < len(MFR):
        Equat = 100 - (100/(1+MFR[w]))
        MFI.append(Equat)
        w = w + 1
    df1['MFI'] = MFI
    df1['Mid Line'] = df1['MFI'].mean()
    df1['SELL'] = df1['Mid Line'] + df1['MFI'].std()
    df1['BUYER'] = df1['Mid Line'] - df1['MFI'].std()
    df1['SMA'] = df1.rolling(window=20).mean()['Close']
    df1['LMA'] = df1.rolling(window=200).mean()['Close']
    df1['20 Day Volatility'] = df1['Close'].rolling(window=20).std()
    df1['Top Bollinger Band']=df1['SMA']+2*df1['20 Day Volatility']
    df1['Bottom Bollinger Band']=df1['SMA']-2*df1['20 Day Volatility']
    df1['Midway'] = (df1['Top Bollinger Band']+df1['SMA'])/2
    x = 1
    MACD_Return = [0]
    Signal_Return = [0]
    while x < days:
        MACD_Return.append((df1['MACD'][x]-df1['MACD'][x-1])/df1['MACD'][x-1])
        Signal_Return.append((df1['Signal Line'][x]-df1['Signal Line'][x-1])/1)
        x = x+1
    df1['MACD Ret'] = MACD_Return
    df1['Signal Ret'] = Signal_Return
    x = days-50
    SellDate = []
    SellPrice = []
    SellDate1 = []
    SellPrice1 = []
    BuyDate = []
    BuyPrice = []
    outputlist = []
    BuyCounter = 0
    BuyReturn = 0
    OtherBuyReturn = 0
    OtherBuyCounter = 0
    SellReturn1 = 0
    SellCounter1 = 0
    SellReturn2 = 0
    SellCounter2 = 0
    SellReturn3 = 0
    SellCounter3 = 0
    Scounter = 0
    Bcounter = 0
    Zeb = 0
    while x < days:
        if df1['Open'][x]>df1['Top Bollinger Band'][x]:
            if df1['Low'][x]<df1['Top Bollinger Band'][x]:
                if df1['Close'][x] <= df1['Open'][x]:
                    if df1['MACD'][x]>=df1['Signal Line'][x]:
                        SellDate1.append(df1.index.date[x])
                        SellPrice1.append(df1['Close'][x])
                        Scounter = x
                        if x + 3>days:
                            Zeb = x
                        else:
                            SellReturn1 = SellReturn1 + ((min(df1['Low'][x+1:x+9])-df1['High'][x])/df1['High'][x])
                            SellCounter1 = SellCounter1 + 1
        if df1['MACD'][x]>df1['Signal Line'][x]:
            if df1['MACD'][x]<df1['MACD'][x-1]:
                if df1['MACD'][x]>df1['MACD Ave'][x]:
                    if df1['MFI'][x]>df1['SELL'][x]:
                        if (abs(df1['MACD'][x])-abs(df1['Signal Line'][x]))<(abs(df1['MACD'][x-1])-abs(df1['Signal Line'][x-1])):
                            if (abs(df1['MACD'][x-1])-abs(df1['Signal Line'][x-1]))<(abs(df1['MACD'][x-2])-abs(df1['Signal Line'][x-2])):
                                if df1['Signal Ret'][x]<df1['Signal Ret'].std()+df1['Signal Ret'].mean():
                                    if df1['Close'][x]>df1['Midway'][x]:
                                        SellDate.append(df1.index.date[x])
                                        SellPrice.append(df1['Close'][x])
                                        Scounter = x
                                        if x + 11>days:
                                            Zeb = x
                                        else:
                                            SellReturn2 = SellReturn2 + ((min(df1['Low'][x+1:x+9])-df1['High'][x])/df1['High'][x])
                                            SellCounter2 = SellCounter2 + 1
        if df1['Low'][x-1]>df1['Top Bollinger Band'][x-1]:
            if df1['High'][x]<df1['Top Bollinger Band'][x]:
                if df1['Close'][x] <= df1['Open'][x]:
                    if df1['MFI'][x]>=df1['Mid Line'][x]:
                        SellDate.append(df1.index.date[x])
                        SellPrice.append(df1['Close'][x])
                        Scounter = x
                        if x + 11>days:
                            Zeb = x
                        else:
                            SellReturn3 = SellReturn3 + ((min(df1['Low'][x+1:x+9])-df1['High'][x])/df1['High'][x])
                            SellCounter3 = SellCounter3 + 1
                        
        if df1['Low'][x]<df1['Bottom Bollinger Band'][x]:
            if df1['Low'][x]<(df1['Low'][x-1])*0.99:
                if df1['Low'][x]<(df1['Low'][x-2])*0.99:
                    BuyDate.append(df1.index.date[x])
                    BuyPrice.append(df1['Low'][x])
                    Bcounter = x
                    if x + 11>days:
                        Zeb = x
                    else:
                        BuyReturn = BuyReturn + ((max(df1['High'][x+1:x+9])-df1['Low'][x])/df1['Low'][x])
                        BuyCounter = BuyCounter + 1
        if df1['MACD'][x]<df1['Signal Line'][x]:
            if df1['MACD'][x]<df1['MACD Ave'][x]:
                if df1['MFI'][x]<df1['BUYER'][x]:
                    if (df1['MACD'][x]-df1['Signal Line'][x])<(df1['MACD'][x-1]-df1['Signal Line'][x-1]):
                        if (df1['MACD'][x-1]-df1['Signal Line'][x-1])>(df1['MACD'][x-2]-df1['Signal Line'][x-2]):
                            if (df1['MACD'][x-2]-df1['Signal Line'][x-2])>(df1['MACD'][x-3]-df1['Signal Line'][x-3]):
                                if df1['Signal Ret'][x]<df1['Signal Ret'].std()+df1['Signal Ret'].mean():
                                    if df1['Close'][x]<df1['Midway'][x]:
                                        BuyDate.append(df1.index.date[x])
                                        BuyPrice.append(df1['Low'][x])
                                        Bcounter = x
                                        if x + 11>days:
                                            Zeb = x
                                        else:
                                            BuyReturn = BuyReturn + ((max(df1['High'][x+1:x+9])-df1['Low'][x])/df1['Low'][x])
                                            BuyCounter = BuyCounter + 1

        x = x + 1
    if Scounter + 4 > days:
        return CompanyCode, "Sell", (days-1-Scounter)
    if Bcounter + 4 > days:
        return CompanyCode, "Buy", (days-1-Bcounter)
    return "","",""


def Main():
    Code = []
    Status = []
    Days = []
    for t in tickers:
        print(t)
        C,S,D = TradingAlgo(t)
        if C == "":
            continue
        else:
            Code.append(C)
            Status.append(S)
            Days.append(D)
    df = pd.DataFrame({'Company':Code,'Status':Status,'Days Ago':Days})
    df.to_csv('Screener_Results.csv')
    print("Printed to csv")

Main()
        
        
        



