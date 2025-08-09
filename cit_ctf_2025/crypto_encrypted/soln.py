ff = open('encrypted', 'rb').read().strip()

nulls = ff.count(b'\x00')

PNG = bytes.fromhex('89504E470D0A1A0A')
print(ff[:8])
print([i^j for i ,j in zip(PNG, ff[:8])])

print(nulls)
x = 10
print("Start {x}:: ", list(ff[:x]))