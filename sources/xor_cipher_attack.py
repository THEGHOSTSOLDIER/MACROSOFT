import sys

# known-plaintext attack on xor encryption
def xor_kpa(cipher:bytes, plain:bytes)->bytes:
    # get the key with known-plaintext attack
    # cipher and plain must have the same length

    # create couple from cipher and plain.
    match = zip(cipher, plain)
    # XOR cipher and plain
    tmp = [a ^ b for a,b in match]
    # return the key
    return bytes(tmp)

# open two files as binary from arguments
with open(sys.argv[1], "rb") as f1, open(sys.argv[2], "rb") as f2:
    # read the files
    cipher = f1.read()
    plain = f2.read()

    # get the key
    key = xor_kpa(cipher, plain)

    # print the key
    print(key)

    #save the key into a binary file
    with open("key.bin", "wb") as f:
        f.write(key)

# end of script