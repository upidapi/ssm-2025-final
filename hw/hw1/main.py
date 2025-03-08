from machine import UART, Pin
import time

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # Pico Pin 0 = TX, Pin 1 = RX

while True:
    if uart.any():
        data = uart.read().decode('utf-8')  # Read and decode incoming data
        print("Received:", data)
    time.sleep(0.1)

