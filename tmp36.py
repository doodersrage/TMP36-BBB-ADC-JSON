import Adafruit_BBIO.ADC as ADC
import time
import socket
import sys
import json

sensor_pin = 'P9_40'
HOST = ''
PORT = 8181

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serv.bind((HOST, PORT))
serv.listen(5)
while True:
    conn, addr = serv.accept()

    ADC.setup()

    reading = ADC.read(sensor_pin)
    millivolts = reading * 1800  # 1.8V reference = 1800 mV
    temp_c = (millivolts - 500) / 10
    temp_f = (temp_c * 9/5) + 32
    
    m = {"mv": millivolts, "C": temp_c, "F": temp_f}
    
    dataj = b"HTTP/1.1 200 OK\r\nContent-type: text/html\r\n\r\n"+json.dumps(m).encode('utf-8')

    #print dataj
    conn.send(dataj)
    conn.recv(4096)
    conn.close()
    
