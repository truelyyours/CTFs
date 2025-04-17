from pwn import *
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long

# from aes import *

# context.encoding = None  # Disable automatic UTF-8 encoding
HOST = "challenge.capturepoint5353.tech"
PORT = 1337

IV = long_to_bytes(0xa0a1a2a3a4a5a6a7a8a9aaabacadaeaf)
ciphertext = long_to_bytes(0x20cccccfe4b301287dc0b3cd0c59c8f94f639242323f3524eb28b1125c2d43bcf189a32a171701277a27d1add688bd93a48d92c450dc7d8e282f28fe80090e36)

conn = remote(HOST, PORT)

def send_plaintext(plaintext):
    conn.recvuntil(b'Enter plaintext (hex): ')
    conn.sendline(plaintext.hex())
    ciphertext = bytes.fromhex(conn.recvline().strip().decode())
    return ciphertext

def recv_line(end_l=''):
    print(conn.recvline().decode(), end=end_l)

def repeated_rec():
    recv_line('')
    print(conn.recvuntil(b': ').decode(),end='\n')
    print()

for i in range(1,2):
    repeated_rec()
    str_to_send = b'\xff' # bytes.fromhex('20cccccfe4b301287dc0b3cd0c59c8f94f639242323f3524eb28b1125c2d43bcf189a32a171701277a27d1add688bd93a48d92c450dc7d8e282f28fe80090e36')#b'c'*16 + b'\x0f'*32 #+ (16).to_bytes()*16
    print("SENDING: ", str_to_send)
    conn.send(str_to_send)
    conn.send('\n')
    recv_line()

exit()
# Step 1: Determine the influence of each plaintext byte on ciphertext bytes
# This step involves sending plaintexts with one byte set and observing changes in ciphertext
# For simplicity, we'll proceed under the assumption that each key byte affects specific ciphertext bytes

# Step 2: Brute-force each key byte
def recover_key():
    key = bytearray(16)
    for pos in range(16):
        print(f"Brute-forcing key byte {pos}...")
        base_plaintext = bytearray(16)
        # Get base ciphertext with all zeros
        base_ciphertext = send_plaintext(base_plaintext)
        found = False
        for guess in range(256):
            # Create plaintext with current guess at position pos
            pt = bytearray(16)
            pt[pos] = guess
            ct = send_plaintext(pt)
            # Here, we would compare the ciphertext with expected patterns
            # For this example, assume the correct guess results in ct matching certain criteria
            # In practice, you need to model how the key byte affects ciphertext bytes
            # This requires understanding the faulty MixColumns, which may vary
            # This is a simplified example; actual implementation requires detailed analysis
            # For the sake of this example, assume the correct key byte is found when ciphertext matches a condition
            if ct[0] == 0x20:  # Example condition, adjust based on actual analysis
                key[pos] = guess
                found = True
                break
        if not found:
            print(f"Failed to find key byte {pos}")
            return None
    return bytes(key)

# Recover the key
master_key = recover_key()
print(f"Recovered Master Key: {master_key.hex()}")

# Decrypt the given ciphertext using the recovered key
def decrypt_ciphertext(ciphertext_hex, key):
    cipher = AES(key)
    ciphertext = bytes.fromhex(ciphertext_hex)
    plaintext = b''
    # Assuming ECB mode, decrypt each block
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        block_int = int.from_bytes(block, 'big')
        decrypted_block = cipher.decrypt(block_int)
        plaintext += decrypted_block.to_bytes(16, 'big')
    return plaintext

# Given ciphertext
ciphertext_hex = "20cccccfe4b301287dc0b3cd0c59c8f94f639242323f3524eb28b1125c2d43bcf189a32a171701277a27d1add688bd93a48d92c450dc7d8e282f28fe80090e36"
decrypted = decrypt_ciphertext(ciphertext_hex, master_key)
print(f"Decrypted: {decrypted}")