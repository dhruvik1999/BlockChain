#server.py
import TxBlock
import socket
import pickle

TCP_PORT = 5005
BUFFER_SIZE = 1024

def newConnect(ip_addr):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((ip_addr,TCP_PORT))
	s.listen()
	return s;

def recvObj(socket):
	new_sock,addr = socket.accept()
	all_data = b''
	while True:
		data = new_sock.recv(BUFFER_SIZE)
		if not data:
			break
		all_data = all_data + data

	return pickle.loads(all_data)

if __name__ == "__main__":
	socket = newConnect('192.168.42.56') 
	newB = recvObj(socket)
	print(newB.data[0])
	print(newB.data[1])

	if newB.is_valid():
		print("Success Tx is valid")
	else:
		print("Error Tx is not valid")




	if(newB.data[0].input[0][1]==2.3):
		print("Suc Input value matches")
	else:
		print("error wrong value for block 1")

	if(newB.data[0].output[0][1]==1.0):
		print("Suc output value matches")
	else:
		print("error wrong value for block 1")

	if(newB.data[0].output[1][1]==1.1):
		print("Suc output value matches")
	else:
		print("error wrong value for block 1")



	if(newB.data[1].input[0][1]==2.3):
		print("Suc Input value matches")
	else:
		print("error wrong value for block 1")

	if(newB.data[1].input[1][1]==1  ):
		print("Suc Input value matches")
	else:
		print("error wrong value for block 1")

	if(newB.data[1].output[0][1]==3.1 ):
		print("Suc output value matches")
	else:
		print("error wrong value for block 1")		




