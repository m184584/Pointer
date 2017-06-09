import serial, urllib2, time

#will read values from serial object
def serread(serial_object):
    #while():
    input=serial_object.readline()
    return input

#will write to serial objects
def serwrite(serial_object,data):
    #while():
    serial_object.write(data)
