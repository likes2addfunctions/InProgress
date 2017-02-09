### Portfolio Note
# This tool rips html from google finance, parses the data to extract quantities
# of interest and then saves the info to a database via sql.
# The tool can accommodate any number of stock symbols from any exchange.

import urllib2  # works fine with Python 2.7.9 (not 3.4.+)
import time
import mysql.connector

#os.chdir(os.path.dirname(os.path.abspath(__file__)))

stat_list = ["cp", "pr" ,"open", "vol", "market_cap","pe_ratio", "Div", "eps", "Shares", "beta", "inst" ]

stock_list = [["DRYS", "NASDAQ"],["AAPL","NASDAQ"],["RAD","NYSE"],["F","NYSE"],["CHK", "NYSE"],["S","NYSE"], ["BAC", "NYSE"],["AMD", "NASDAQ"],["FB", "NASDAQ"]]

data_header = ["symbol", "exchange"] + [stat_list]

sql_stat_tuple = ("symbol", "stockexchange", "cp", "pr" ,"open_price", "vol", "market_cap","pe_ratio", "Div_", "eps", "Shares", "beta", "inst" )

dh_str = ""
for k in str(sql_stat_tuple):
    if k != "'":
        dh_str = dh_str + k

def try_append(char):
    try:
        int(char)
        return True
    except:
        if char == "." or char == "M" or char == "B" or char == "-" or char == "//" or char == "%":
            return True
        else:
            return False   
            
def get_stat(stat,content):
    statistic = stat
    stat_location = content.find(statistic)
    flag = 0
    ignore = 1
    value = ""
    if stat == "pr":
        ignore = 0
    pair = [statistic]
    for char in content[stat_location+1:]:
        if char == "&":
            pair = pair + [value]
            return pair
        if char == "\"":
            if ignore == 0:
                ignore = 1
            else:
                ignore = 0 
        if ignore == 0:
            if try_append(char):
                try:
                    int(char)
                    value = value + char
                    flag = 1
                except:
                    if flag == 1:
                        if char == "B":
                            value = str(float(value)*(10**9))
                            pair = pair + [value]
                            return pair
                        if char == "M":
                            value = str(float(value)*(10**6))
                            pair = pair + [value]
                            return pair
                        if char == "%":
                            value = str(float(value)*(10**(-2)))
                            pair = pair + [value]
                            return pair
                        value = value + char
            if flag ==1 and not(try_append(char)):
                pair = pair + [value]
                return pair
    return [statistic, 'NA']
            

def fetchMarketData(stock):
    symbol = stock[0]
    exchange = stock[1]
    link = "https://www.google.com/finance?q=" + "exhcange" + "%3A" + symbol
    url = link
    u = urllib2.urlopen(url)
    content = u.read()
    summary_start = content.find("renderRecentQuotes();")
    content = content[summary_start:]
    header = [symbol,exchange]
    stats = [["symbol", "exchange"], header]
    for stat in stat_list:
        if stat == '':
            stat = 'NA'
        stats_0 = []
        stats_1 = []
        new_pair = get_stat(stat, content)
        stats_0 = stats[0] + [new_pair[0]]
        stats_1 = stats[1] + [new_pair[1]] 
        stats = [stats_0] + [stats_1]  
    #print stats 
    return stats

def gather_data(stat_list, stock_list):
    data = [data_header]
    for stock in stock_list:
        data = data + [fetchMarketData(stock)[1]]
    return data

raw_data = gather_data(stat_list, stock_list)



cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='gf_data')
        
for entry in raw_data[1:]:
    entrytuple = tuple(entry)
    querystr = "insert into masterdata " + dh_str + " values " + str(entrytuple)
    print querystr
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)


  
cnx.commit()

print "capture complete", time.strftime("%b %d %H:%M")

cnx.close()

