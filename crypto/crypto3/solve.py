#!/usr/bin/env python3
import requests
import randcrack

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

cracker = randcrack.RandCrack()
url = "https://303-see-other.ctfchall.se:50000"

session = requests.Session()

num_calls = 156

print("[*] Collecting state from robots.txt ...")
for i in range(num_calls):
    resp = session.get(url + "/robots.txt", verify=False)
    text = resp.text.strip()
    try:
        flag_path = text.split("Disallow: /")[1].strip()
    except IndexError:
        print("[-] Could not parse robots.txt response.")
        exit(1)
    value = int(flag_path, 16)
    for shift in range(0, 128, 32):
        chunk = (value >> shift) & 0xffffffff
        print(f"{chunk = }")
        cracker.submit(chunk)
    if (i+1) % 20 == 0:
        print(f"    Collected {i+1} / {num_calls} responses.")

print("[*] State reconstructed, predicting next output ...")
predicted = 0
for shift in range(0, 128, 32):
    predicted |= cracker.predict_getrandbits(32) << shift

predicted_hex = predicted.to_bytes(16, "big").hex()
print(f"[*] Predicted flag path: /{predicted_hex}")

flag_resp = session.get(url + "/" + predicted_hex, verify=False)
print("[*] Flag response:")
print(flag_resp.text)
