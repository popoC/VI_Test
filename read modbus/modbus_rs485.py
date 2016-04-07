from ConfigParser import SafeConfigParser
from PyCRC.CRC16 import CRC16
import serial
import time
from datetime import datetime

FILENAME = datetime.strftime(datetime.now(),'_%Y%m%d%H%M%S_' + 'VIC.txt')
fp = open(FILENAME,'w')

try:
    conf = SafeConfigParser()
    conf.read('modbus_IP_port.conf')
    COM = conf.get('SYSTEM','COMPORT')
    BAUDRATE = conf.getint('SYSTEM','BAUDRATE')
    waittime = conf.getfloat('SYSTEM','FUEL_TIMEOUT')
except:
    print 'No config file'

#COM = 'COM20'

try:
    ser = serial.Serial(COM,BAUDRATE,timeout = 1)
except:
    print 'port open error'
    ser.close()



a='\x01\x03\x00\x00\x00\x08\x44\x0c'

def get_Modbus_TCP_datas(command):
    datas =[]
    ser.write(command)
    time.sleep(0.1)
    bb = ser.readline()
    lenght = len(bb)
    crc16_flag = hex(CRC16(modbus_flag=1).calculate(bb[0:lenght-2]))[2:].zfill(4)
    crc16_flag = crc16_flag[2:4]+crc16_flag[0:2]
        
    if crc16_flag == bb[lenght-2:lenght].encode('hex'):
        V = int((bb[3]+bb[4]).encode('hex'),16)
        I = int((bb[5]+bb[6]).encode('hex'),16)
        C = int((bb[7]+bb[8]).encode('hex'),16)
        strw1 = ''
        cc = datetime.now()
        Sec = cc.hour*60*60 + cc.minute*60 + cc.second
        strw1 = "{:04.2f}".format(float(V)/100)+" "+"{:04.2f}".format(float(I)/100)+" "+"{:04.2f}".format(float(C)/100)
        strw1 = strw1+" "+str(Sec)+'\r\n'
        print strw1
        fp.write(strw1)
        return datas



while True:
    try:
        get_Modbus_TCP_datas(a)
    
    except KeyboardInterrupt:
        fp.close()
        ser.close()
        
        print 'Bye~'

print '         close ~ exit'


