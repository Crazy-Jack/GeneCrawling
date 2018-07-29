import socket
import os
import time


def everyconnect(i, url, host, port=80):
	start = time.time()
	mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mysocket.connect((host,port))
	mysocket.send(cmd(url, i))
	with open('Gene#-'+str(i)+'.html', 'w') as f: 
		while True:
			data = mysocket.recv(1024)
			if len(data) < 1:
				break
			f.write(data.decode())
	mysocket.close()
	end = time.time()
	return end - start




def cmd(url, i):
	return ("GET " + url + str(i) +  " HTTP 1.1 \n\n").encode()
