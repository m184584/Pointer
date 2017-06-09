from bin import mbedread
from bin import gpsutils
from Test import randGPS
import serial, urllib2, time

# setup inital serial port for gps position
ser1_gps = serial.Serial("COM14")
ser.setBaudrate(9600)

#set up second serial port to send azimuth and elevation to antenna pointer
ser2_antenna = serial.Serial("COM14")
ser.setBaudrate(9600)

#read gps position from antenna
lla1 = mbedread.serrerad(ser1_gps)

#substantiantes the class gpsutils
helper = gpsutils.GpsUtils()

#initiates the degrees for azimuth and elevation
azieleD = [0,0]

while(1):

    #gps position for plane
    lla2

    #converts longitute latitude and altitude to east north up
    enu = gpsutils.lla2enu(lla1,lla2)

    #converts enu to azimuth and elevation comands
    aziele = enu2azel (enu)

    #Converts azimuth and elevation to degrees
    azieleD[0] = helper.rad2deg(aziele[0])
    azieleD[1] = helper.rad2deg(aziele[1])

    #sends the angles via serial port
    mbedread.serwrite(ser2_antenna,"%f,%f\\r\\n" % (azieleD[0],azieleD[1]))

    #will only run every 20 second
    time.sleep(20)
