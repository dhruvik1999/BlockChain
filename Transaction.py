import Signetures
class Tx:
	input = None
	output =  None
	sigs = None
	reqd = None

	def __init__(self):
		self.input=[]
		self.output=[]
		self.sigs=[]
		self.reqd=[]

	def add_input(self,from_addr,amount):
		self.input.append((from_addr,amount))

	def add_output(self,to_addr,amount):
		self.output.append((to_addr,amount))

	def add_reqd(Self,addr):
		self.reqd.append(addr)

	def sign(self,private):
		message = self.__gather()
		newsig = Signetures.sign(message,private)
		self.sigs.append(newsig)

	def is_valid(self):
		message = self.__gather()
		for addr,amout in self.input:
			found = False

			for s in self.sigs:
				if Signetures.verify(message,s,addr):
					found=True

				if not found:
					return False

		return True

	def __gather(self):
		data = []
		data.append(self.input)
		data.append(self.output)
		data.append(self.reqd)

		return data


if __name__=='__main__':
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
	tx3.add_output(pu3,1.1)
	tx3.sign(pr3)

	for t in [tx1,tx2,tx3]:
		print(t,t.is_valid())

	tx3 = Tx()
	tx3.add_input(pu3,1.2)
	tx3.add_output(pu3,1.1)
	tx3.sign(pr3)

	tx3 = Tx()
	tx3.add_input(pu3,1.2)
	tx3.add_output(pu3,1.1)
	tx3.sign(pr3)

	tx3 = Tx()
	tx3.add_input(pu3,1.2)
	tx3.add_output(pu3,1.1)
	tx3.sign(pr3)

	tx3 = Tx()
	tx3.add_input(pu3,1.2)
	tx3.add_output(pu3,1.1)
	tx3.sign(pr3)
