#Signatures.py
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_keys():
	private = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
		backend=default_backend()
	)
	public = private.public_key()
	pu_ser = public.public_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	return private, pu_ser

def sign(msg,private):
	message = bytes(str(msg),'utf-8')
	sig = private.sign(
		message,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH
		),
		hashes.SHA256()
	)
	return sig

def verify(msg,sig,pub_ser):
	public = serialization.load_pem_public_key(
		pub_ser,
		backend=default_backend()
		)
	msg = bytes(str(msg),'utf-8')
	try:
		public.verify(
			sig,
			msg,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)
		return True
	except InvalidSignature:
		return False
	except:
		print("Error in public key verify ")



if __name__ == '__main__':
	pr,pu = generate_keys()
	print(pr)
	print(pu)
	message = b"ramesh send suresh 2$"
	sig = sign(message,pr)
	print(sig)
	correct = verify(message,sig,pu)

	print(correct)


	pr2,pu2 = generate_keys()
	sig2 = sign(message,pr2)

	message = b"remesh send suresh 200$"


	print(verify(message,sig2,pu2))
