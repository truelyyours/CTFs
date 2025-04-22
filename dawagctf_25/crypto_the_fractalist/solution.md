# The Fractalist
Math and science are powerful tools, but imagination might be the key to success.

## Solution
Quick google search shows that "The Fractalist" is the memoir of Mathematician Benoit Mandelbrot who pioneered fractal geometry. 
Then, asking gpt about more information, I found about checking for mandelbrot Membership which is specifically for mandelbrot's factor. With suffeciently larg iteration (1000 is what i used), you can convert each of the point to a char when it escapes and it will give you the flag.
```
def mandelbrot(c, max_iter=1000):
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return -1  # flag as inside set

decoded = ""
for pt in nos:
    count = mandelbrot(pt)
    if 32 <= count <= 126:
        decoded += chr(count)
    else:
        decoded += '.'  # or skip
print(decoded)
```

## Flag
DawgCTF{BeN01tWh0Co1N3dFr@CtaLs}