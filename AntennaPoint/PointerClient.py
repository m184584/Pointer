import argparse, datetime, logging, pprint, sys
import time, serial

from bin import mbedread, gpsutils, proxy_mavlink


logger = logging.getLogger(__name__)
helper = gpsutils.GpsUtils()

def stream(args):
    home_lla = set_home(args)
    helper = gpsutils.GpsUtils()
    plane_telemetry = proxy_mavlink.MavlinkParser(args.device)
    antenna = serial.Serial(serialout, 115200, timeout=None, parity=serial.PARITY_NONE)
    while(1):
        telemetry  = plane_telemetry.get_telemetry()
        plane_lla = [telemetry.latitude,telemetry.longitude,telemetry.altitude_msl]
        enu = lla2enu(home_lla,plane_lla)
        aziele = helper.enu2azel(enu)

def set_home(args):
    gps = serial.Serial(args.gpsdevice, 115200, timeout=None, parity=serial.PARITY_NONE)
    time.sleep(1)
    serialinput = gps.readline()
    home = serialinput.split(',')
    return [float(home[0]),float(home[1]),float(home[2])]

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
        'stream',
        help='Stream angles to pointer.')
    subparser.set_defaults(func=stream)
    subparser.set_defaults(func=set_home)
    args = parser.parse_args()
    if args.serialout:
        serialout = args.serialout
    else:
        serialout = 'COM16'
    args.func(args)

if __name__ == '__main__':
    main()
