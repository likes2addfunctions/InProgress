import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='gf_data')


def getDataRange(startDate,startHour, startMin, \
                endDate, endHour, endMin,\
                symbol):
    querystr = "select cp, pr from masterdata where " \
               + "symbol = '" + symbol \
               + "' and " + startDate + " <= time_gathered <= " + endDate \
               + " and hour(time_gathered) <= " + endHour \
               + " and " + startHour + " <= hour(time_gathered) " \
               + " and minute(time_gathered) <= " + endMin \
               + " and " + startMin + " <= minute(time_gathered) ;" 
    print querystr             
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    for (cp, pr) in data:
        print "{}".format(cp)
        
    return tuple(cursor)

def getDataRangeb(startDate,startHour, startMin, \
                endDate, endHour, endMin,\
                symbol):
    querystr = "select cp, pr from masterdata where " \
               + "symbol = '" + symbol \
               + "' and " + startDate + " <= time_gathered <= " + endDate \
               + " and hour(time_gathered) <= " + endHour \
               + " and " + startHour + " <= hour(time_gathered) " \
               + " and minute(time_gathered) <= " + endMin \
               + " and " + startMin + " <= minute(time_gathered) ;" 
    print querystr             
    query = (querystr)
    cursor = cnx.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    for cp in data:
        print "{}".format(cp)
        
    return tuple(cursor)

getDataRange("2017-02-08", "06", "57", \
            "2017-02-08", "12", "59", \
            "AMD")


cnx.close()


