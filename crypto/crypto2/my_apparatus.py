#!/usr/bin/env python3
flagfish = b"yay"

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from os import urandom
from random import SystemRandom
import bcrypt
from hashlib import sha256

rng = SystemRandom()

iv = urandom(16)
key = urandom(16)
aes = AES.new(key, AES.MODE_CBC, iv=iv)
magidiced = aes.encrypt(pad(flagfish, 16))

print("You walk up to the apparatus, worryingly observing.")
print("Eventually, a magidiced flagfish falls out.")
print((iv + magidiced).hex())

while True:
    try:
        encrypted = bytes.fromhex(input())
        iv = encrypted[:16]
        encrypted = encrypted[16:]

        aes = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted = aes.decrypt(encrypted)
        plaintext = unpad(decrypted, 16)

        # :see_no_evil:
        r = rng.random()
        print(f"{r = }")
        print(f"{r < 0.2 = }")
        if r < 0.2:
            print(b"It's a lucky day!".encode())
            print(key)

        print("-------------")

        print(
            bcrypt.hashpw(urandom(16) + encrypted + urandom(16), bcrypt.gensalt()).hex()[
                32:96
            ]
        )

    except KeyboardInterrupt:
        print("goodbye!")
        break

    except Exception as e:
        "ono!"
        print(sha256(urandom(16) + encrypted + urandom(16)).hexdigest())
