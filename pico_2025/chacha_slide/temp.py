from pwn import *

host = "activist-birds.picoctf.net" 
port = 62407

proc = remote(host, port)

def get_something():
    l = proc.recvuntil(b'hex): ')
    print(l)
    print()
    return bytes.fromhex(proc.recvline().strip().decode())

def pad16(data: bytes) -> bytes:
    """Pad data to a multiple of 16 bytes."""
    padding_len = (16 - (len(data) % 16)) % 16
    return data + bytes(padding_len)

p1 = get_something()
c1_temp = get_something()
c1 = c1_temp[:-28]
c1_tag = c1_temp[-28:-12]

p2 = get_something()
c2_temp = get_something()
c2 = c2_temp[:-28]
c2_tag = c2_temp[-28:-12]

assert c1_temp[-12:] == c2_temp[-12:]
nonce = c1_temp[-12:]
print(nonce)

print("ONE: ", p1, c1, c1_tag.hex())
print("TWO: ", p2, c2, c2_tag.hex())

assert len(p1) == len(c1)
print("lenghts: ", len(p1), len(p2))
k1 = int.from_bytes(p1[:70]) ^ int.from_bytes(c1[:70])
k2 = int.from_bytes(p2[:70]) ^ int.from_bytes(c2[:70])

assert k1 == k2
key = bytes.fromhex(hex(k1)[2:])

poly_key = key[:32]

from Crypto.Hash import Poly1305
from Crypto.Cipher import ChaCha20, ChaCha20_Poly1305

idk = pad16(c2) + len(b"").to_bytes(8, 'little') + len(c2).to_bytes(8, "little")
cip = Poly1305.Poly1305_MAC(poly_key[:16], poly_key[16:],None)
cip.update(idk)
print(c2_tag.hex(), cip.digest().hex())

enc = b""
goal = ("But it's only secure if used correctly!").encode()

for i, c in enumerate(goal):
    enc += ( c ^ key[i]).to_bytes()

tag = Poly1305.Poly1305_MAC(poly_key[:16], poly_key[16:], pad16(enc) + bytes(8) + len(enc).to_bytes(8,'little')).digest()
# print(tag, ChaCha20_Poly1305.new(key=poly_key, nonce=nonce).digest())
print(proc.recvuntil(b'message? '))
proc.sendline((enc + tag + nonce).hex().encode())

proc.recvuntil(b'decrypted): ')
print(proc.recvline())

