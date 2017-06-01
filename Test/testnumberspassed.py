from bin import mbedread
import serial, urllib2, time

ser = serial.Serial("COM14")
ser.setBaudrate(9600)

mbedread.serwrite(ser,"1.0\\r\\n")

print mbedread.serread(ser)
