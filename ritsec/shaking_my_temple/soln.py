def verify_key(key: str) -> bool:
    if len(key) != 32 or not key.isalnum():
        return False
    
    try:
        # Condition 1: Positions 1-4
        if (ord(key[0]) ^ ord(key[1])) + (ord(key[2]) * ord(key[3])) != 232:
            print("Condition 1 failed")
            return False

        # Condition 2: Positions 5-7
        if (pow(ord(key[4]), 2) + pow(ord(key[5], 2))) % 256 != ord(key[6]):
            return False

        # Condition 3: Positions 8-11
        sum_product = ord(key[7]) + ord(key[8]) * ord(key[9])
        remainder = (5 * ord(key[10]) + 10) % 100
        if sum_product != remainder:
            return False

        # Condition 4: Positions 12-15
        if (ord(key[11]) ^ ord(key[12])) + ord(key[13]) * ord(key[14]) != 200:
            return False

        # Condition 5: Positions 17-20
        sum_mod = (ord(key[16]) + ord(key[17])) % 37
        product_mod = (ord(key[18]) * ord(key[19])) % 90
        if sum_mod != product_mod:
            return False

        # Condition 6: Positions 21-22
        if pow(ord(key[20]), 2) + pow(ord(key[21]), 2) != 250:
            return False

        # Condition 7: Positions 23-25
        xor_part = ord(key[22]) + (2 * ord(key[23]))
        remainder_part = ord(key[24]) % 10
        if xor_part ^ remainder_part != 30:
            return False

        # Condition 8: Positions 26-28
        if ord(key[25]) * ord(key[26]) != (ord(key[27]) ^ 20):
            return False

        # Condition 9: Positions 29-32
        sum_part = ord(key[28]) + ord(key[29])
        diff_part = ord(key[30]) - ord(key[31])
        if (sum_part ^ diff_part) != 15:
            return False

    except IndexError:
        return False

    return True

# Example usage with the sample key from previous answer
sample_key = "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"
sample_key = "A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"
print(f"Verification result: {verify_key(sample_key)}")
