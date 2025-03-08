import requests
from PIL import Image
import cv2
import subprocess

# Create a ZXing decoder
# reader = zxing.BarCodeReader()

url = "https://qrgb.ctfchall.se:50000"


def fetch_image(path):
    # print(url + path)
    r = requests.get(url + path)
    with open("image.png", "wb") as f:
        f.write(r.content)


def get_image(data):
    data = {"data": data}  # The payload

    try:
        response = requests.post(
            url + "/generate_qr", json=data, timeout=10
        )  # Send POST request with JSON data
        # print("Response Status Code:", response.status_code)
        return response.text

    except requests.exceptions.RequestException as e:
        print("Error:", e)

import string


fetch_image(get_image("AB" + "AB" * 36 + "AB"))
# fetch_image(get_image("AB" * 38))


# Open an image file
image = Image.open("image.png")

# Convert the image to RGB mode if it's not
image = image.convert("RGB")

# Get the width and height of the image
width, height = image.size


def to_bin(d):
    return (bin(d)[2:] + "0" * 8)[:8]


def print_colors(r, g, b):
    print(to_bin(r), to_bin(g), to_bin(b))


# Iterate through all pixels

# most_common = {}
# ma = [0, 0, 0]
#
for y in range(height):
    for x in range(width):
        r, g, b = image.getpixel((x, y))
        c = (r, b, g)
        print_colors(*c)
#
#         ma = [
#             max(ma[0], r),
#             max(ma[1], g),
#             max(ma[2], b),
#         ]
#
#         if c in most_common:
#             most_common[c] += 1
#         else:
#             most_common[c] = 1
#
# m = sorted(most_common.items(), key=lambda x: x[1], reverse=True);
# for c, count in m:
#     print(count, c)
#
# replace = m[0][0] if m[0][0] != (0, 0, 0) else m[1][0]
# print(ma)

d = 0
for i in range(0):
    qr_code = Image.new("RGB", (width, height), color="white")
    has_non = False

    for y in range(height):
        for x in range(width):
            
            r, g, b = image.getpixel((x, y))
            
            val = (to_bin(r) + to_bin(g) + to_bin(b))[i] == "1"
            c = 255 if val else 0
            qr_code.putpixel((x, y), (c, c, c))

            has_non = has_non or val

    if not has_non:
        continue

    qr_code = qr_code.resize((width * 10, height * 10), Image.NEAREST)
    
    qr_code.save("qrcode.png")
    qr_code.show()
    
    try:
        res = subprocess.check_output(", qrrs --read qrcode.png", shell=True)
        print(f"{res}")
    except subprocess.CalledProcessError:
        pass


    # # Open the desired image (can also be a jpg)
    # img = cv2.imread("qrcode.png")
    # # Instantiate a new detector object
    # detector = cv2.QRCodeDetector()
    # # Decode the image
    # data = detector.detectAndDecode(img)
    # # Show the results

    # print()
