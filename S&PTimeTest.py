import pandas as pd
import numpy as np
import os 
import pandas.io.data
from pandas import Series, DataFrame
from pandas import ExcelWriter 
from pandas import read_csv 
import matplotlib.pyplot as plt
import datetime 
from scipy.stats import ttest_1samp 
import matplotlib.pyplot as plt 
from random import randint 
now = datetime.datetime.now()

list = '^GSPC'
start = None
while start is None:
    try:
        start = datetime.datetime(randint(1950,2015), randint(1,12), randint(1,31))
    except:
        pass 
end = datetime.datetime(now.year, now.month, now.day)

df = pd.io.data.get_data_yahoo(list, start, end)['Adj Close']
df = DataFrame(df)
df['Returns'] = df.pct_change()
df['Date'] = df.index 
df['Date'] = [time.date() for time in df['Date']] 
l = df.index.values
for i in range(0,len(l)):
    df.loc[l[i], 'DayoftheWeek'] = datetime.datetime.strptime(str(df.loc[l[i], 'Date']), '%Y-%m-%d').strftime('%A') 

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
Monday = 0 
MonCount = 0
Mon = []
Tuesday = 0
TueCount = 0
Tue = []
Wednesday = 0
WedCount = 0
Wed = []
Thursday = 0
ThuCount = 0
Thu = []
Friday = 0
FriCount = 0
Fri = []
#Need to loop through days and then loop through df to sum up all returns while also summing the total count. Then create average
for i in range(1,len(l)):
    
    
    dump = 0 
    if df.loc[l[i], 'DayoftheWeek'] == 'Monday':
        Monday = Monday + df.loc[l[i], "Returns"]
        MonCount = MonCount + 1
        Mon.append(df.loc[l[i],'Returns'])
    if df.loc[l[i], 'DayoftheWeek'] == 'Tuesday':
        Tuesday = Tuesday + df.loc[l[i], "Returns"]
        TueCount = TueCount + 1
        Tue.append(df.loc[l[i],'Returns'])
    if df.loc[l[i], 'DayoftheWeek'] == 'Wednesday':
        Wednesday = Wednesday + df.loc[l[i], "Returns"]
        WedCount = WedCount + 1
        Wed.append(df.loc[l[i],'Returns'])
    if df.loc[l[i], 'DayoftheWeek'] == 'Thursday':
        Thursday = Thursday + df.loc[l[i], "Returns"]
        ThuCount = ThuCount + 1
        Thu.append(df.loc[l[i],'Returns'])
    if df.loc[l[i], 'DayoftheWeek'] == 'Friday':
        Friday = Friday + df.loc[l[i], "Returns"]
        FriCount = FriCount + 1
        Fri.append(df.loc[l[i],'Returns'])
    else:
        dump = dump + df.loc[l[i], 'Returns']
    
dict = {'Monday': Monday/MonCount, 'Tuesday': Tuesday/TueCount, 'Wednesday': Wednesday/WedCount, 'Thursday': Thursday/ThuCount, 'Friday': Friday/FriCount}
dg = pd.Series(dict, name='DailyValue')
dff = DataFrame(dg)
dff['Day'] = dff.index
dff['Sorter'] = [5,1,4,2,3]


dff.sort_values(by = ['Sorter'], inplace = True) 
#dff.sort(['Day'], ascending = True) 

#dff.plot(kind='bar', grid = True, y = ['DailyValue'])
plt.show()
# Buy/Sell decision

for i in range(1,len(l)):
    if df.loc[l[i], 'DayoftheWeek'] == 'Friday':
        df.loc[l[i], "Signal"] = "Sell"
        df.loc[l[i], "Market"] = 1
    elif df.loc[l[i], 'DayoftheWeek'] == 'Monday':
        df.loc[l[i], "Signal"] = "Buy"
        df.loc[l[i], "Market"] = 0 
    else:
        df.loc[l[i], 'Signal'] = "Hold"
        df.loc[l[i], "Market"] = 1 
     
# Investment calculations
df['Investment'] = ""
df['S&P500 Investment'] = ''
df['Investment'][0] = 10000
df['S&P500 Investment'][0] = 10000

for i in range(1,len(l)):
    df.loc[l[i], 'S&P500 Investment'] = df.loc[l[i-1], 'S&P500 Investment'] * (1 + df.loc[l[i], 'Returns'])
    if df.loc[l[i], "Signal"] == "Sell":
        df.loc[l[i], "Investment"] = df.loc[l[i-1], 'Investment'] * (1 + df.loc[l[i], "Returns"])
    elif df.loc[l[i], "Signal"] == "Buy":
        df.loc[l[i], "Investment"] = df.loc[l[i-1], 'Investment']
    elif df.loc[l[i], 'Signal'] == "Hold":
        df.loc[l[i], 'Investment'] = df.loc[l[i-1], 'Investment'] * (1 + df.loc[l[i], "Returns"])

print(df.head())
        



#Excess Return over S&P500 Column 
#for i in range(1,len(l)):
#    df.loc[l[i], 'Excess Return'] = df.loc[l[i], 'Investment'] - df.loc[l[i], 'S&P500 Investment']

    
file = ExcelWriter('Time1.xlsx')
df.to_excel(file, 'Data')
file.close()
os.startfile('Time1.xlsx')

df.plot(y = ['Investment', 'S&P500 Investment'])
plt.show() 




print("Average Monday return: %s" % (Monday/MonCount))      
print("Average Tuesday return: %s" % (Tuesday/TueCount))
print("Average Wednesday return: %s" % (Wednesday/WedCount))
print("Average Thursday return: %s" % (Thursday/ThuCount))
print("Average Friday return: %s" % (Friday/FriCount))

print("1 sample t-tests for each day to test significance of daily returns against 0 are as follows:")
print(ttest_1samp(Mon,0))
print(ttest_1samp(Tue,0))
print(ttest_1samp(Wed,0))
print(ttest_1samp(Thu,0))
print(ttest_1samp(Fri,0)) 
