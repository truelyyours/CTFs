# SummitCTF{N0T_3z_C43s3r_C1ph3r_!@#&&$@(#}

def decrypt_transposition(ciphertext, rows, cols):
    # Split ciphertext into a grid
    grid = [ciphertext[i:i+cols] for i in range(0, len(ciphertext), cols)]

    # Read columns in order to reconstruct plaintext
    plaintext = ''.join([''.join(row[i] for row in grid if i < len(row)) for i in range(cols)])
    return plaintext

cipthertext = 'FgAmf1_&}·hP0_3c!$··zGGPeu@@··zS_4_3#(··v{33Pe&#··'

# Just a gues based on prev et et challenge that it will bt 5x10 for 50 chars
cc_temp = decrypt_transposition(ciphertext, 5, 10)

# Simple ceaser decrypt of cc_temp = FhzzvgPGS{A0G_3m_P43f3e_P1cu3e_!@#&&$@(#}
