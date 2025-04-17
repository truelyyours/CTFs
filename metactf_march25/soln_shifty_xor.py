def recover_input(hex_output):
    # Convert hex to bytes
    try:
        xor_result = bytes.fromhex(hex_output)
    except ValueError:
        return "Invalid hex string"
    
    n = len(xor_result)
    if n == 0:
        return "Empty input"
    
    # Check if total XOR is zero
    total_xor = 0
    for b in xor_result:
        total_xor ^= b
    if total_xor != 0:
        return "No solution possible (XOR checksum failed)"
    
    # Compute cumulative XORs for positions 1 to n-1
    cumulative = [0] * n
    current = 0
    for i in range(1, n):
        current ^= xor_result[i]
        cumulative[i] = current
    
    # Try all possible s0 values (prioritizing printable ASCII)
    solutions = []
    for s0 in range(32, 127):  # Check printable ASCII first
        s = [s0]
        valid = True
        for i in range(1, n):
            si = s0 ^ cumulative[i]
            if si < 32 or si > 126:  # Check if printable
                valid = False
                break
            s.append(si)
        if valid:
            try:
                text = bytes(s).decode('ascii')
                solutions.append(text)
            except UnicodeDecodeError:
                continue
    
    # If no printable solutions, check all possible bytes
    if not solutions:
        for s0 in range(256):
            s = [s0]
            for i in range(1, n):
                si = s0 ^ cumulative[i]
                s.append(si)
            solutions.append(bytes(s).decode('latin-1'))
    
    return solutions

# Example usage:
hex_output = "686950021716160b1a54541b4f59161a590c41414d0c0f1759541b4f4f010b490c4f010b455716185946131b0d171d06014f016969530607174548071f1545541c0915544e014f4f010b45460f0e12071716534f1a0154414157161859541b4f421017040a4b491d580c4207060214061645541c09155457181a1908444207454b02070a444f094641161c1c1613164a0e743c0d45460a0d064749074e4302121645531c02080a010b4543020f4e491a536d2811152217123d0f03476f28434d2639131b0d1745015e31325d42416c335d5a586c365e4a510c42170154490f4659161a52551745521704050d070947541c011a5f0c696947121016005359161a55410d1e1704051d5942101d040e45491d5a00000e7732091c5c0c696e4b004c4a1f0607544b0e001550420709050c131f07094759161a55480917130b495355"  # Replace with your hex string
print(recover_input(hex_output), sep='\n')
# "I present to you, a many to one, one way function! I sure hope that no one figures out a way to break it, because that would be kind of awkward. The flag in case someone can is MetaCTF{tw0_w4y_funct10n_m0r3_l1k3_i7}, but if you're reading this, I guess you already broke it... Welp, I'll just keep believing you haven't!"