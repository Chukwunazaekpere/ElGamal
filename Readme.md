# Introduction

This is the ElGamal crypto-system inplementation for my masters at the University of Europe for Applied Scineces, in Germany. The code is splitted into three units, in order ro properly simulate the expected real-world scenario of the ElGamal encryption and decryption concepts. 
The various units are the required algorithm for the following

# Algorithms

1. Key Generation
   - Large prime
   - Primitive roots
   - Public key generation
2. Encryption
   - Secret key generation
   - Encoding
   - Character encryption
3. Decryprion
   - Scret key discovery
   - Decoding 
   - Unicode decryption 

# Testing Steps
Run the `python3 app.py` which will trigger the following steps
1. Creates public key, which will be generated and stored under files in `files/public_keys.txt`
2. Plain message will be encrypted from the file location in which exists and and encrypted message will be generated under files in `files/encrypted_message.txt`
3. Decryption will be run, with the final result generated under files in `files/decrypted_message.txt`
