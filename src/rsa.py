import numpy as np
import sympy as sp
import math


class RsaKeyPublic:
    def __init__(self, e, n):
        self.e = e
        self.n = n


class RsaKeyPrivate:
    def __init__(self, e, d):
        self.d = e
        self.n = d


class RSA:
    def __init__(self, keysize):
        assert math.log2(keysize) == int(math.log2(keysize))
        self.keysize = keysize

        self.public_key = RsaKeyPublic(0, 0)
        self.private_key = RsaKeyPrivate(0, 0)
        self._p = 0
        self._q = 0

    def generate_keys(self):
        limits = (2**(self.keysize-1), 2**self.keysize - 1)
        self._p = sp.randprime(limits[0], limits[1])
        self._q = sp.randprime(limits[0], limits[1])
        n = self._p * self._q

        phi = (self._p - 1) * (self._q - 1)
        e = sp.randprime(3, phi-1)
        d = pow(e, -1, phi)

        self.public_key = RsaKeyPublic(e, n)
        self.private_key = RsaKeyPrivate(d, n)

    def encrypt(self, msg):
        return pow(msg, self.public_key.e, self.public_key.n)

    def decrypt(self, cph):
        return pow(cph, self.private_key.d, self.private_key.n)

    def sign(self, msg):
        return pow(msg, self.private_key.d, self.private_key.n)

    def check_sign(self, sign, cph):
        return pow(sign, self.public_key.e, self.public_key.n) == self.decrypt(cph)


if __name__ == '__main__':
    m = 123
    rsa = RSA(32)
    rsa.generate_keys()
    p = rsa.encrypt(m)
    print(p, rsa.decrypt(p))
