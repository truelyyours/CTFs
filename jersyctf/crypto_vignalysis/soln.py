from collections import defaultdict, Counter
import math


ciphertext = open('encryptedText.txt', 'rb').read().decode()

# Kasiski Examination (Key Length Detection)

def find_repeated_sequences(ciphertext, min_len=4):
    sequences = defaultdict(list)
    for i in range(len(ciphertext) - min_len + 1):
        seq = ciphertext[i:i+min_len]
        sequences[seq].append(i)
    return {seq: positions for seq, positions in sequences.items() if len(positions) > 1}

def compute_gcds(positions):
    distances = []
    for i in range(1, len(positions)):
        distances.append(positions[i] - positions[i-1])
    return distances

def kasiski_examination(ciphertext, max_key_len=30):
    repeated_sequences = find_repeated_sequences(ciphertext)
    distance_gcds = []
    
    for seq, positions in repeated_sequences.items():
        distances = compute_gcds(positions)
        for d in distances:
            for k in range(2, max_key_len + 1):
                if d % k == 0:
                    distance_gcds.append(k)
    
    # Count most common GCDs
    cc = Counter(distance_gcds).most_common(8)
    ans = []
    for i in cc:
        ans.append([i[0], i[1] *100 / len(distance_gcds)])
    return ans

# Example usage:
print("Kasiski Examination")
print(kasiski_examination(ciphertext))
print()

# Index of Coincidence
def index_of_coincidence(ciphertext, key_len):
    total_ic = 0.0
    for i in range(key_len):
        group = ciphertext[i::key_len]
        freq = [0] * 26
        for c in group:
            freq[ord(c) - ord('a')] += 1
        n = len(group)
        if n < 2:
            continue
        ic = sum(f * (f - 1) for f in freq) / (n * (n - 1))
        total_ic += ic
    return total_ic / key_len

def find_key_length_ic(ciphertext, max_len=20):
    ics = []
    for k in range(1, max_len + 1):
        ics.append((k, index_of_coincidence(ciphertext, k)))
    # Sort by closeness to English IC (~0.0667)
    ics.sort(key=lambda x: abs(x[1] - 0.0667))
    return ics[:5]

# Example usage:
print("Index of Coincidence")
print(find_key_length_ic(ciphertext))
print()

# Frequency Analysis

english_freq = [
    0.08167, 0.01492, 0.02782, 0.04253, 0.12702,  # a, b, c, d, e
    0.02228, 0.02015, 0.06094, 0.06966, 0.00153,  # f, g, h, i, j
    0.00772, 0.04025, 0.02406, 0.06749, 0.07507,  # k, l, m, n, o
    0.01929, 0.00095, 0.05987, 0.06327, 0.09056,  # p, q, r, s, t
    0.02758, 0.00978, 0.02360, 0.00150, 0.01974,  # u, v, w, x, y
    0.00074                                         # z
]

def frequency_analysis(group):
    best_shift = 0
    best_score = -float('inf')  # Higher dot product = better match
    
    for shift in range(26):
        freq = [0] * 26
        for c in group:
            decrypted = (ord(c) - ord('a') - shift) % 26
            freq[decrypted] += 1
        
        # Normalize frequencies to [0, 1]
        total = len(group)
        if total == 0:
            continue
        observed = [f / total for f in freq]
        
        # Compute dot product with English frequencies
        dot_product = sum(obs * eng for obs, eng in zip(observed, english_freq))
        
        if dot_product > best_score:
            best_score = dot_product
            best_shift = shift
    
    return chr(best_shift + ord('a'))

def find_key(ciphertext, key_len):
    key = []
    for i in range(key_len):
        group = ciphertext[i::key_len]
        key.append(frequency_analysis(group))
    return ''.join(key)

# Example usage:
key_len = 8  # From Kasiski/IC results
print("Frequency Analysis")
print("Possible key:", find_key(ciphertext, key_len))
print()
