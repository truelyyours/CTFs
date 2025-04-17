from pwn import *
import base64
import os
import signal

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# COORDS = open("coordinates.txt").read().strip()


def encrypt(message, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded)
    return base64.b64encode(iv + ciphertext).decode()


def validate(data, key):
    try:
        data = base64.b64decode(data)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        print("Decrypted: ", decrypted)

        return decrypted == "SHIP:FIRE"
    except Exception as e:
        print("Exception: " , e)
        print("Invalid transmission.")
        raise SystemExit(1)

key = os.urandom(16)
iv = os.urandom(16)

# cip = base64.b64decode(encrypt("SHIP:SAFE", key, iv))
# iiv = cip[:16]
# assert(iiv == iv)
# cip = cip[16:]

# Receiving data from server
conn = remote("mothership.ctf.ritsec.club", 31750)
print(conn.recvline().decode())
print(conn.recvline().decode())
print(conn.recvline().decode())

for _ in range(200):
    temp = conn.recvline().decode().strip()
    print(temp)
    cip = base64.b64decode(temp.split(" ")[-1])
    iiv = cip[:16]
    cip = cip[16:]
    print()
    print("IV & Ciphertext: ", iiv.hex(), cip.hex())

    # need to modify the IV such that decrypted text is "SHIP:FIRE"
    expt_dec = "SHIP:FIRE"
    exploit = b''
    for ind,tt in enumerate(zip("SAFE", "FIRE")):
        exploit += int.to_bytes(ord(tt[0]) ^ ord(tt[1]) ^ iiv[ind + 5])
    mod_iv = iiv[:5] + exploit + iiv[9:]
    assert(len(mod_iv) == 16)
    print("Modified IV: ", mod_iv.hex())
    print()

    # Sending data back to server
    # print(conn.recvline().decode())
    conn.sendline(base64.b64encode(mod_iv + cip).decode())
    print(conn.recvline().decode())
    print(conn.recvline().decode())
print(conn.recvline().decode())
print(conn.recvline().decode())
# print("Validation: ", validate(base64.b64encode(mod_iv + cip).decode(), key))
# mcip = base64.b64decode(encrypt("SHIP:FIRE", key, iv))
# print("IV & Ciphertext: ", mcip.hex())

# The corrds result in 41.1366088, -81.8638384
# Put it in what3words.com and you get ///humans.knee.barn

# def main():
#     print("=== Alien Transmission System ===")
#     print("Welcome to the transmission system.")

#     signal.alarm(11)
#     for i in range(200):
#         key = os.urandom(16)
#         iv = os.urandom(16)

#         print("\nSAFE TRANSMISSION:", encrypt("SHIP:SAFE", key, iv))
#         data = input("SEND TRANSMISSION: ")
#         if not validate(data, key):
#             print("Safe transmission received. Exiting.")
#             return
#         print(f"Attack transmission received ({i + 1}/200). Continue to confirm.")

#     print("Attack mode initiated. Ship coordinates:", COORDS)


# if __name__ == "__main__":
#     main()

