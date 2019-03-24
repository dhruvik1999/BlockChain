from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
"""

"""

class someClass:
	def __init__(self,myString):
		self.string = myString

	def __repr__(self):
		return self.string 

class CBlock:
	data = None
	previousHash = None
	previousBlock = None

	def __init__(self,data,previousBlock):
		self.data = data
		if previousBlock != None:
			self.previousHash = previousBlock.computeHash() 
			self.previousBlock = previousBlock

	def computeHash(self):
		digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
		digest.update(bytes(str(self.data),'utf-8'))
		digest.update(bytes(str(self.previousHash),'utf-8'))
		return digest.finalize()

if __name__ == '__main__':
	root = CBlock("i am dhruvik",None)
	b1 = CBlock("i am child",root)
	b1.previousHash=root.computeHash()
	b2 = CBlock("i am child 2",root) 
	b2.previousHash=root.computeHash()
	b3 = CBlock(12345,b1)
	b3.previousHash=b1.computeHash()
	b4 = CBlock(someClass('hi'),b2)
	b4.previousHash=b2.computeHash()

	for b in  [b1,b2,b3,b4]:
		if b.previousBlock.computeHash() == b.previousHash:
			print("yes")
		else:
			print("no")

	b1.data = "dhruvik"

	for b in  [b1,b2,b3,b4]:
		if b.previousBlock.computeHash() == b.previousHash:
			print("yes")
		else:
			print("no")
