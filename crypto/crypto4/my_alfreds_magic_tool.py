#!/usr/bin/env python3
from Crypto.Util.number import getPrime
from Crypto.Util.number import bytes_to_long

flag = b"SSM{yay}"

a, b, n = sorted([getPrime(512) for _ in range(3)])

print(f"{a = }")
print(f"{b = }")
print(f"{n = }")


def lcg(x):
    return (a * x + b) % n


flag = bytes_to_long(flag)

for _ in range(bytes_to_long(b"a very very very beautiful number :D")):
    flag = lcg(flag)

flag1 = lcg(flag)
flag2 = lcg(flag1)

print(f"y1 = {hex(flag1 >> 252)}")
print(f"y2 = {hex(flag2 >> 252)}")
