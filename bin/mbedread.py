import serial, urllib2, time


def serread(serial_object):
    #while():
        input=serial_object.readline()
        return input


def serwrite(serial_object,data):
    #while():
        serial_object.write(data)