import pandas as pd
import math
import datetime

woo = ['AAPL','AMZN','ARKG','ARKK','BLK','GOOGL','ICLN','MSFT','SQ','VOO']

def TechIndicators(info, track):
    df = info
    df['26 EMA'] = df.ewm(span = 26, min_periods = 26).mean()['Close']
    df['12 EMA'] = df.ewm(span = 12, min_periods = 12).mean()['Close']
    df['MACD'] = df['12 EMA'] - df['26 EMA']
    df['Signal Line'] = df.ewm(span = 9, min_periods = 9).mean()['MACD']
    days = df['Close'].count()
    df['Typical Price'] = (df['Close'] + df['High'] + df['Low'])/3
    RawMon = [df['Typical Price'][0]*df['Volume'][0]]
    Positive = [RawMon[0]]
    Negative = [0]
    x = 0
    while x < days - 1:
        if df['Typical Price'][x+1]>df['Typical Price'][x]:
            RawMon.append(df['Typical Price'][x+1]*df['Volume'][x+1])
            Positive.append(RawMon[x+1])
            Negative.append(0)
        else:
            RawMon.append((df['Typical Price'][x+1]*df['Volume'][x+1])*(-1))
            Negative.append(RawMon[x+1])
            Positive.append(0)
        x = x + 1
    df['Raw Money'] = RawMon
    z = 0
    w = 0
    PosRatio = 0
    NegRatio = 0
    MFR = []
    MFI = [50,50,50,50,50,50,50,50,50,50,50,50,50,50]
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
    df['MFI'] = MFI
    counter = 0
    result = []
    dater = []
    buy_price = []
    buy_q = []
    buy_spreader = []
    df['SMA'] = df.rolling(window=20).mean()['Close']
    df['20 Day Volatility'] = df['Close'].rolling(window=20).std()
    df['Top Bollinger Band']=df['SMA']+2*df['20 Day Volatility']
    df['Bottom Bollinger Band']=df['SMA']-2*df['20 Day Volatility']
    boring_price = []
    boring_q = []
    while counter < days:
        if counter % 20 == 0:
            boring_q.append(15/df['Adj Close'][counter])
            boring_price.append(15)
            result.append("Buy")
            buy_q.append(15/df['Adj Close'][counter])
            buy_price.append(15)
            buy_spreader.append(counter)
        else:
            boring_price.append(0)
            boring_q.append(0)
            if df['MFI'][counter] < 40:
                if df['MACD'][counter] < df['Signal Line'][counter]:
                    if abs(df['MACD'][counter]-df['Signal Line'][counter])<abs(df['MACD'][counter-1]-df['Signal Line'][counter-1]):
                        if abs(df['MACD'][counter-1]-df['Signal Line'][counter-1])>abs(df['MACD'][counter-2]-df['Signal Line'][counter-2]):
                            if abs(df['MACD'][counter-2]-df['Signal Line'][counter-2])>abs(df['MACD'][counter-3]-df['Signal Line'][counter-3]):
                                if df['MACD'][counter] < 0:
                                    if buy_price[len(buy_price)-1] == 20:
                                        if buy_spreader[len(buy_spreader)-1] > counter - 20:
                                            result.append("Hold")
                                        else:
                                            result.append("Buy")
                                            buy_q.append(20/df['Adj Close'][counter])
                                            buy_price.append(20)
                                            buy_spreader.append(counter)
                                    else:
                                        result.append("Buy")
                                        buy_q.append(20/df['Adj Close'][counter])
                                        buy_price.append(20)
                                        buy_spreader.append(counter)
            if df['Low'][counter]<df['Bottom Bollinger Band'][counter]:
                if buy_price[len(buy_price)-1] == 20:
                    if buy_spreader[len(buy_spreader)-1] > counter - 20:
                        result.append("Hold")
                    else:
                        result.append("Buy")
                        buy_q.append(20/df['Adj Close'][counter])
                        buy_price.append(20)
                        buy_spreader.append(counter)
                else:
                    result.append("Buy")
                    buy_q.append(20/df['Adj Close'][counter])
                    buy_price.append(20)
                    buy_spreader.append(counter)
        dater.append(df['Date'][counter])
        counter = counter + 1
        if len(result)<counter:
            result.append("Hold")
        if len(buy_price)<counter:
            buy_price.append(0)
        if len(buy_q)<counter:
            buy_q.append(0)        
    df2 = pd.DataFrame(data = {'Date':dater,'Action':result,'Spent':buy_price,'Bought Quantity':buy_q,'Boring Price':boring_price,'Boring Q':boring_q})
    df2.to_csv(woo[track]+"69.csv")
    print("The strategy for ",woo[track]," led to a price of ",round(df2['Spent'].sum()/df2['Bought Quantity'].sum(),2))
    print("No strategy got this price", round(df2['Boring Price'].sum()/df2['Boring Q'].sum(),2))
    print("The quantity of units bought in the strat: ",round(df2['Bought Quantity'].sum(),2)," and the amount bought in no strat: ",round(df2['Boring Q'].sum(),2))
    return

def inputClose_outputInfo():
    track = 0
    for w in woo:
        data = pd.read_csv(w+".csv")
        TechIndicators(data, track)
        print("TA done")
        track = track + 1
    print("All done")
    return

inputClose_outputInfo()

