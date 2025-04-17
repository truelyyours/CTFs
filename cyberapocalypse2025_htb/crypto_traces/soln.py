#NOTE: COMPLETED! 
# HTB{Crib_Dragging_Exploitation_With_Key_Nonce_Reuse!}

from Crypto.Util import Counter
from Crypto.Cipher import AES
from pwn import *

def encrypt(key, msg):
    encrypted_message = AES.new(key, AES.MODE_CTR, counter=Counter.new(128)).encrypt(msg)
    return encrypted_message

def intermediate_decrypt(key, msg):
    l = len(key)
    dec = b''
    ll = len(msg)
    for i in range(ll//l):
        dec += bytes(k^m for k,m in zip(key,msg[i*l: i*l + l]))
        
    if ll%l != 0:
        temp = [i^j for i,j in zip(key, msg[(0 - ll%l):])]
        dec += bytes(temp)
    print("INTERMDIATE DECRYPTE IS::::::::::::::::::::::::::::::::::")
    print(dec)
    print()
    return dec
    # print(":::::::::::::::::::::::::::::::::::::::::::::::::")

enc_key = b''

HOST = "83.136.251.68"
PORT = 56561


conn = remote(HOST, PORT)
def recv_banner():
    print(conn.recvline().decode(), end='')
    print(conn.recvline().decode(), end='')
    print(conn.recvline().decode(), end='')
    print(conn.recvline().decode(), end='')
    print(conn.recvline().decode(), end='')
    print(conn.recvline().decode(), end='')
    print(conn.recvline().decode(), end='')
    # print(conn.recvline())

recv_banner()
# join general
msg = b'join #general'
conn.sendline(msg)
enc_msgs = []
for  i in range(21):
    enc_msgs.append(bytes.fromhex(conn.recvline().decode().strip().split(' ')[-1]))

keystream = bytes(i^j for i,j in zip(enc_msgs[-4], b"Understood. I'm disconnecting now. If they have seen us, we must disappear immediately."))
# print(enc_msgs)
# NOTE: BELOW NOT NEEDED RN
# for m in enc_msgs:
#     intermediate_decrypt(keystream, m)
secret_key = intermediate_decrypt(keystream, enc_msgs[7]).decode().strip().split(' ')[-1]
print("Secret Key::::::::::::::::::::::: ", secret_key)
print(conn.recvline().decode(), end='')
conn.sendline(b'!nick nick')
conn.sendline(b'!leave')
# print(conn.recvline().decode(), end='')
recv_banner()
conn.sendline(b'join #secret ' + secret_key.encode())

# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')
# print(conn.recvline().decode(), end='')

enc_msgs_secret = []
for  i in range(16):
    ww = conn.recvline().decode().strip().split(' ')[-1]
    # print("------------------ ", ww)
    enc_msgs_secret.append(bytes.fromhex(ww))

keystream = bytes(i^j for i,j in zip(enc_msgs_secret[-4], b"We should end this meeting and move to a more secure sanctum. If their mages or spies are closing in, they may intercept our words. We must not take that chance. Let this be the last"))
# keystream = bytes(i^j for i,j in zip(enc_msgs_secret[9], b"Yes, but we must treat it only as a last resort. If we activate it too soon, we risk revealing its location. It is labeled as: HTB{Crib_Dragging_Exploit"))
# 'Yes, but we must treat it only as a last resort. If we activate it too soon, we risk revealing its location. It is labeled as: HTB{Crib_Dragging_Exploitation_With_Key_Nonce_Reuse!}'
# keystream = bytes(i^j for i,j in zip(enc_msgs_secret[5], b"I've been studying the traces left behind by our previous incantations, and something feels wrong. Our network of spells has sent out signals to an unknown "))
# keystream = bytes(i^j for i,j in zip(enc_msgs_secret[4], b"Agreed. The enemy's scouts grow more persistent. If they catch even a whisper of our designs, they will move against us. We must not allow their seers or spies to track our steps."))
# keystream = bytes(i^j for i,j in zip(enc_msgs_secret[-6], b"Good. No record of it must exist in the written tomes. I will ensure all traces are erased, and it shall never be spoken of openly. If the enemy ever learns of it, we will have "))
# keystream = bytes(i^j for i,j in zip(enc_msgs_secret[-5], b"Agreed. The more we discuss it, the greater the risk. Every moment we delay, the Council strengthens its defenses. We must act soon before our window of opportunity closes."))
for m in enc_msgs_secret:
    intermediate_decrypt(keystream, m)

print(conn.recvline().decode(), end='')

