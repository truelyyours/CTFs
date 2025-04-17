from z3 import *
from pwn import *
import secrets
import hashlib
from Crypto.Hash import Poly1305
from Crypto.Cipher import ChaCha20, ChaCha20_Poly1305
from Crypto.Util.number import long_to_bytes

# Verifying if my logic is correct or not!!
my_key = hashlib.sha256(secrets.token_bytes(64)).digest()
my_nonce = secrets.token_bytes(12)

messages = [
    "Did you know that ChaCha20-Poly1305 is an authenticated encryption algorithm?",
    "That means it protects both the confidentiality and integrity of data!"
]
goal = "But it's only secure if used correctly!"

def get_hash(kk, enc_mess):
    cip = Poly1305.Poly1305_MAC(kk[:16], kk[16:32], enc_mess)
    r, s, nonce = ChaCha20._derive_Poly1305_key_pair(my_key, my_nonce)
    print("other rs is:", ChaCha20_Poly1305.new(key=my_key, nonce=my_nonce).encrypt(b'\x00'*32).hex())
    print("GET_HASH rs kk: ", (r + s).hex(), kk.hex())
    return cip.digest()


def my_encrypt(mess):
    cipher = ChaCha20_Poly1305.new(key=my_key, nonce=my_nonce)
    ciphertext, tag = cipher.encrypt_and_digest(mess)
    for_hash = ciphertext
    if len(ciphertext) & 0x0F:
        for_hash += b'\x00' * (16 - (len(ciphertext) & 0x0F))
    for_hash += long_to_bytes(0, 8)[::-1]
    for_hash += long_to_bytes(len(ciphertext), 8)[::-1]
    hh = Poly1305.new(key=my_key, nonce=my_nonce, cipher=ChaCha20, data=for_hash)
    some = ChaCha20_Poly1305.new(key=my_key, nonce=my_nonce).encrypt(b'\x00'*32)
    dsf = get_hash(some, for_hash)
    print("MY_ENCRYPT: ", hh.digest().hex(), tag.hex(), dsf.hex())
    return [ciphertext, tag, my_nonce]

def my_decrypt(mess_enc):
    ciphertext = mess_enc[0]
    tag = mess_enc[1]
    cipher = ChaCha20_Poly1305.new(key=my_key, nonce=my_nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

for message in messages:
    print("Plaintext: " + repr(message))
    message = message.encode()
    # print("Plaintext (hex): " + message.hex())
    ciphertext = my_encrypt(message)
    key_temp = bytes([i^j for i, j in zip(message[:64], ciphertext[0][:64])])
    for_rs = my_encrypt(b'\x00'*32)[0]
    # print(len(for_rs), for_rs.hex(), key_temp[:32].hex())
    assert (key_temp[:32].hex()) == (my_encrypt(b'\x00'*32)[0].hex())

    for_hash = ciphertext[0]
    if len(ciphertext[0]) & 0x0F:
        for_hash += b'\x00' * (16 - (len(ciphertext[0]) & 0x0F))
    for_hash += long_to_bytes(0, 8)[::-1]
    for_hash += long_to_bytes(len(ciphertext[0]), 8)[::-1]
    hash_temp = get_hash(key_temp, for_hash)
    print(key_temp.hex(), ciphertext[1].hex(), hash_temp.hex())
    print("Ciphertext (hex): " + str([i.hex() for i in ciphertext]))
    print()

exit()

host = "activist-birds.picoctf.net" 
port = 55737

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
k1 = int.from_bytes(p1[:64]) ^ int.from_bytes(c1[:64])
k2 = int.from_bytes(p2[:64]) ^ int.from_bytes(c2[:64])

assert k1 == k2
key = bytes.fromhex(hex(k1)[2:])

poly_key = key[:32]

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



assert int.from_bytes(p1)^int.from_bytes(p2) == int.from_bytes(c1)^int.from_bytes(c2)
# Constants
KEY_BITS = 256
NONCE_BITS = 96
WORD_SIZE = 32
NUM_ROUNDS = 20

# Initialize Z3 solver
solver = Solver()

# Key (32 bytes = 256 bits)
key = BitVecs('key_0 key_1 key_2 key_3 key_4 key_5 key_6 key_7', WORD_SIZE)

# Nonce (12 bytes = 96 bits)
nonce = BitVecs('nonce_0 nonce_1 nonce_2', WORD_SIZE)

# ChaCha20 quarter round function
def quarter_round(a, b, c, d):
    a = (a + b) & 0xFFFFFFFF
    d = d ^ a
    d = RotateLeft(d, 16)

    c = (c + d) & 0xFFFFFFFF
    b = b ^ c
    b = RotateLeft(b, 12)

    a = (a + b) & 0xFFFFFFFF
    d = d ^ a
    d = RotateLeft(d, 8)

    c = (c + d) & 0xFFFFFFFF
    b = b ^ c
    b = RotateLeft(b, 7)

    return a, b, c, d

# Initial ChaCha20 state (simplified model with only key + nonce)
def chacha20_state(key, nonce):
    # State: [constants, key, counter, nonce]
    state = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574]  # Constants
    state += key
    state += [BitVec('counter', WORD_SIZE)]
    state += nonce
    return state

# Encrypt function (1 round for simplicity)
def encrypt_block(state):
    a, b, c, d = state[0], state[1], state[2], state[3]
    a, b, c, d = quarter_round(a, b, c, d)
    return a ^ state[0], b ^ state[1], c ^ state[2], d ^ state[3]

# Known Plaintext and Ciphertext (Example placeholders)
P1 = BitVec('P1', WORD_SIZE)
P2 = BitVec('P2', WORD_SIZE)
C1 = BitVec('C1', WORD_SIZE)
C2 = BitVec('C2', WORD_SIZE)

# Keystream recovery constraints
solver.add(C1 ^ P1 == C2 ^ P2)  # XOR Equation for nonce reuse

tc1 = bytes.fromhex('195a2963155894790bb1cc6e91ec5fad74e0dfcf457414e3de663492d594fc3630ab99eedf3cd068019db53d6f56b11c0f85cd85beca84e95e1092d54bde13d7aad980bac108fa4fe5c766265899f5e6246b28f9e40250b3af6b4ff6b719efa6d7157f8cf1944089c0')
tc2 = bytes.fromhex('095b2c374c5a84380eac8370c5b847be6fb4f9c450445ce0832271e2ce90e02760f4c2a8df2b95671bd4b524724aad521a82cac4a3c194ac5c0c98d34b8e08d8e5d3c1afcc4e501b5eab27be981b1feaacd05158c1b119efa6d7157f8cf1944089c0')
# Example constraints (replace with real plaintexts/ciphertexts)
solver.add(P1 == 0x44696420796f75206b6e6f7720746861742043686143686132302d506f6c793133303520697320616e2061757468656e7469636174656420656e6372797074696f6e20616c676f726974686d3f)
solver.add(C1 == int.from_bytes(tc1[:-28]))
solver.add(P2 == 0x54686174206d65616e732069742070726f746563747320626f74682074686520636f6e666964656e7469616c69747920616e6420696e74656772697479206f66206461746121)
solver.add(C2 == int.from_bytes(tc2[:-28]))

# Solve the system
if solver.check() == sat:
    model = solver.model()
    print("Solution Found")
    print(model)
else:
    print("No solution")

