from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

data = b"hello world!"
print('data', data)
key = get_random_bytes(32)
print('key', key)
cipher = AES.new(key, AES.MODE_EAX)
print('cipher:', cipher)
ciphertext, tag = cipher.encrypt_and_digest(data)
print('ciphertext/tag',  ciphertext)
encoded = [ x for x in (cipher.nonce, tag, ciphertext) ]

nonce, tag, ciphertext = encoded

cipher = AES.new(key, AES.MODE_EAX, nonce)
print(cipher)
data = cipher.decrypt_and_verify(ciphertext, tag)
print(data)