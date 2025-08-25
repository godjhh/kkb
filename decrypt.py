from Crypto.Cipher import AES
aes_key  = "133a985d25765d4af3c84fcb1f8296f888d5d8fa028697e186939dbaf283108e"
cipher_hex = (
    "11 D1 66 5C FA B6 FE 29 58 9E 8E 01 E8 6E BD 91 59 76 41 10 E3 90 11 0D A1 72 9F 84 C0 06 C8 1B 36 5F C6 42 73 6A 91 77 93 5A 02 63 CA 7B B3 EF A1 C3"
)
key  = bytes.fromhex(aes_key)
cipher_bytes = bytes.fromhex(cipher_hex)

nonce, rest = cipher_bytes[:12], cipher_bytes[12:]
cipher_text, tag     = rest[:-16], rest[-16:]

pt = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=16).decrypt_and_verify(cipher_text, tag)
print(pt.decode()) 