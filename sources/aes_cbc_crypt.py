import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def aes_cbc_encrypt(data:bytes, key:bytes, iv:bytes)->bytes:
    # encrypt data with AES CBC
    # data must be a multiple of 16 bytes
    # key must be 16, 24 or 32 bytes

    #Add padding to get 16 bytes multiple
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()

    #Return the initialization vector and the encrypted message
    return ct

def aes_cbc_decrypt(data:bytes, key:bytes, iv:bytes)->bytes:
    # decrypt data with AES CBC
    # data must be a multiple of 16 bytes
    # key must be 16, 24 or 32 bytes

    # decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(data) + decryptor.finalize()

    #Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    #Return the decrypted message
    return data.decode('utf-8')

def aes_cbc_file(filename:str, mode:int, key:bytes, iv:bytes)->bytes:
    # encrypt and decrypt file with AES CBC
    # file must be a multiple of 16 bytes
    # key must be 16, 24 or 32 bytes

    # load the file
    with open(filename, "rb") as f:
        data = f.read()

    # encrypt or decrypt the file
    if mode == 0:
        # encrypt the file
        encrypted = aes_cbc_encrypt(data, key, iv)
        # write the result on the same file
        with open(filename, "wb") as f:
            f.write(encrypted)

        return iv

    elif mode == 1:
        # decrypt the file
        decrypted = aes_cbc_decrypt(data, key, iv)
        # write the result on the same file
        with open(filename, "wb") as f:
            f.write(bytes(decrypted,'utf-8'))

# end of script