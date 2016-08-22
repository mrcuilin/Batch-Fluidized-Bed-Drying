import logging
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader

import MySQLdb
import readThread
import string
import os
import datetime

logger = logging.getLogger('sensor')
fh = logging.FileHandler('/home/pi/mysite/log/sensors.log')
formatter = logging.Formatter('%(asctime)s %(message)s')  
fh.setFormatter(formatter)  
logger.addHandler( fh )
logger.setLevel( logging.INFO )

def defLog() :
    return logger

# Show the Sample status
# Also show the proper command button
def result( request ):
    log = defLog()
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    # Get the RUNNING Status
    curs = db.cursor()
    curs.execute("SELECT * from statusTB where keyword='RUNNING' " )
    status = ''
    data = curs.fetchone()
    status = data[1]
    curs.close()

    # Get the ENABLED status
    curs = db.cursor()
    curs.execute("SELECT * from statusTB where keyword='ENABLED' ")
    ENABLED = ''
    data = curs.fetchone()
    ENABLED = data[1]
    curs.close()
    db.close()

    showStatus = ''
    if status == 'YES' :
        showStatus = 'RUN'
    else :
        showStatus = 'STOP'
    status = ''

    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("select * from Sensordata order by sessionId DESC, sampleTimeStamp DESC limit 0,20" )
    data = curs.fetchall()
    curs.close()
    db.close()

    #c = 0
    dataStr = []
    sesId = data[0][0]
    for d in data:
        if d[0] == sesId :
            tempstr = "T(s):" + str( round( d[11]*0.001, 2 )) + ' S1:' + str( round( string.atof(d[1]),1)) + 'c ' + str( round( string.atof(d[2]),1)) + '% ' \
                         ' S2:' + str( round( string.atof(d[3]),1)) + 'c ' + str( round( string.atof(d[4]),1)) + '% ' \
                         ' S3:' + str( round( string.atof(d[5]),1)) + 'c ' + str( round( string.atof(d[6]),1)) + '% '
            dataStr.append( tempstr )
        #c = c + 1
    return render( request = request,template_name='cmds.html',context={ 'status': showStatus , 'enable': ENABLED , 'nowdata' : dataStr, 'nowST' : sesId } )
    #return HttpResponse("The current status is " + status )

# Begin the Sample process    
def commandRun( request ):
    log = defLog()
    DT = request.POST['DT']
    log.info( DT )
    if DT:
        os.system("sudo date -s '" + DT + "'")
        log.info( "Set Time successful :" + DT )
    
    
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("update statusTB set status = 'YES' where keyword='RUNNING' " )
    db.commit()
    curs.close()
    db.close()

    READER = readThread.reader()
    READER.start()
    
    return render( request = request,template_name='gohome.html' )

# End the Sample Process
def commandStop( request ):
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("update statusTB set status = 'NO' where keyword='RUNNING' " )
    db.commit()
    curs.close()
    db.close()
    return render( request = request,template_name='gohome.html' )
    
def testCmd( request ):
    #template = loader.get_template('Cmds.html')
    tempContext = {
        'status' : 'STOP',
    }
    return render( request,'cmds.html',tempContext )


# List the exist days
def dayList( request ):
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("select distinct sessionId from dataSession order by sessionId DESC limit 0,100" )
    data = curs.fetchall()
    curs.close()
    db.close()
    return render( request=request, template_name='daylist.html', context = { 'days' : data } )

def sessionList( request ):
    theDay = request.GET['DAY']
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("select sampleTime from dataSession where sessionId='" + theDay + "' order by sampleTime ASC" )
    data = curs.fetchall()
    curs.close()
    db.close()
    return render( request=request, template_name='sessionlist.html', context = { 'samplesessions' : data , 'day' : theDay } )

def download( request ) :
    theSampleTime = request.GET['SES']
    res = HttpResponse( content_type='APPLICATION/OCTET-STREAM' )
    res['Content-Disposition'] = 'attachment; filename=' + theSampleTime + '.csv'
    
    res.write("SampleBegin,\tTime(ms),\tSensor1_Temp(C),\tSensor1_Hum(%),\tSensor2_Temp(C),\tSensor2_Hum(%),\tSensor3_Temp(C),\tSensor3_Hum(%)\r\n")
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("select * from Sensordata where sessionId='" + theSampleTime + "'" )
    data = curs.fetchall()
    for row in data:
        res.write( "'" + row[0] )
        res.write( "," )
        res.write( row[11] )
        res.write( "," )
        res.write( row[1] )
        res.write( "," )
        res.write( row[2] )
        res.write( "," )
        res.write( row[3] )
        res.write( "," )
        res.write( row[4] )
        res.write( "," )
        res.write( row[5] )
        res.write( "," )
        res.write( row[6] )
        res.write( "\r\n" )
    
    curs.close()
    db.close()
    return res
    
def show( request ) :
    theSampleTime = request.GET['SES']
    res = HttpResponse( )
    res.write("<html><body><pre>")
    res.write("SampleBegin,\tTime(ms),\tSensor1_Temp(C),\tSensor1_Hum(%),\tSensor2_Temp(C),\tSensor2_Hum(%),\tSensor3_Temp(C),\tSensor3_Hum(%)\r\n")
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("select * from Sensordata where sessionId='" + theSampleTime + "'" )
    data = curs.fetchall()
    for row in data:
        res.write( "" + row[0] )
        res.write( ",\t" )
        res.write( row[11] )
        res.write( ",\t" )
        res.write( row[1] )
        res.write( ",\t" )
        res.write( row[2] )
        res.write( ",\t" )
        res.write( row[3] )
        res.write( ",\t" )
        res.write( row[4] )
        res.write( ",\t" )
        res.write( row[5] )
        res.write( ",\t" )
        res.write( row[6] )
        res.write( "\r\n" )

    res.write("</pre></body></html>")
    curs.close()
    db.close()
    return res

def showRaw( request ) :
    theSampleTime = request.GET['SES']
    res = HttpResponse( )
    db = MySQLdb.connect("localhost","root",'','dataCapture')
    curs = db.cursor()
    curs.execute("select * from Sensordata where sessionId='" + theSampleTime + "'" )
    data = curs.fetchall()
    res.write( "var D = [" )
    for row in data:
    	res.write( "[" )
        res.write( row[11] / 60000.0 )
        res.write( "," )
        res.write( row[1] )
        res.write( "," )
        res.write( row[2] )
        res.write( "," )
        res.write( row[3] )
        res.write( "," )
        res.write( row[4] )
        res.write( "," )
        res.write( row[5] )
        res.write( "," )
        res.write( row[6] )
        res.write( "],\r\n" )
    res.write("];")
    curs.close()
    db.close()
    return res

def showGraph( request ) :
    theSampleTime = request.GET['SES']
    return render( request=request, template_name='SHOWGRAPH.html', context = { 'SES' : theSampleTime } )

