# Cantor's Pairadox
Now that I have encrypted my flag with a new math function I was just researching I can know share it with my friend Cantor and no one will know how to read it except us!

## Solution

As the name suggest, it is cantor's pairing and it is reversible. Google and find that it can be reversed as:
```
def unpair(z):
    w = floor((sqrt(8*z + 1) - 1) / 2)
    t = (w*(w + 1)) //2
    y = z - t
    x = w- y
    return (x, y)
```

We do this for each number in a array 6 times as follows:
```
def unpair_array(arr):
    result = []
    for z in arr:
        x, y = unpair(z)
        result.extend([x, y])
    return result
# unpair for 6 rounds
arr = [4036872197130975885183239290191447112180924008343518098638033545535893348884348262766810360707383741794721392226291497314826201270847784737584016]
for _ in range(6):
    arr = unpair_array(arr)
```

## Flag
Dawg{1_pr3f3r_4ppl3s_t0_pa1rs_4nyw2y5}