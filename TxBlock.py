#TxBlock
from Blockchain import CBlock
from Signetures import generate_keys,sign,verify
from Transaction import Tx
import pickle
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import random
import time	

reward = 25.0
leading_zeros = 2
next_char=25

class TxBlock (CBlock):
	nonce = "AAAAAA"
	def __init__(self,previousBlock):
		super(TxBlock,self).__init__([],previousBlock)

	def addTx(self,Tx_in):
		self.data.append(Tx_in)

	def __count_totals(self):
		total_in = 0
		total_out = 0

		for tx in self.data:
			for addr,amt in tx.input:
				total_in = total_in + amt

			for addr,amt in tx.output:
				total_out = total_out + amt

		return total_in,total_out

	def is_valid(self):
		if not super(TxBlock,self).is_valid():
			return False
		for tx in self.data:
			if not tx.is_valid():
				return False
		total_in,total_out = self.__count_totals()
		if total_out - total_in - reward > 0.000000000001:
			return False
		return True

	def good_nonce(self):
		digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
		digest.update(bytes(str(self.data),'utf-8'))
		digest.update(bytes(str(self.previousHash),'utf-8'))
		digest.update(bytes(str(self.nonce),'utf-8'))
		this_hash = digest.finalize()

		if this_hash[:leading_zeros] != bytes(''.join( ['\x4f' for i in range(leading_zeros)]),'utf-8'):
			return False
		else:
			return int(this_hash[leading_zeros]) < next_char 

	def find_nonce(self):
		for i in range(1000000):
			self.nonce = ''.join([chr(random.randint(0,255)) for i in range(10*leading_zeros) ])
			if self.good_nonce(): 
				return self.nonce
		return None

if __name__ == "__main__":
	pr1,pu1 = generate_keys()
	pr2,pu2 = generate_keys()
	pr3,pu3 = generate_keys()
	pr4,pu4 = generate_keys()

	tx1 = Tx()
	tx1.add_input(pu1,1)
	tx1.add_output(pu2,1)
	tx1.sign(pr1)

	#print(tx1.is_valid())
	if tx1.is_valid():
		print("Success Tx is valid")

	savefile=open("tx.dat","wb")
	pickle.dump(tx1,savefile)
	savefile.close()

	loadfile = open("tx.dat","rb")
	newTx = pickle.load(loadfile)
	loadfile.close()

	#print(newTx.is_valid())
	if newTx.is_valid():
		print("success , loaded tx1 is valid")


	root = TxBlock(None)
	root.addTx(tx1)

	tx2 = Tx()
	tx2.add_input(pu2,1.1)
	tx2.add_output(pu3,1)
	tx2.sign(pr2)
	root.addTx(tx2)

	B1 = TxBlock(root)

	tx3 = Tx()
	tx3.add_input(pu3,1.1)
	tx3.add_output(pu1,1)
	tx3.sign(pr3)
	B1.addTx(tx3)

	tx4 = Tx()
	tx4.add_input(pu1,1)
	tx4.add_output(pu2,1)
	tx4.add_reqd(pu3)
	tx4.sign(pr1)
	tx4.sign(pr3)
	B1.addTx(tx4)

	start = time.time();

	print(B1.find_nonce())
	elapsed = time.time()-start;
	print("Time : ",elapsed);
	
	if elapsed < 60:
		print("Error ! Minning Error Minning to fast")

	if B1.good_nonce():
		print("Suc Nonce is good")
	else:
		print("Error! Bad nonce")


	B1.is_valid()
	root.is_valid()

	savefile = open("block.dat","wb")
	pickle.dump(B1,savefile)
	savefile.close()

	loadfile = open("block.dat","rb")
	load_B1 = pickle.load(loadfile)
	loadfile.close()

	load_B1.is_valid()

	for b in [root,B1,load_B1,load_B1.previousBlock]:
		if b.is_valid():
			print("success! valid block")
		else:
			print("ERROR! Bad block")

	if B1.good_nonce():
		print("Suc Nonce is good after save and load")
	else:
		print("Error! Bad nonce after save and load")


	B2 = TxBlock(B1)
	tx5 = Tx()
	tx5.add_input(pu3,1)
	tx5.add_output(pu1,100)
	tx5.sign(pr3)
	B2.addTx(tx5)

	load_B1.previousBlock.addTx(tx4)
	for b in [ B2 , load_B1 ]:
		if b.is_valid():
			print("Error ! Bad block varified")
		else:
			print("Success ! Bad block detected") 


	#test mining rewards and tx fees
	B3 = TxBlock(B2)
	B3.addTx(tx2)
	B3.addTx(tx3)
	B3.addTx(tx4)

	tx6 = Tx()
	tx6.add_output(pu4,25)
	B3.addTx(tx6)

	if B3.is_valid():
		print("Success ! block reward succeeds")
	else:
		print("error ! block reward fail")


	B4 = TxBlock(B3)
	B4.addTx(tx2)
	B4.addTx(tx3)
	B4.addTx(tx4)

	tx7 = Tx()
	tx7.add_output(pu4,25.2)
	B4.addTx(tx7)

	if B4.is_valid():
		print("Success ! Tx fees succeeds")
	else:
		print("error ! Tx fees fail")


	#Greedy miners

	B5 = TxBlock(B4)
	B5.addTx(tx2)
	B5.addTx(tx3)
	B5.addTx(tx4)

	tx8 = Tx()
	tx8.add_output(pu4,26.2)
	B5.addTx(tx8)

	if not B5.is_valid():
		print("Success ! greedy miners detected")
	else:
		print("error ! greedy miners not detected")

