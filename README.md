# Portfolio-Timing-Tool
This python sheet helped with deciding on the best strategy for investing into the US and AUS Portfolios

Using the 5-year historical data tables from yahoo finance I created a python script that would analyse whether it would be more beneificial to complete a classic dollar
cost averaging method for investing into my model portfolio, or if a strategy would assist more. The result showed that generally using a strategy of combined technical 
buy signals, along with the dollar cost averaging model had a better average price per unit for each company, but it also had a higher quantity at this average price per unit.
With the US broker I use not having any transaction fees, investing this often is easy even with such small amounts of money per trade.

The dollar cost averaging method was to buy every 20 trading days and hold on the other 19 days. The technical buy strategy bought every 20 trading days as well, however, 
if a buysignal triggered it would buy a further $20 worth once a month when that happened. The buy signal was the low crossing the bottom bollinger band. As well as
a buy signal based on MFI being low, and the MACD starting to being coming together.

Attached in the files is the python code as well as a few excel sheets that show more of the output.

As an extension on this I created a technical screener that would look through the securities I want to invest into and tell me if it is a technically good time to invest 
in those securities. This will assist with better timing and active participation in timing the entries into the market.
