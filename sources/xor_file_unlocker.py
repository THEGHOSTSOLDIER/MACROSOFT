# decrypt a xor encrypted file with a key in a binary file
#
# usage: python3 xor_file_unlocker.py <key_file> <file_to_decrypt>
#
# example: python3 xor_file_unlocker.py key.bin secret.bin

import sys

# check the number of arguments
if len(sys.argv) != 3:
    print("usage: python3 xor_file_unlocker.py <key_file> <file_to_decrypt>")
    sys.exit(1)

# get the key and file to decrypt
key_file = sys.argv[1]
file_to_decrypt = sys.argv[2]

# read the key file
with open(key_file, "rb") as f:
    key = f.read()

# read the file to decrypt
with open(file_to_decrypt, "rb") as f:
    cipher = f.read()

# decrypt the file
plain = bytes([a ^ b for a,b in zip(cipher, key)])

# write the decrypted file
with open(file_to_decrypt, "wb") as f:
    f.write(plain)

# print a message
print(f"File {file_to_decrypt} decrypted with key {key_file}")

# end of script