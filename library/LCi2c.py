##YWROBOT
#ifndef LiquidCrystal_I2C_h
#define LiquidCrystal_I2C_h

#include <inttypes.h>
#include "Print.h" 
#include <Wire.h>
import smbus
import time

## commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET  = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

## flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

## flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

## flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

## flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

## flags for backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

En = 0b00000100  ## Enable bit
Rw = 0b00000010  ## Read/Write bit
Rs = 0b00000001  ## Register select bit

class LiquidCrystal_I2C:
    def __init__( self, lcd_addr, lcd_cols, lcd_rows ):
        self._Addr = lcd_addr
        ## self._displayfunction 
        ## self._displaycontrol
        ## self._displaymode
        ## self._numlines
        self._cols = lcd_cols
        self._rows = lcd_rows
        self._backlightval = LCD_NOBACKLIGHT

        
    def begin( self, cols, lines, dotsize ) :
        if lines > 1:
            self._displayfunction = self._displayfunction | LCD_2LINE
        self._numlines = lines

        ## for some 1 line displays you can select a 10 pixel high font        
        if dotsize != 0 and lines == 1 :
            self._displayfunction = self._displayfunction | LCD_5x8DOTS
        ## SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
        ## according to datasheet, we need at least 40ms after power rises above 2.7V
        ## before sending commands. Arduino can turn on way befer 4.5V so we'll wait 50
        time.sleep( 0.05 )

        ## Now we pull both RS and R/W low to begin commands
        self.expanderWrite( self._backlightval )
        time.sleep( 1 )
        
        ## put the LCD into 4 bit mode
        ## this is according to the hitachi HD44780 datasheet
        ## figure 24, pg 46
    
        ## we start in 8bit mode, try to set 4 bit mode
        self.write4bits( 0x03 << 4 )
        time.sleep( 0.0045 ); ## wait min 4.1ms
   
        ## second try
        self.write4bits(0x03 << 4)
        time.sleep( 0.0045 ); ## wait min 4.1ms
   
        ## third go!
        self.write4bits(0x03 << 4)
        time.sleep( 0.0015 );
   
        ## finally, set to 4-bit interface
        self.write4bits( 0x02 << 4 ) 

        ## set # lines, font size, etc.
        self.command( LCD_FUNCTIONSET | self._displayfunction )
    
        ## turn the display on with no cursor or blinking default
        self._displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
        self.display()
    
        ## clear it off
        self.clear()
    
        ## Initialize to default text direction (for roman languages)
        self._displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
    
        ## set the entry mode
        self.command( LCD_ENTRYMODESET | self._displaymode)
    
        self.home()
  

        

    def clear( self ):
        self.command(LCD_CLEARDISPLAY)  ##clear display, set cursor position to zero
        time.sleep(0.002) ## this command takes a long time!
        
    def home( self ):
        self.command(LCD_RETURNHOME)  ## set cursor position to zero
        time.sleep(0.002)  ## this command takes a long time!
        
    def noDisplay( self ) :
        self._displaycontrol = self._displaycontrol & (~LCD_DISPLAYON)
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol);
    
    def display( self ):
        self._displaycontrol = self._displaycontrol | LCD_DISPLAYON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    
    def noBlink( self ):
        self._displaycontrol = self._displaycontrol & ( ~LCD_BLINKON )
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)       
    def blink( self ):
        self._displaycontrol = self._displaycontrol | LCD_BLINKON
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
        
    def noCursor( self ):
        self._displaycontrol = self._displaycontrol & ( ~LCD_CURSORON )
        self.command(LCD_DISPLAYCONTROL | self._displaycontrol)
    
    def cursor( self ):
        self._displaycontrol = self._displaycontrol | LCD_CURSORON
        self.command( LCD_DISPLAYCONTROL | self._displaycontrol);
    
    def scrollDisplayLeft( self ):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)
    
    def scrollDisplayRight(self):
        self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def leftToRight( self ):
        self._displaymode = self._displaymode | LCD_ENTRYLEFT;
        self.command(LCD_ENTRYMODESET | self._displaymode)
    
    def rightToLeft( self ):
        self._displaymode = self._displaymode & ( ~LCD_ENTRYLEFT )
        self.command(LCD_ENTRYMODESET | self._displaymode)        

    def noBacklight( self ):
        self._backlightval=LCD_NOBACKLIGHT
        self.expanderWrite(0)
    
    def backlight( self ):
        self._backlightval=LCD_BACKLIGHT;
        self.expanderWrite(0)
    
    def autoscroll( self ) :
        self._displaymode = self._displaymode | LCD_ENTRYSHIFTINCREMENT
        self.command( LCD_ENTRYMODESET | self._displaymode )
    
    def noAutoscroll( self ):
        self._displaymode = self._displaymode & ( ~LCD_ENTRYSHIFTINCREMENT )
        self.command( LCD_ENTRYMODESET | self._displaymode )
    
    def createChar( self, location , charmap ):
        location = location & 0x7; ## we only have 8 locations 0-7
        self.command( LCD_SETCGRAMADDR | (location << 3))
        for i in range[7]:
            self.send( charmap[i], Rs )
    
    
    def setCursor( self, col , row ) :
        row_offsets = ( 0x00, 0x40, 0x14, 0x54 )
        if  row > self._numlines :
            row = self._numlines-1;    ## we count rows starting w/0
    
        self.command( LCD_SETDDRAMADDR | (col + row_offsets[row]) )        

    def command( self, value ):
        self.send(value, 0)
    
    def init( self ):
        self.init_priv()

    def init_priv( self ):
        self.bus = smbus.SMBus(1)
        self._displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
        self.begin( self._cols, self._rows, 0 )
        
    def send(self, value , mode ):
        highnib = value & 0xf0
        lownib = ( value<<4 ) & 0xf0
        self.write4bits((highnib) | mode)
        self.write4bits((lownib) | mode)
    
    def write4bits( self, value ):
        self.expanderWrite(value)
        self.pulseEnable(value)
    
    def expanderWrite(self, _data ):
        self.bus.write_byte( self._Addr, _data | self._backlightval )
    
    def pulseEnable( self, _data ):
        self.expanderWrite( _data | En )    ## En high
        time.sleep(0.000001)        ## enable pulse must be >450ns
    
        self.expanderWrite( _data & ~En )   ## En low
        time.sleep(0.00005 )        ## commands need > 37us to settle


    def write( self, value ):
        self.send( value, Rs )

    def printstr( self, _data ):
        for s in range(len(_data)):
            _byteV = ord( _data[s] )
            self.write( _byteV )
