import base64, string, math

cip = "PFFUQYTUONPSK5LAMNDXGJ35ER4CM5C7ORETY3A="

def hamming_distance_bytes(text1: bytes, text2: bytes) -> int:
    """Given two stream of bytes, the function returns the Hamming Distance
    between the two.
    Note: If the two texts have unequal lengths, the hamming distance is
    computed only till one of the text exhausts, other bytes are not iterated.
    """
    dist = 0
    for byte1, byte2 in zip(text1, text2):
        dist += bin(byte1 ^ byte2).count('1')
    return dist

def hamming_score_bytes(text1: bytes, text2: bytes) -> float:
    """Given two streams of bytes, the function computes a normalized Hamming
    Score based on the Hamming distance.
    Normalization is done by dividing the Hamming Distance by the number of bits
    present in the shorter text.
    """
    return hamming_distance_bytes(text1, text2) / (8 * min(len(text1), len(text2)))

def compute_key_length(text: bytes) -> int:
    """The function returns the length of the encryption key
    by chunking and minimizing the Average Hamming Score
    """
    min_score, key_len = None, None

    # We check for chunk lengths from 2 till the half the length of the
    # plain text. Here we assume that the Encryption Key had to be
    # repeated at least twice to match the length of the plaintext
    for klen in range(2, math.ceil(len(text)/2)):

        # We create chunks such that length of each chunk if `klen`
        chunks = [
            text[i: i+klen]
            for i in range(0, len(text), klen)
        ]

        # To gain better accuracy we get rid of the last chunk that had
        # length smaller than klen/2
        if len(chunks) >= 2 and len(chunks[-1]) <= len(chunks[-2])/2:
            chunks.pop()

        # For each chunk length, for every pair of chunks we compute the
        # Hamming Score and keep piling it in a list.
        _scores = []
        for i in range(0, len(chunks) - 1, 1):
            for j in range(i+1, len(chunks), 1):
                score = hamming_score_bytes(chunks[i], chunks[j])
                _scores.append(score)

        # The Hamming Score for a chunk length is the average
        # hamming score computed over all possible pairs of chunks
        score = sum(_scores) / len(_scores)

        # Keep track of the minimum score we have seen and the key length
        # corresponding to it.
        if min_score is None or score < min_score:
            min_score, key_len = score, klen

    # return the key length corresponding to the minimum score
    return key_len

cip_64 = base64.b64decode(cip).decode('latin-1')
cip_32 = base64.b32decode(cip).decode('latin-1')
cip_85 = base64.b85decode(cip)
print("Decode 64:", cip_64, "LEN: ", len(cip_64))
print("Decode 32:", cip_32, "LEN: ", len(cip_32))

print("KeyLength for 64byte decode: ", compute_key_length(cip_64))
print("Key length for 32 byte decode: ", compute_key_length(cip_32))

printables = string.printable

def decrypt_xor(cip, key):
    arr = []
    for i,c in enumerate(cip):
        arr.append(chr(c^key[i%len(key)]))
    return ''.join(arr)

print(decrypt_xor(cip_32, b'\x3a\x02\x1c\x19\x01\xff\xff')) # ends with \x11
print(decrypt_xor(cip_64, b'\x7f\x18\x00:\xff\xff')) # ends with \x11
# for c in string.printable:
#     print("CHARS: ", c, " __ ", decrypt_xor(cip_64, '59'.encode()))
# print(decrypt_xor(cip_85, b'\x1b\x06\x06'))
# for i in printables:
# CIt{yUp_5m9_nUU_rOttXN_MbO2mNyVXSDkl2OT0m72}