import threading  
import time
import MySQLdb
import readSensor
import LCi2c

class reader( threading.Thread ):
    def __init__( self ):
        threading.Thread.__init__( self )
        self.thread_stop = False
        time.timezone = -28800
        nowStr = time.strftime("%Y%m%d%H%M%S", time.localtime( time.time() + 28800 ))
        nowDate = time.strftime("%Y-%m-%d", time.localtime( time.time() + 28800 ) )
        self.sessionId = nowStr
        self.beginTime = time.time()+ 28800

        db = MySQLdb.connect("localhost","root","","dataCapture")
        cur = db.cursor()
        SQL = "insert into dataSession values('" + nowStr + "','" + nowDate + "')"
        cur.execute( SQL )
        db.commit()
        cur.close()
        db.close()
        
        self.LCD = LCi2c.LiquidCrystal_I2C( 0x27, 16, 2 )
        self.LCD.init()
        self.LCD.noBacklight()
        self.LCD.clear()

    def _getStatus( self ):
        db = MySQLdb.connect("localhost","root",'','dataCapture')
        curs = db.cursor()
        curs.execute("SELECT * from statusTB where keyword='RUNNING' " )
        status = ''
        data = curs.fetchone()
        status = data[1]
        curs.close()
        db.close()
        return status

    def run( self ):
        run = True
        self.LCD.backlight()
        self.LCD.clear()
        while run :
            RR = readSensor.readAllSensor()

            self.LCD.setCursor( 0,0 )
            self.LCD.printstr( ' ' + str( round(( RR[0][0] + RR[1][0] )/2 , 1 )) + 'C ' \
                               + str( round(( RR[0][1] + RR[1][1] )/2 , 1 )) + '%    ' )
            
            self.LCD.setCursor( 0,1 )
            self.LCD.printstr( 'IN' + str( round(( RR[2][0] ) , 1 )) + 'C ' )
            
            SQL = "INSERT INTO Sensordata values('" + self.sessionId + "'," + \
                  "'" + ( '%f' % RR[0][0] ) + "'," + \
                  "'" + ( '%f' % RR[0][1] ) + "'," + \
                  "'" + ( '%f' % RR[1][0] ) + "'," + \
                  "'" + ( '%f' % RR[1][1] ) + "'," + \
                  "'" + ( '%f' % RR[2][0] ) + "'," + \
                  "'" + ( '%f' % RR[2][1] ) + "'," + \
                  "'7','8','9','10'," + \
                  "'" + ( '%d' % (( time.time() + 28800 - self.beginTime ) * 1000 )) + "')"
            print SQL
            db = MySQLdb.connect("localhost","root",'','dataCapture')
            curs = db.cursor()
            curs.execute( SQL )
            db.commit()
            curs.close()
            db.close()
            print "Write " + self.sessionId + "," + ( '%d' % (( time.time() + 28800 - self.beginTime) * 1000 ) )
            
            time.sleep( 2 )
            
            currentStatus = self._getStatus()
            if currentStatus == "NO" :
                run = False
                self.LCD.noBacklight()
                
    def stop(self):
        self.thread_stop = True
        self.LCD.noBacklight()
