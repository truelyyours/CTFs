# Baby RSA 2
If all I have to do is keep my factors p and q secret, then I can save computation time by sharing the same modulus between all my friends. I'll give them unique e and d pairs to encrypt and decrypt messages. Sounds secure to me!

## Solution

Here both `(e_priv, d_priv)` and `(e_pub, d_pub)` are modular inverse of each other `mod phi`. I.e.
```
e_priv * d_priv - 1 ≡ 0 mod φ(N)
e_pub  * d_pub  - 1 ≡ 0 mod φ(N)
```
Since `e_pub` is a 16-bit prime, and `d_pub` is given, `d_pub * e_pub - 1` is a multiple of `phi`. Given that `phi` is very large (around the same size as `N`), and `e_pub` is small, d_pub * e_pub - 1 is likely to be k * phi for some **small integer** `k`.

So we can brute force 10000 k's and check if we can find a falid phi and hence find valid `p` and `q`.
```
for k in range(1, 10000):
    if k_phi % k != 0:
        continue
    phi_candidate = k_phi // k

    sum_pq = N + 1 - phi_candidate
    diff_pq_squared = sum_pq**2 - 4 * N

    if diff_pq_squared < 0:
        continue

    diff_pq = math.isqrt(diff_pq_squared)
    if diff_pq * diff_pq != diff_pq_squared:
        continue # not a square!
    
    # print("SUM and diff: ", sum_pq, diff_pq_squared)
    p = (sum_pq + diff_pq) // 2
    q = (sum_pq - diff_pq) // 2
    # print("SOME p and q: ", p, q)

    if p * q == N:
        # Found valid p and q
        print("Found valid p and q")
        phi = phi_candidate
        d_priv = inverse(e_priv, phi)

        m = pow(c, d_priv, N)
        flag = long_to_bytes(m)
        print("Flag is: ", flag.decode())
        break
```

## Flag
DawgCTF{kn0w1ng_d_1s_kn0w1ng_f4ct0rs}