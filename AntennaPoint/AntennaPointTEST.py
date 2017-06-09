from bin import mbedread
from bin import gpsutils
from bin import enu2azel
from Test import TestCordinates
import serial, urllib2, time

# setup inital serial port for gps position
#ser1_gps = serial.Serial("COM14")
#ser1_gps.setBaudrate(9600)

#set up second serial port to send azimuth and elevation to antenna pointer
ser2_antenna = serial.Serial("COM16", 115200,timeout=None,parity=serial.PARITY_NONE)
#read gps position from antenna
#lla1 = mbedread.serrerad(ser1_gps)
lla1 = (0,0,0)

count=0
#substantiantes the class gpsutils
helper = gpsutils.GpsUtils()
lla2_all = TestCordinates.coordinate()
print lla2_all

while(count<6):

    #gps position for plane


    enu = lla2_all[count]



    #converts longitute latitude and altitude to east north up
    #enu = helper.lla2enu(lla2,lla1)
    #print enu

    #converts enu to azimuth and elevation comands
    aziele = enu2azel.enu2azel (enu)

    azieleD = [0,0]
    azieleD[0] = helper.rad2deg(aziele[0])
    azieleD[1] = helper.rad2deg(aziele[1])

    statement = "%.4f,%.4f\\r\\n" % (azieleD[0],azieleD[1])
    mbedread.serwrite(ser2_antenna,statement)
    print statement
    time.sleep(5)

    count = count + 1
ser2_antenna.close()
