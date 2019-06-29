#client.py

from TxBlock import TxBlock
from Transaction import Tx
import Signetures
import pickle
import socket

TCP_PORT = 5005

def sendBlock(ip_addr,blk):
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((ip_addr,TCP_PORT))
	data = pickle.dumps(blk)
	s.send(data)
	s.close()
	return False


if __name__ == "__main__":
	pr1,pu1 = Signetures.generate_keys()
	pr2,pu2 = Signetures.generate_keys()
	pr3,pu3 = Signetures.generate_keys()

	tx1 = Tx()
	tx1.add_input(pu1,2.3)
	tx1.add_output(pu2,1.0)
	tx1.add_output(pu3,1.1)
	tx1.sign(pr1)

	tx2 = Tx()
	tx2.add_input(pu3,2.3)
	tx2.add_input(pu2,1.0)
	tx2.add_output(pu1,3.1)
	tx2.sign(pr2)
	tx2.sign(pr3)

	B1 = TxBlock(None)
	B1.addTx(tx1)
	B1.addTx(tx2)

	sendBlock('192.168.42.56',B1)





