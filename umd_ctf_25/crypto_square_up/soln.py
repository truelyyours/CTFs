
from sage.all import *

N = 1298690852855676717877172430649235439701166577296380685015744142960768447038281361897617173145966407353660262643273693068083328108519398663073368426744653753236312330497119252304579628565448615356293308415969827357877088267274695333
lp = 1
lq = -1
c = 162345251908758036296170413099695514860545515965805244415511843227313118622229046299657295062100889503276740904118647336251473821440423216697485906153356736210597508871299190718706584361947325513349221296586217139380060755033205077

# Step 1: Compute the Jacobi symbol condition (m | N) = lp * lq = -1
def find_m():
    # Brute-force small candidates (works if m is small)
    for m in range(1, 2^20):
        if pow(m, 2, N) == c % N:
            if jacobi_symbol(m, N) == lp * lq:
                return m
    return None

# Step 2: If m is not small, use Coppersmith (if prefix is known)
def coppersmith_attack():
    P= PolynomialRing(Zmod(N), names='x')
    x = P.gen()
    known_prefix = b"UMDCTF{"
    known_part = int.from_bytes(known_prefix, 'big')
    k = (N.bit_length() // 8 - len(known_prefix)) * 8  # Unknown bits
    f = (known_part * 2**k + x)**2 - c
    roots = f.small_roots(X=2**k, beta=0.5)
    if roots:
        m = known_part * 2**k + roots[0]
        if jacobi_symbol(m, N) == lp * lq:
            return m
    return None

m = coppersmith_attack()
if m:
    print("Recovered m:", m)
    print("Flag:", m.to_bytes((m.bit_length() + 7) // 8, 'big'))
else:
    print("Failed to recover m.")