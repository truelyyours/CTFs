from PIL import Image

def extract_lsb(image_path):
    img = Image.open(image_path)
    pixels = img.load()

    width, height = img.size
    bits = ""

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

    # Convert bits to bytes
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
    decoded = ""
    for byte in bytes_list:
        if len(byte) == 8:
            decoded += chr(int(byte, 2))

    return decoded

def find_flag(decoded_text):
    start = decoded_text.find('CIT{')
    if start == -1:
        return None
    end = decoded_text.find('}', start)
    if end == -1:
        return None
    return decoded_text[start:end+1]

if __name__ == "__main__":
    image_path = "dogpicture.png"  # Make sure the image is in the same folder
    hidden_text = extract_lsb(image_path)
    flag = find_flag(hidden_text)
    if flag:
        print(f"Found flag: {flag}")
    else:
        print("Flag not found!")
