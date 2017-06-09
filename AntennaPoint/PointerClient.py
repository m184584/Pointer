import argparse, datetime, logging, pprint, sys
import time, serial

from bin import gpsutils, proxy_mavlink


#initialize the stream of data between pixhawk and computer
def stream(args):
    pprint.pprint('initializing...')
    #defining the home lattitude longitude and altitude
    home_lla = set_home(args)
    #logging the individual values
    logger = logging.getLogger(__name__)
    #setting up the class gpsutils
    helper = gpsutils.GpsUtils()
    #inputed plane telemetry data
    plane_telemetry = proxy_mavlink.MavlinkParser(args.device)
    #connecting to the plane via serial port
    antenna = serial.Serial(args.serialout, 115200, timeout=5, parity=serial.PARITY_NONE)
    while(1):
        #isolating data from the pixhawk
        telemetry  = plane_telemetry.get_telemetry()
        #parsing telementry data into a matrix of lla format
        plane_lla = [telemetry.latitude,telemetry.longitude,telemetry.altitude_msl]
        #converting lla to enu
        enu = helper.lla2enu(home_lla,plane_lla)
        #converting enu to azimuth and elevation
        aziele = helper.enu2azel(enu)
        #output these values as degree values
        output = '%.5f,%.5f\\n' % (helper.rad2deg(aziele[0]),helper.rad2deg(aziele[1]))
        pprint.pprint(output)

def set_home(args):
    pprint.pprint('setting home...')
    #Home is defined as the position of GPS device, connected via serial below
    gps = serial.Serial(args.gpsdevice, 9600, timeout=5, parity=serial.PARITY_NONE)
    time.sleep(0.5)
    #read values that are being sent over the serial port
    serialinput = gps.readline()
    #making a matrix deliminated by the commas
    home = serialinput.split(',')
    #returning the values of lla where gps is located
    return [float(home[0]),float(home[1]),float(home[2])]

def calibrate(args):
    #moves the arm of the antenna for inital calibration
    pprint.pprint('Calibration Routine:')
    pprint.pprint('Press [,] or [.] and enter to move the arm, and [/] to stop motion until arm is vertical.')
    pprint.pprint('Ensure dish is oriented towards true North. When satisfied, enter [m].')

    #connects with the box mbed to move certain distances
    antenna = serial.Serial(args.serialout, 115200, timeout=5, parity=serial.PARITY_NONE)
    feed = ''
    while(feed!='m'):
        #run the calibration sequence until the character 'm' is inputed
        feed = raw_input('>>>')
        antenna.write(feed)


def main():
    #setup logging
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='%(asctime)s: %(name)s: %(levelname)s: %(message)s')

    # Parse command line args.
    parser = argparse.ArgumentParser(description='USNA SUAS Antenna Pointing CLI.')
    parser.add_argument('--serialout',
                        type=str,
                        help='Serial Port for antenna controller.')
    parser.add_argument('--device',
                        type=str,
                        required=True,
                        help='Device Address for MAVLINK connection.')
    parser.add_argument('--gpsdevice',
                        type=str,
                        help='Serial port for GPS device.')
    subparsers = parser.add_subparsers(help='Sub-command help.')
    subparser = subparsers.add_parser(
        'calibrate',
        help='Antenna Calibration.')
    subparser.set_defaults(func=calibrate)
    subparser = subparsers.add_parser(
        'stream',
        help='Stream angles to pointer.')
    subparser.set_defaults(func=stream)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
