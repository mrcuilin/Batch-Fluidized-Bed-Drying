from sht1x.Sht1x import Sht1x as SHT1x
import time

def readOneSensor( dataPin, clkPin ):
    sht1x = SHT1x( dataPin, clkPin )
    temper = sht1x.read_temperature_C()
    sht1x = SHT1x( dataPin, clkPin )
    humi = sht1x._read_humidity( temper )
    return ( temper, humi )

def test():
    R = readOneSensor( 40, 36 )
    print 'current Temperaute : %f C     Humidity: %f %%' % ( R[0], R[1] )
    #print 'Current Temperuate :'
    #print temper
    #print 'C    Humidity : '
    #print humi
    #print '%\n'

def readAllSensor():
    R1 = readOneSensor( 40,38 ) 
    R2 = readOneSensor( 36,32 )
    R3 = readOneSensor( 37,35 )
    return ( R1, R2, R3 )

