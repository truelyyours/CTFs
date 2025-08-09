import base64, json

cip = 'TFJDe0gzeV9ldmlfdzMzX0FYQ0M2V19Wa1hidldINDYxTXR1YlgyOXZnYn0='

cip_64 = base64.b64decode(cip)
# cip_32 = base64.b85decode(cip)
print("BASE64 decode: " , cip_64)
# print("BASE32 decode: " , cip_32)
chars = '01234a67895bcdefghijklrnopqmsTuvwxyzABCDXFGHIJKLMNOPQRStUVWEYZ'
def rot_all_ciphers(text):
    """Generate all possible ROT cipher transformations (ROT-1 to ROT-25)"""
    results = {}
    last = []
    for rot in range(0, 26):
        transformed = []
        for char in text:
            if char.isupper():
                transformed.append(chr((ord(char) - 65 + rot) % 26 + 65))
            elif char.islower():
                transformed.append(chr((ord(char) - 97 + rot + 5) % 26 + 97))
            elif char.isdigit():
                transformed.append(chr((ord(char) - 48 + rot) % 10 + 48))
            else:
                transformed.append(char)
            # ind = chars.find(char)
            # if ind != -1:
            #     transformed.append(chars[(ind + rot)%len(chars)])
            # else:
            #     transformed.append(char)
        last.append(''.join(transformed).split('_')[-1][:-1])
        results[f'ROT-{rot}'] = ''.join(transformed)
    print(['CIT{H3y_are_w33_ROTT3N_' + str(base64.b64decode(i)) + '}' for i in last])
    
    return results

print(json.dumps(rot_all_ciphers(cip_64.decode()), indent=4))
# print(json.dumps(rot_all_ciphers("PVG{LxxdJwAXJGcsDoncKfRctddA}"), indent=4))
# print(json.dumps(rot_all_ciphers("TFJDe0gzeV9ldmlfdzMzX0FYQ0M2V19Wa1hidldINDYxTXR1YlgyOXZnYn0="), indent=4))
#     "ROT-53": "CIt{yUp_5m9_nUU_rOttXN_MbO2mNyVXSDkl2OT0m72}",
# PVG{LxxdJwAXJGcsDoncKfRctddA}
# CIT{H3y_are_w33_ROTT6N_VkXbvWH461MtubX29vgb}
