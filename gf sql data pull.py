import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='gf_data')


def getStatHelp(startTime, endTime, symbol, exchange, stat):
    querystr = "select" + stat + "from gf_data.masterdata where" \
               + "symbol =" + symbol \
               + "and exchange =" + exchange \
               + "and " + startTime + " <= TimeStamp and TimeStamp <= " + endTime
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)

print cursor

cnx.commit()

cnx.close()

