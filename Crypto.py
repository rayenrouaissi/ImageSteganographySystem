''' 
we need first to install the library 
   pycryptodome
'''
pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


def encrypt_message(message):
    key = get_random_bytes(16)  # Generate a random 128-bit key
    cipher = AES.new(key, AES.MODE_ECB)
    padded_message = pad(message.encode(), AES.block_size)
    ciphertext = cipher.encrypt(padded_message)
    return key, ciphertext



def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = cipher.decrypt(encrypted_message)
    # Unpad the decrypted message
    decrypted_message = unpad(decrypted_message, AES.block_size)
    return decrypted_message.decode()

# Example usage:
message = "Hello, world!"
key, encrypted_message = encrypt_message(message)
print("Key:", key)
print("Encrypted message:", encrypted_message)
decrypted_message = decrypt_message(encrypted_message, key)
print("Decrypted message:", decrypted_message)
