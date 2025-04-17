# SummitCTF{M3d1um_C43s3r_C1ph3r_l0l}

def decrypt_transposition(ciphertext, rows, cols):
    # Split ciphertext into a grid
    grid = [ciphertext[i:i+cols] for i in range(0, len(ciphertext), cols)]

    # Read columns in order to reconstruct plaintext
    plaintext = ''.join([''.join(row[i] for row in grid if i < len(row)) for i in range(cols)])
    return plaintext

# Ciphertext
ciphertext = "StMms1_uC3_3plmTdCrh0mF14_3li{u3Cr}"

# Known start of plaintext
known_start = "SummitCTF{"

# Try different grid sizes (rows and columns)
for rows in range(1, len(ciphertext)):
    cols = len(ciphertext) // rows
    if len(ciphertext) % rows == 0:  # Ensure perfect division
        decrypted = decrypt_transposition(ciphertext, rows, cols)
        if decrypted.startswith(known_start):
            print(f"Decrypted Text: {decrypted}")
            print("ROWS, COLS: ", rows, cols)
            break

