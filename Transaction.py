#Transaction.py
import Signetures

class Tx:

	def __init__(self):
		self.input=[]
		self.output=[]
		self.sigs=[]
		self.reqd=[]

	def add_input(self,from_addr,amount):
		self.input.append((from_addr,amount))

	def add_output(self,to_addr,amount):
		self.output.append((to_addr,amount))

	def sign(self,private_key):
		message = self.__gather()
		newsig = Signetures.sign(message,private_key)
		self.sigs.append(newsig)

	def is_valid(self):
		total_in=0
		total_out=0



		message = self.__gather()
		for addr,amount in self.input:
			found = False

			total_in+=amount

			for s in self.sigs:
				if Signetures.verify(message,s,addr):
					found=True

			if not found:
				return False

			if amount<0:
				return False

		for addr in self.reqd:
			found = False

			for s in self.sigs:
				if Signetures.verify(message,s,addr):
					found=True
			if not found:
				return False

		for addr,amount in self.output:
			total_out+=amount
			if amount <0:
				return False

		if total_out > total_in:
			return False

		return True



	def add_reqd(self,private_key):
		self.reqd.append(private_key)

	def __gather(self):
		data = []
		data.append(self.input)
		data.append(self.output)
		data.append(self.reqd)

		return data

if __name__ == '__main__':
	pr1,pu1 = Signetures.generate_keys()
	pr2,pu2 = Signetures.generate_keys()
	pr3,pu3 = Signetures.generate_keys()
	pr4,pu4 = Signetures.generate_keys()

	tx1 = Tx()
	tx1.add_input(pu1,1)
	tx1.add_output(pu2,1)
	tx1.sign(pr1)

	tx2 = Tx()
	tx2.add_input(pu1,2)
	tx2.add_output(pu2,1)
	tx2.add_output(pu3,1)
	tx2.sign(pr1)


	tx3 = Tx()
	tx3.add_input(pu3,1.2)
	tx3.add_output(pu1,1.1)
	tx3.add_reqd(pu4)
	tx3.sign(pr3)
	tx3.sign(pr4)


	for t in [tx1,tx2,tx3]:
		if t.is_valid():
			print("Success! transacion is valid")
		else:
			print("Error ! transacion is not valid")


	tx4 = Tx()
	tx4.add_input(pu1,1)
	tx4.add_output(pu2,1)
	tx4.sign(pr2)

	#escrow not sign by the arbiter
	tx5 = Tx()
	tx5.add_input(pu3,1.2)
	tx5.add_output(pu1,1.1)
	tx5.add_reqd(pu4)
	tx5.sign(pr3)

	tx6 = Tx()
	tx6.add_input(pu3,1)
	tx6.add_input(pu4,0.1)
	tx6.add_output(pu1,1.1)
	tx6.sign(pr3)

	tx7 = Tx()
	tx7.add_input(pu4,1.2)
	tx7.add_output(pu1,1)
	tx7.add_output(pu2,2)
	tx7.sign(pr4)

	tx8 = Tx()
	tx8.add_input(pu2,-1)
	tx8.add_output(pu1,-1)
	tx8.sign(pr2)


	for t in [tx4,tx5,tx6,tx7,tx8]:
		if t.is_valid():
			print("Error ! is valid")
		else:
			print("Suc !  invalid")











	