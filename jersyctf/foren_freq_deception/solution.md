# Frequency Deception

The audio file clearly has DTMF tones. The tones are approx every 0.12 seconds apart
I used this https://dtmf.netlify.app/ site with threshold 0.04.
This is 0's and 1's with space in between. So I group them in group of 3 chars

```
bits = [chr(int(dtmf[i:i+3])) for i in range(0,942,3)]
# bits = [chr(int(i)) for i in bits.split(' ')]
asci = [int(i, 2) for i in ''.join(bits).split(' ')]

print("FLAG: ", ''.join(chr(i) for i in asci))
```

## Flag
`dOnT_C0me_$tAY_aW@Y_Fr0M_th!s_Pl@cE` (wrapped in jctfv)


