from bin import mbedread, gpsutils, proxy_mavlink
from Test import TestCordinates
import serial, urllib2, time

# setup inital serial port for gps position
#ser1_gps = serial.Serial("COM14")
#ser1_gps.setBaudrate(9600)

#set up second serial port to send azimuth and elevation to antenna pointer
#ser2_antenna = serial.Serial("COM16", 115200,timeout=None,parity=serial.PARITY_NONE)
#read gps position from antenna
#lla1 = mbedread.serrerad(ser1_gps)
lla1 = (0,0,0)

count=0
#substantiantes the class gpsutils
helper = gpsutils.GpsUtils()
lla2_all = TestCordinates.coordinate()
plane_source = proxy_mavlink.MavlinkParser('127.0.0.1:14502')

print lla2_all

while(1):

    #gps position for plane


    enu = lla2_all[count]

    telemetry = plane_source.get_telemetry()

    #converts longitute latitude and altitude to east north up
    #enu = helper.lla2enu(lla2,lla1)
    #print enu

    #converts enu to azimuth and elevation comands
    aziele = helper.enu2azel(enu)

    azieleD = [0,0]
    azieleD[0] = helper.rad2deg(aziele[0])
    azieleD[1] = helper.rad2deg(aziele[1])

    statement = "%.4f,%.4f\\r\\n" % (azieleD[0],azieleD[1])
    #mbedread.serwrite(ser2_antenna,statement)
    print statement
    #time.sleep(5)
    print telemetry.latitude,telemetry.longitude
#ser2_antenna.close()
