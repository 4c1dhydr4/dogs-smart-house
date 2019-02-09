#python -m serial.tools.list_ports #en consola brinda una  lista de los puertos disponibles
#python -m serial.tools.miniterm <port_name>
import serial
import time
PORT = 'COM7'
# PORT = '/dev/ttyUSB0'

def read_serialLine():
	try:
		ser = serial.Serial()
		ser.baudrate = 9600
		ser.port = PORT
		ser.open()
		flag = True
		if ser.is_open:
			while flag:
				ser.flushInput()
				time.sleep(1)
				s = ser.readline()
				try:
					serial_line = s.decode()
				except:
					serial_line = False

				if serial_line:
					flag = False
					ser.close()
		else:
			print("puerto no disponible")
			serial_line = "@@"
	except:
		print("Puerto no disponible")
		serial_line = "@NODATA@"
	return serial_line

def decode_serial():
	serial_line = read_serialLine()
	while not (serial_line):
		serial_line = read_serialLine()
	lista = serial_line.split("@")
	lista.remove(lista[0])
	lista.remove(lista[-1])
	return lista

#print(decode_serial(serial_line))

def read_status():
	status = {'moving':False,'sound':False}
	decode_list = decode_serial()
	if decode_list:
		for data in decode_list:
			sensor = data[0]
			if(sensor == "M"):
				status['moving'] = float(data[2:])
			if(sensor == "S"):
				status['sound'] = float(data[2:])
	return status

def send_data(mjs):
	try:
		ser = serial.Serial()
		ser.baudrate = 9600
		ser.port = PORT
		ser.open()
		for x in range(0,3):
			ser.write(mjs.encode())
			time.sleep(1)
		ser.close()
		return True
	except:
		return False

def start():
	stat = read_status()
	return stat
#print(controler_status)


