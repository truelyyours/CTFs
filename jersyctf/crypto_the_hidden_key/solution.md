# The Hidden Key

We are given `N`, `e` and list of ciphers. Each representing one encrypted character.
We start by factoring the `N` and find `p` and `q`: `p = 3769` and `q = 5351`.
$\phi(n)$ = `(p-1) * (q-1)`
$d = inverse_mod(e(=65537), \phi)$
`d` will be `687473`.
Then simply decrypt each message and get the flag:
dec = [pow(i,d,n) for i in ct]
''.join([long_to_bytes(i).decode() for i  in dec])

## Flag

jctfv{Pr1v@t3_k3y_f0r_1nF0rm@t10n}
