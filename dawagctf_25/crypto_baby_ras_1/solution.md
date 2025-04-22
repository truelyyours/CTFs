# Baby RSA 1
You think your Algebra skills are pretty good huh? Well let's test it out.

## Solution
Given is simple system of linea equations. Write them as matrix and you can solve it.
`delta = a * d - b * c`
`p = (d * x - b * y) // delta`
`q = (-c * x + a * y) // delta`

And then you can get the flag as:
```
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
m = pow(ct, d, N)
plaintext = long_to_bytes(m)
```

## Flag
DawgCTF{wh0_s41d_m4th_15_us3l3ss?}