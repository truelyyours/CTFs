# MOVeit
During a covert mission on a Covenant-controlled world, Spartan Palmer intercepts an encrypted communication between Covenant leaders. Can you help her decrypt the message?

## Looking at the Sauce! 
It is a simple ECDH. It uses custom curve so there will potentially be a vulnerability. And a quick look at the title of challenge, it a MOV attack. This is a well known attack on ECDH where we can reduce the ECDLP problem to a DLP problem when $k$ is small enough.
Checking that $E$ is supersingular tells us that the embedding degree $k$ (smallest $k$ such that the order of $E$ divides $(p^k - 1)$ is small $(k \leq 6)$. And computing it explicitly tells us that is $2$.

The MOV attack works by using the [Weil pairing](https://en.wikipedia.org/wiki/Weil_pairing) to translate solving the dlog in the elliptic curve group to solving it in the multiplicative group $\mu_m$ (group of$m$-th group of unity), where sub-exponential algorithms exist.

## Let's code!
There are quite a lot of code available online itself. Or you can just "vibe code" it. In our case we want to find $n_a$ and $n_b$ for Alice and Bob respectively. These are essentially the "private" keys that ensures that you cannot decrypt the message as you would never know the common key $S$ ($S1$ and $S2$ in the challenge code).
So, I define a helper function `movAttack` which takes the generator $G$ and point $P$ where $P = n * G$ and return the value of $n$.
```python
def movAttack(G, P):
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
    # print("B order:", B.order())
    # print("G order:", G.order())
    assert G.order() == B.order()

    Ge = Ee(G)
    Pe = Ee(P)

    n = G.order()
    alpha = Ge.weil_pairing(B, n)
    beta = Pe.weil_pairing(B, n)

    print('Computing log...')
    nP = beta.log(alpha)
    return nP
```
So, using this we find the private keys using which we get the common key (or point to be precise). Also, I check for the correctness by ensuring that the shared key is in fact same!
```python
Alice_n = movAttack(G, Alice_point)
Bob_n = movAttack(G, Bob_point)

# Verifying the eventual equality of shared key
S1 = (Alice_point*Bob_n).xy()[0]
S2 = (Bob_point*Alice_n).xy()[0]
assert S1 == S2
```

## Capture the Flag!
Knowing the shared key (point) we can simply decrypt the encrypted flag using AES and get the final flag!
```python
cipher = AES.new(str(S1).encode()[:16], AES.MODE_ECB)
flag = cipher.decrypt(bytes.fromhex(enc_flag)).hex()

print("Decrypted Flag: ", unpad(bytes.fromhex(flag), AES.block_size))
```

Voila:
`flag{14d62aab-c804-4a29-9e09-431c9e615676}`

