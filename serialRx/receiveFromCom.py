# -*- coding: utf-8 -*-
import glob
import time
from pathlib import Path
import sys
from openpyxl import Workbook
import datetime as dt
import serial 


newdir = Path.cwd() / dt.datetime.now().strftime("%Y-%m-%d_%H%M")
newdir.mkdir()
log_txt=newdir / Path(sys.argv[0]).with_suffix('.txt')
log_xlsx=newdir / Path(sys.argv[0]).with_suffix('.xlsx')

wb = Workbook()
ws = wb.active
ws.append(['t [°C]', 'date', 'time', 'id'])

with serial.Serial('COM3', 9600, timeout=None) as ser:
    line = True
    while line:
        line = ser.readline().decode()
        with open(log_txt,'a') as lf:
            print(line, file = lf, end='')
        (rTemp, unit, rDate, rTime, device_id, OK_or_not) = line.split()
        ws.append([rTemp, rDate, rTime, device_id, OK_or_not])
        wb.save(log_xlsx)
        print(line, end = '')
