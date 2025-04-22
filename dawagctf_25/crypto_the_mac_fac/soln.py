from pwn import *
from Crypto.Cipher import AES
from Crypto.Util.strxor import *
from Crypto.Util.number import *
from Crypto.Util.Padding import *
from Crypto.Random import get_random_bytes

HOST = "connect.umbccd.net" 
PORT = 27811

IV = b'g\x19\x85_\xa7\x06\xcfw\x81I\x01\xfc\xec\x14\x03.'
NULL_IV = b'\x00'*16

def xor(data: bytes, key: bytes) -> bytes: #Installing pwntools in docker was giving me issues so I have to port over xor from strxor
    repeated_key = (key * (len(data) // len(key) + 1))[:len(data)]
    return strxor(data, repeated_key)

# assert(len(mac_key) == 16)
# assert(len(xor_key) == 16)

conn = remote(HOST, PORT)

# Helper functions
def custom_recvline():
    print(conn.recvline().decode().strip())
def custom_recvuntil(delim):
    print(conn.recvuntil(delim).decode().strip())

def recv_menu():
    for i in range(6):
        custom_recvline()

# def for_input():
#     print(conn.recvuntil(b'> ').decode().strip())
def send_option(opt):
    "Send option 1-5"
    custom_recvuntil(b'> ')
    conn.sendline(opt.encode())

def send_message(msg):
    """Send a "message" to be tagged i.e. encrypted."""
    custom_recvuntil(b'Message: ')
    conn.sendline(msg)
    print("Message Sent:: ", conn.recvline().decode().strip())

def send_IV(iv):
    """Send IV"""
    custom_recvuntil(b'hex): ')
    conn.sendline(iv)

def get_tag():
    """Return the tag for previouly i.e. most recently sent message"""
    custom_recvuntil(b'is:  ')
    return conn.recvline().decode().strip()

def get_log_line():
    """Return (msg-hex, iv_hex) for given one log entry line"""
    custom_recvuntil(b'msg=')
    msg_hex = conn.recvuntil(b', ', True).decode().strip()
    custom_recvuntil(b'IV=')
    iv_hex = conn.recvline().decode().strip()
    return (msg_hex, iv_hex)

custom_recvline()
# custom_recvline()
recv_menu()
custom_recvline()

# For gettting tag once
send_option('1')
send_message(b'1'*16)
send_IV(NULL_IV.hex().encode())
tag = get_tag()
print("TAG for 16 1s: ", tag)

# View Logs
recv_menu()
# custom_recvline()
send_option('3')
# custom_recvline()
# 1st log is for admin setup
admin_msg_hex, admin_iv_hex = get_log_line()

# Because I sent a NULL bytes IV, my messages IV in log entry will be simply the key repeated nultiple time, ig!
my_msg_xored_hex, iv_xored_hex = get_log_line()

print("Supposedly xor_key:: ", iv_xored_hex)
# print("16 1s xored is: ", my_msg_xored_hex, len(my_msg_xored_hex))
print("If 16 1s then noice:: ", unpad(xor(bytes.fromhex(my_msg_xored_hex), bytes.fromhex(iv_xored_hex)), 16))

xor_key_recovered = bytes.fromhex(iv_xored_hex)
admin_passphrase = unpad(xor(bytes.fromhex(admin_msg_hex), xor_key_recovered), 16)
print("Admin message: ", admin_passphrase)

# print("Admin IV: ", admin_iv_hex, len(admin_iv_hex))
admin_iv_bytes = xor(bytes.fromhex(admin_iv_hex), xor_key_recovered)

# get admin's tag
recv_menu()
send_option('1')
send_message(admin_passphrase)
send_IV(admin_iv_bytes.hex().encode())
admin_tag = get_tag()
print("TAG for admin passphrase ", admin_tag)

# Attempt to send admin phrase
recv_menu()
send_option('4')

custom_recvuntil(b'passphrase: ')
custom_msg = b'\x00'*16 + admin_passphrase[16:]
custom_msg_pad = pad(custom_msg, 16)
admin_msg_pad = pad(admin_passphrase, 16)
assert(len(custom_msg_pad) == len(admin_msg_pad))
new_iv = strxor(admin_iv_bytes, admin_msg_pad[:16])
conn.sendline(custom_msg)
send_IV(new_iv.hex().encode())

custom_recvuntil(b'hex): ')
conn.sendline(admin_tag.encode())

# ERROR in verif:
custom_recvline()
custom_recvline()
custom_recvline()
# FLAG: DawgCTF{m0r3_r4nd0mne55_15_n0t_4lw4y5_m0r3_53cur3}