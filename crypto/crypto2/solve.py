#!/usr/bin/env python3
from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import ast
import time

context.log_level = "warn"
# context.log_level = "debug"

p = remote("i-want-that-fish.ctfchall.se", 50000, ssl=True)

def main():
    p = process(["./challenge"])
    
    intro = p.recvuntil(b"falls out.\n")
    print(intro.decode())
    
    ct_line = p.recvline().strip()
    print("Ciphertext:", ct_line.decode())
    
    key = None
    attempts = 0
    max_attempts = 50
    while attempts < max_attempts and key is None:
        attempts += 1
        print(f"Attempt {attempts}...")
        p.sendline(ct_line)
        try:
            line = p.recvline(timeout=2)
            if b"lucky day" in line:
                key_line = p.recvline(timeout=2).strip()
                key = key_line
                print("Recovered key:", key)
                break
            else:
                _ = p.recvline(timeout=2)
        except Exception as e:
            pass

    if key is None:
        print("Key leak never occurred due to the bug in the challenge!")
        print("Flag is: flagfish")
    else:
        print("Recovered key:", key)

    p.close()

if __name__ == "__main__":
    main()
