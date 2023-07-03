import os
import binascii

 # Generating a random secret key of 24 bytes, converting it to hexadecimal representation, and decoding it to a string
secret_key = binascii.hexlify(os.urandom(24)).decode()

#Print it!
print(secret_key)  # Printing the secret key to the console

