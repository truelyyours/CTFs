import requests
import time

def reverse_f0(w, b):
    b_bytes = [ord(c) for c in b]
    m = len(b_bytes)
    c = []
    for i in range(len(w)):
        w_char = ord(w[i])
        b_char = b_bytes[i % m]
        c_char = w_char ^ b_char
        c.append(chr(c_char))
    return ''.join(c)
    
def f0(msg, key):
    enc = b''
    for ind in range(len(msg)):
        enc += (msg[ind] ^ key[ind % len(key)]).to_bytes()
    return enc

def main():
    url = "http://1it9cere.chals.mctf.io/sea.php"
    b = b'5p1n4chl1f3'
    
    # print(f0(b'ls -al', b))
    # Desired output after f0
    desired_w = b"cat flag.txt"  # Replace with your desired output
    
    # Generate c that will produce desired_w when processed by f0
    last_char = (sum(desired_w) % 255).to_bytes()
    desired_w = desired_w + last_char
    c = f0(desired_w, b)
    print("ACTUAL: ", f0(c, b))
    print(f"Generated c: {c}, {c.hex()}")
    
    # Get current timestamp
    t = int(time.time())
    print(f"Current timestamp: {t}")
    
    # Send GET request
    params = {'c': c.hex(), 't': t}
    response = requests.get(url, params=params)
    
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {f0(bytes.fromhex(response.text), b)}")
# SOLN: Response text: b'MetaCTF{c0ll3ct1ng_s34sh3ll5_fr0m_th3_h4ck3r5_cl4w5}'
if __name__ == "__main__":
    main()