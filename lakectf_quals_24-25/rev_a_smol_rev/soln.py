import base64

b64 = open('chal', 'r').read()
b64.strip()
bytes = base64.b64decode(b64)
print(len(bytes), bytes[:4])

open('chalbin', 'wb').write(bytes)