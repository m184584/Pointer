#Test
import time
file = open('Test/log.txt','w+')
try:
    while True:
        file.write('hello\n')
        time.sleep(0.2)
except KeyboardInterrupt:
    file.close()
    pass
