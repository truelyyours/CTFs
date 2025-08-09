# Marks the Spot

Give: ```3D*=H1,:U?.l&je6W$Z;1,:U?.l&je6V:H?1,:U?.l&je6V&t)1,:U?.l&je6V(<U=>Eu6.p+P66V'461,:U?.l&je6W$?41,:U?.l&j```

Given string is Acii-85 which is decoded to PLUS codes. When you enter the codes to `https://plus.codes/<code>` and consider the lat, long in that order and all the values correspond to ASCII chars.
Decoded plus codes: ```9JVM2222+22\nCQP52222+22\nCJX82222+22\nCH2J2222+22\nCHXPX2X2+X2\nCH9P2222+22\nCQG72222+22```.

9JVM2222+22 -> 97,73
CQP52222+22 -> 84, 123
CJX82222+22 -> 89, 66
CH2J2222+22 -> 70, 52
CHXPX2X2+X2 -> 90, 54
CH9P2222+22 -> 77, 54
CQG72222+22 -> 80, 125

i.e. `''.join(chr(i) for i in [97,73,84, 123, 89, 66, 70, 52, 89, 54, 77, 54, 80,125])`

## Flag
CIT{YBF4Y6M6P}