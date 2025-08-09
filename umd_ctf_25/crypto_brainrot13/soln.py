from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
import codecs
from sympy import symbols, Poly, gcd
# import re

n = 96685821958083526684938680238271304286887980859392922334047044570819254535637534763165507014186569373580269436562287115575895071477094697751185058766474544708343165263644182297048851208627306861544906558700694910255483830223450427540731613986917757415247541102253686241820221043700623282515147528145504812161

ct1 = 31415617614942980419493801728329478459882170524654275330189702271291172239569974917796230082992620119324013322311500280165046115132115888952730272833129650105740565501270236988682510607126061981801996717672566496111413558704046446132351270004211376270714769910968931266620926532143617027921568831958784579911
ct2 = 72563774621694978528581466712845934115989091233025298416607646944054938010207983336599181951465053976617135146411342652500844040957885351294246597514830545442455636203961703603515841401653220929094734409672423770927867923227749902813163411103868690480354808090999202815188200468063383568781761012284874177390
e = 3

x = symbols('x')

# Step 1: Make symbolic polynomials
# m2 = f(m1) = ROT13(m1) (in bytes), so let’s build that as a symbolic function
# Let m = x, and define f(x) as ROT13 applied on bytes
# We'll simulate ROT13 on each byte and treat it as known

# First, try to guess a flag that will help us simulate ROT13
# Since length is 28 and format is UMDCTF{...}, we know the first 7 chars

def build_rot13_bytes(b: bytes):
    return codecs.encode(b.decode(), 'rot13').encode()

def pad(msg: bytes) -> bytes:
    while len(msg) < 120:
        msg += b'OAEP'
    return msg

# We’ll try this with a dummy flag to create structure
dummy_flag = b'UMDCTF{aaaaaaaaaaaaaaaaaaaa}'  # 28 bytes
m1_bytes = pad(dummy_flag)
m2_bytes = build_rot13_bytes(m1_bytes)

# Now build m1 = x, and m2 = known function of x
# That is, m2 = ROT13(m1) = m1 + delta  (byte-wise difference known)
delta = bytes(a ^ b for a, b in zip(m1_bytes, m2_bytes))

# Interpret delta as integer constant
delta_int = bytes_to_long(delta)

# So m2 = m1 ^ delta  ⇒ m2 = m1 + delta (since ROT13 is simple XOR in ascii range)
# Then:
#   ct1 = m1^e mod n
#   ct2 = (m1 + delta)^e mod n

# Define polynomials:
P = Poly(x**e - ct1, x, modulus=n)
Q = Poly((x + delta_int)**e - ct2, x, modulus=n)

# Step 2: Compute GCD of the two polynomials
G = gcd(P, Q)

# Step 3: Extract root
if G.degree() == 1:
    m1_root = -G.all_coeffs()[0] % n
    recovered = long_to_bytes(m1_root)
    print("[+] Recovered plaintext:")
    print(recovered)
else:
    print("[-] Failed to extract root. GCD degree:", G.degree())


