import numpy as np
import time

def randGPS():

        #outputs 3 random numbers sbetween 36.88 and 37
        lat = np.random.uniform(36.98,36.98001)
        lng = np.random.uniform(67.0000,67.0001)
        alt = np.random.uniform(0,300)

        array = (lat,lng,alt)

        return array
