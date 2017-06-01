from math import atan2, sqrt

def enu2azel(enu):
	azimuth = atan2(enu[0],enu[1])
	elevation = atan2(enu[2], sqrt(enu[0]**2+enu[1]**2))
	return [azimuth,elevation]
