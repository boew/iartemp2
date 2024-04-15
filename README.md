Logging temperature

Raspberry pi (RPi) reads onewire temperature sensors and transmits readings via UART to hos PC.
No (direct) connection to network reduces security concerns.

* RPi reads onewire sensors & transmits readings to UART using pyserial 
* Host PC uses pyserial to receive (and store) readings  

RPi -> USB -> LPC2148 UART1 (by the power led) -> serial cable -> LPC2148 UART1 -> USB -> Host PC

* RPi HW
* RPi HW
** RPi, power supply, keyboard, (HDMI cable to) monitor
** N x ds18B20 connected to +3.3, GND & GPIO4  
** 4k7 (?) pull-up resistor +3.3 <-> GPIO4 

* CDC-UART HW: 
** 2x  LPC2148 kit
** uart cable(s)

* RPi setup 
** in folder serialTx, set up and activate virtual environment as illustrated by dove.bash
** make sure to use the right (LPC2148 virtual) /dev/ttyUSB* port in onewire2serial.py
** "python onewire2serial.py"


* Host PC setup 
** Use EWARM 9.20.2 to build VirtualCom example & flash 2x LPC2148
** in folder serialRx, set up and activate virtual environemnt as illustrated by dove.cmd
** make sure to use the right (LPC2148 virtual) COM port in receiveFromCom.py
** "python receiveFromCom.py"

