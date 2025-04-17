import random, itertools, tqdm

msg = """Welcome! Here's the flag! It's just encrypted with a vigenere cipher with a random key! The key is a random length, and I randomly picked letters from "squirrelctf" to encrypt the flag! With so much randomness there's no way you can decrypt the flag, right?
Flag: akpffazkzryxgdqqlnafvnlmkvklcy"
"""

characters = 'squirrelctf'

cip = "akpffazkzryxgdqqlnafvnlmkvklcy"

def generate_random_key(length):
    # Characters to choose from
    # Generate a random key
    return ''.join(random.choice(characters) for _ in range(length))

def decrypt(cip, key):
    dec = ''
    kl = len(key)
    for i in range(len(cip)):
        shift = ord(key[i % kl]) - ord('a')
        dec += chr((ord(cip[i]) - shift - ord('a')) % 26 + ord('a'))
    
    return dec

for l in range(5,6):
    for key_tuple in tqdm.tqdm(itertools.product(characters, repeat=l)):

        key = ''.join(key_tuple)
        # key = generate_random_key(l)
        temp_dec = decrypt(cip, key)
        print("DECRYPTED:: ", temp_dec, "__ KEY:: " , key)
    # print()
    # print("DONE for lenght:: ", l)
    # print()


