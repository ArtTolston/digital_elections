from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

key_bob = RSA.generate(2048)

pub_key_bob = key_bob.public_key()

print(pub_key_bob.n)
print(type(pub_key_bob.n))
print(pub_key_bob.e)


priv_key_bob = key_bob
print(priv_key_bob.d)
print(priv_key_bob.p)
print(priv_key_bob.q)

key2 = RSA.generate(2048)

msg = 1000
r = 71

msg_to_sign = msg * (r ** pub_key_bob.e) % pub_key_bob.n

s = pkcs1_15.new(key_bob).sign(msg_to_sign)

