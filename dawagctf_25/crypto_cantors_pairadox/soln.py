# import math
from sage.all import sqrt, floor

flag = 4036872197130975885183239290191447112180924008343518098638033545535893348884348262766810360707383741794721392226291497314826201270847784737584016

def getTriNumber(n):
    return n * (n + 1) // 2  # Ensure integer division

def pair(n1, n2):
    S = n1 + n2
    return getTriNumber(S) + n2

def pair_array(arr):
    result = []
    for i in range(0, len(arr), 2):
        result.append(pair(arr[i], arr[i + 1]))    
    return result

def pad_to_power_of_two(arr):
    result = arr
    n = len(result)
    while (n & (n - 1)) != 0:
        result.append(0)
        n += 1
    return result
    
def unpair(z):
    w = floor((sqrt(8*z + 1) - 1) / 2)
    t = (w*(w + 1)) //2
    y = z - t
    x = w- y
    return (x, y)

def unpair_array(arr):
    result = []
    for z in arr:
        x, y = unpair(z)
        result.extend([x, y])
    return result
# unpair for 6 rounds
arr = [flag]
for _ in range(6):
    arr = unpair_array(arr)

print(''.join(chr(c) if 32 <= c < 127 else '.' for c in arr))