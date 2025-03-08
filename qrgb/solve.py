import requests
from PIL import Image
from pyzbar.pyzbar import decode


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


fetch_image(
    get_image(
        "öasjdfjklasfdjklöaskjlöaslkjöaslkjöasöjlsafdljsöfksdlfsaddfjlkökjlösakjlöasfkjlöasfkjlasfdkjlösjklökjlöasfdsalskjdlkasdjlkajsdlkdjaslkdjlaskjdhjashflkjasdhfkljashdkfhasdjfklhaskjdfhasdkjfhlkwehfihfbxbcnkjenjjlkkjlaöjklfkjl"
    )
)


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
for y in range(height):
    for x in range(width):
        r, g, b = image.getpixel((x, y))
        print_colors(r, g, b)


# image = Image.new('RGB', (m, n), color='white')
