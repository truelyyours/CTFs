xr101 = bytes.fromhex('434542034a46505a4c516a6a5e496b5b025b5f6a46760a0c420342506846085b6a035f084b616c5f66685f616b535a035f6641035f6b7b5d765348')
# squ1rrel{}
key = '0472845678953' # total 13, 9 + 4 missing
# assert len(key) == 13
nums = '0123456789'
alphanum = 'ABCDEFGHIJKLMNOPQRSTUVWXYZqwertyuiopasdfghjklzxcvbnm_1234567890{}'

dec = ''
poss = {}
for i in range(len(xr101)):
    if (i % 13) in range(0):
        poss[i] = []
        for n in nums:
            if chr(ord(n) ^ xr101[i]) in alphanum:
                poss[i].append((chr(ord(n) ^ xr101[i]), n))
        dec += "*"
    else:
        dec += chr(ord(key[i%13]) ^ xr101[i])

for i,v in poss.items():
    print(i, " :: ", v)

print("DEC: ", dec)
