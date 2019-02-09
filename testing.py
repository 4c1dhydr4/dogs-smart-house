import time
import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM7'
ser.open()
c = 0
while(True):
	ser.write("ODN\n".encode())
	print(c)
	c = c +1
	time.sleep(1)

