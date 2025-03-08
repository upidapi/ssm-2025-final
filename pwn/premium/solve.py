from pwn import *
import time 

# context.log_level = "debug"

p = process("./chall")
p.recvuntil(b"Choice: ")

def tim(data, loops):
    c = 0

    for i in range(loops):
        # print(i)
        d = ("1\n" + data + "\n") * 100 + "2\naaa\n"

        # p.recvuntil(b"Choice: ")
        s = time.time_ns()
        p.send(d.encode())

        # print("flip")
        p.recvuntil(b"AAA")
        e = time.time_ns()

        # print("ch")
        p.recvuntil(b"Choice: ")

        c +=  e - s

    return c / loops


print(tim("SSM{", 1000))
print(tim("aaaa", 1000))
print(tim("SSM{", 1000))
print(tim("aaaa", 1000))
