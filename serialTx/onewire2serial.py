import glob
import time
from pathlib import Path
import sys
from openpyxl import Workbook
import datetime as dt
import serial 
base_dir = '/sys/bus/w1/devices/'

device_files=[]
for device_folder in glob.glob(base_dir + '28*'):
    device_files.append(Path(device_folder + '/w1_slave'))

newdir = Path.cwd() / dt.datetime.now().strftime("%Y-%m-%d_%H%M")
newdir.mkdir()
log_txt=newdir / Path(sys.argv[0]).with_suffix('.txt')
log_xlsx=newdir / Path(sys.argv[0]).with_suffix('.xlsx')

def read_temp_raw(device_file):
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp(device_file):
    #lines = read_temp_raw(device_file)
    #while lines[0].strip()[-3:] != 'YES':
    #    time.sleep(0.2)
    lines = read_temp_raw(device_file)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
    return (temp_c, lines[0].strip()[-3:])

wb = Workbook()
ws = wb.active
ws.append(['t [Â°C]', 'date', 'time', 'id'])
while True:
    for device_file in device_files:
        rDate = time.strftime("%Y-%m-%d")
        rTime = time.strftime("%H:%M:%S")
        (rTemp, OK_or_not) = read_temp(device_file)
        msg = f'{rTemp}\tÂ°C\t{rDate}\t{rTime}\t{device_file}\t{OK_or_not}'
        with open(log_txt,'a') as lf:
            print(msg, file = lf)
        print(msg.replace('\t', '¤'))
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
            ser.write(bytearray(msg, 'utf-8'))
        ws.append([rTemp, rDate, rTime, device_file.parts[-2][-4:], OK_or_not])
        wb.save(log_xlsx)
        #time.sleep(2) # every 2 s
        time.sleep(60) # every minute
    #sensorInRoomWhiteCable="c3798"
    #sensorCorridorGrayCable_sometimes_85="c0482"
