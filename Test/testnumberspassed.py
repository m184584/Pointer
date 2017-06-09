import serial, urllib2, time

ser = serial.Serial("COM14")
ser.setBaudrate(9600)

ser.write("1.0\\r\\n")

print ser.readline()
