from sage.all import EllipticCurve, GF, ZZ
import random
from math import gcd
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


p = 14537114296651069957
a = -30
b = 56
E = EllipticCurve(GF(p), [a,b])

# Finding k for MOV attack
def movAttack(G, Q):
    k = 1
    while (p**k - 1) % E.order():
        k += 1

    Ee = EllipticCurve(GF(p**k, 'y'), [a, b])

    R = Ee.random_point()
    m = R.order()
    d = gcd(m, G.order())
    B = (m // d) * R

    assert G.order() / B.order() in ZZ
    # If below give Assertion Error, just re run the script!
    print("B order:", B.order())
    print("G order:", G.order())
    assert G.order() == B.order()

    Ge = Ee(G)
    Qe = Ee(Q)

    n = G.order()
    alpha = Ge.weil_pairing(B, n)
    beta = Qe.weil_pairing(B, n)

    print('Computing log...')
    nQ = beta.log(alpha)
    return nQ

# Generator: (12060282013991235054 : 8742152935278645013 : 1)
# Alice Public key: (9425743319987468555 : 3179626149587149192 : 1)
# Bob Public key: (11922449306804274285 : 10464671187496881937 : 1)
enc_flag = "25dee22ea0a045ee91a2985baa52059917569614b4a5bf2d4cea88328fe73ded7c14c037256a627373dace9411a49090"

Gx = 12060282013991235054
Gy = 8742152935278645013
G = E(Gx, Gy)

Alice_x = 9425743319987468555
Alice_y = 3179626149587149192
Alice_point = E(Alice_x, Alice_y)

Bob_x = 11922449306804274285
Bob_y = 10464671187496881937
Bob_point = E(Bob_x, Bob_y)

Alice_n = movAttack(G, Alice_point)
Bob_n = movAttack(G, Bob_point)
print("Alice n:", Alice_n)
print("Bob n:", Bob_n)

# Verifying the eventual equality of shared key
S1 = (Alice_point*Bob_n).xy()[0]
S2 = (Bob_point*Alice_n).xy()[0]
assert S1 == S2


cipher = AES.new(str(S1).encode()[:16], AES.MODE_ECB)
flag = cipher.decrypt(bytes.fromhex(enc_flag)).hex()

print("Decrypted Flag: ", unpad(bytes.fromhex(flag), AES.block_size))