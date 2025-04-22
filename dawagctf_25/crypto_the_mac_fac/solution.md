# The MAC FAC

Check out my new MAC generator! I know you are supposed to use random and secret IVs in CBC-AES mode, so I decided to improve upon standard MACs by implementing that. Good luck trying to forge any messages now!

nc connect.umbccd.net 27811

## Solution

The log entries have simple xor with hidden key. So you send a 16bytes NULL IV. The log entry will have the IV as the xor_key. You can use this to recover the admin's passphrase and IV as follows:

```code[python]
xor_key_recovered = bytes.fromhex(iv_xored_hex)
admin_passphrase = unpad(xor(bytes.fromhex(admin_msg_hex), xor_key_recovered), 16)
print("Admin message: ", admin_passphrase)

# print("Admin IV: ", admin_iv_hex, len(admin_iv_hex))
admin_iv_bytes = xor(bytes.fromhex(admin_iv_hex), xor_key_recovered)
```

Then, for "tag", we know that only the last 16 bytes are used. So we ill perform CBC-MAC forgery attack.
We know the (`admin_phrase`, `admin_iv`) and the resulting `admin_tag`, so we can forge a message and IV that will produce the same tag. This is because the first block in CBC is affected by the IV XORed with the first plaintext block.
We can forge the new IV as:
`IV' = IV ^ P1 ^ P1'`.

This will ensure that the C1' is same as C1 as if the original admin passphasre is assed because, `C1' = AES(P1' ^ IV') = AES(P1' ^ (IV ^ P1 ^ P1')) = AES(P1 ^ IV) = C1`

However, note that your message's length should eb same as admin's passphrases'. A simple way to achieve this is replace the 1st 16 bytes of admins' passphrase with NULL bytes and the new IV will be the xor of admin's IV and first 16 bytes of admin's passphrase.
This combination passes the check that:
`if msg != admin_phrase and tag == admin_tag`

```
custom_msg = b'\x00'*16 + admin_passphrase[16:]
custom_msg_pad = pad(custom_msg, 16)
admin_msg_pad = pad(admin_passphrase, 16)
assert(len(custom_msg_pad) == len(admin_msg_pad))
new_iv = strxor(admin_iv_bytes, admin_msg_pad[:16])
```

## FLAG:
You will get the flag as:
`DawgCTF{m0r3_r4nd0mne55_15_n0t_4lw4y5_m0r3_53cur3}`

