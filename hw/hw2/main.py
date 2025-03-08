from machine import UART, Pin
import time
import re

# Set up UART on pins 0 (TX) and 1 (RX) at 9600 baud
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))


def read_uart():
    if uart.any():
        data = uart.read().decode("utf-8")
        print(data)
        return data
    return ""


first = 1

while True:
    time.sleep(0.2)
    print("--------------")
    received = read_uart()
    if not received:
        continue

    if "Enter your choice:" in received:
        choice = b"1"
        uart.write(choice + b"\n")
        print("Sent:", str(choice))

    if "problem:" in received:
        m = re.search(r"\d+ \+ \d+", received).group(0)
        print("m = ", m)
        mm = eval(m)
        print("mm = ", mm)
        send = str(mm).encode() + b"\n"
        uart.write(send)
