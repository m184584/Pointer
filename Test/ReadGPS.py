from bin import mbedread
import serial, urllib2, time

ser1_gps = serial.Serial("COM21", 9600)

while(1):

    statement = mbedread.serread(ser1_gps)

    combined = statement.split(',')

    lat= combined[0]
    longitute=combined[1]
    height=combined[2]

    print lat
    print longitute
    print height
