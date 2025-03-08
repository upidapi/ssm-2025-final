#!/usr/bin/env python3
import string
import gdb
import tempfile
import os

# Initialize GDB and load the binary
gdb.execute("file crackme2")
gdb.execute("b *main+272")  # Set a breakpoint at the specified address

flag = "a" * 0x21  # Initialize the flag with a placeholder of 32 characters

# Define the set of characters to test
charset = string.ascii_letters + string.digits + "{}#$%&'()*+,-./:;<=>?@[\\]^_`|~ "

i = -1
while True:
    i += 1
    found_char = False
    for char in charset:
        new_flag = flag[:i] + char + flag[i+1:]
        print(f"Trying: {new_flag}")

        try:
            # Create a temporary file to simulate stdin
            with tempfile.NamedTemporaryFile() as temp_input:
                temp_input.write(new_flag.encode())
                temp_input.flush()

                # Run the program with stdin redirected from the temporary file
                gdb.execute(f"run < {temp_input.name}")

                # After hitting the breakpoint, calculate the address at rbp - 0x28
                rbp_value = int(gdb.parse_and_eval("$rbp"))
                target_address = rbp_value - 0x28

                # Read the memory at the calculated address
                inferior = gdb.selected_inferior()
                mem_value = inferior.read_memory(target_address, 1)
                mem_value_int = int.from_bytes(mem_value, byteorder='little')

                # Check if the memory value matches the expected length
                if mem_value_int == i + 1:
                    flag = new_flag
                    print(f"Found correct character: {char}")
                    found_char = True
                    break
        except gdb.MemoryError:
            print("Memory access error occurred.")
        except Exception as e:
            print(f"An error occurred: {e}")

    if not found_char:
        # If no character matched, assume the flag is complete
        print("Flag extraction complete.")
        break

print(f"Extracted flag: {flag}")
