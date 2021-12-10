from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
import os

key = RSA.generate(1024, os.urandom)
print(key.public_key().export_key())

a = b'message1'

b = b'message2'

hash1 = SHA256.new(a)

signature = pkcs1_15.new(key).sign(hash1)

print(hash1.hexdigest())

pubkey = key.public_key()

pkcs1_15.new(pubkey).verify(SHA256.new(b), signature)
