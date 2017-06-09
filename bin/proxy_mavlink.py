# Module to receive MAVLink packets and forward telemetry via interoperability.
# Packet details at http://mavlink.org/messages/common#GLOBAL_POSITION_INT.

import logging
import sys
import time
import types
from pymavlink import mavutil


class MavlinkParser(object):
    def __init__(self,device):
        self.logger = logging.getLogger(__name__)
        self.PRINT_PERIOD = 5.0
        self.mav = mavutil.mavlink_connection(device, autoreconnect=True)
        self.sent_since_print = 0
        self.last_print = time.time()

    def mavlink_latlon(self,degrees):
        """Converts a MAVLink packet lat/lon degree format to decimal degrees."""
        return float(degrees) / 1e7


    def mavlink_alt(self,dist):
        """Converts a MAVLink packet millimeter format to decimal feet."""
        return dist * 0.00328084


    def mavlink_heading(self,heading):
        """Converts a MAVLink packet heading format to decimal degrees."""
        return heading / 100.0


    def get_telemetry(self):
        """Receives packets over the device (UDP connection) and parses into lat, lon, and alt:

        Args:
            device: A pymavlink device name to forward.

        Returns:

        """
        msg = self.mav.recv_match(type='GLOBAL_POSITION_INT',
                            blocking=True,
                            timeout=10.0)
        if msg is None:
            logger.critical(
                'Did not receive MAVLink packet for over 10 seconds.')
            sys.exit(-1)
        # Convert to telemetry.
        telemetry = types.Telemetry(latitude=self.mavlink_latlon(msg.lat),
                              longitude=self.mavlink_latlon(msg.lon),
                              altitude_msl=self.mavlink_alt(msg.alt),
                              uas_heading=self.mavlink_heading(msg.hdg))

        # Track telemetry rates.
        self.sent_since_print += 1
        self.now = time.time()
        self.since_print = self.now - self.last_print
        if self.since_print > self.PRINT_PERIOD:
            self.logger.info('Telemetry rate: %f Hz', self.sent_since_print / self.since_print)
            self.sent_since_print = 0
            self.last_print = self.now
        return telemetry
