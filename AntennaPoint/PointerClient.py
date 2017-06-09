import argparse, datetime, logging, pprint, sys
import time, serial

from bin import mbedread, gpsutils, proxy_mavlink



def stream(args):
    pprint.pprint('initializing...')
    home_lla = set_home(args)
    logger = logging.getLogger(__name__)
    helper = gpsutils.GpsUtils()
    plane_telemetry = proxy_mavlink.MavlinkParser(args.device)
    antenna = serial.Serial(args.serialout, 115200, timeout=5, parity=serial.PARITY_NONE)
    while(1):
        telemetry  = plane_telemetry.get_telemetry()
        plane_lla = [telemetry.latitude,telemetry.longitude,telemetry.altitude_msl]
        enu = helper.lla2enu(home_lla,plane_lla)
        aziele = helper.enu2azel(enu)
        output = '%.5f,%.5f\\n' % (helper.rad2deg(aziele[0]),helper.rad2deg(aziele[1]))
        pprint.pprint(output)
        #mbedread.serwrite(antenna,output)

def set_home(args):
    pprint.pprint('setting home...')
    gps = serial.Serial(args.gpsdevice, 9600, timeout=5, parity=serial.PARITY_NONE)
    time.sleep(1)
    serialinput = gps.readline()
    home = serialinput.split(',')
    return [float(home[0]),float(home[1]),float(home[2])]

def calibrate(args):
    pprint.pprint('Calibration Routine:')
    pprint.pprint('Press [,] or [.] to move the arm, and [/] to stop motion until arm is vertical.')
    pprint.pprint('Ensure dish is oriented towards true North. When satisfied, enter [m].')

    antenna = serial.Serial(args.serialout, 115200, timeout=5, parity=serial.PARITY_NONE)
    feed = ''
    while(feed!='m'):
        feed = raw_input('>>>')
        mbedread.serwrite(antenna,feed)


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
