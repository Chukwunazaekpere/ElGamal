


import random
import math
class DecryptionAlgorithm:
    def __init__(self, private_key: int):
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"

    def _file_writer(self, file_name:str, content=""):
        """Read file containing message to be encrypted or decrypted"""
        with open(file_name, "+a")as file_handle:
            file_handle.write(content)

    def _generate_large_prime(self):
        count = 2
        rand = random.getrandbits(40)
        while count <= 10:
            if rand % count == 0:
                rand = random.getrandbits(40)
                count = 2
            count+=1
        return rand
    
    def _generate_primitive_root(self):
        large_prime = self._generate_large_prime()
        stringified_prime = str(large_prime)
        self._file_writer(self.public_key_file_name, "\n\t Generated Prime: \n")
        self._file_writer(self.public_key_file_name, stringified_prime)
        large_prime_len = len(stringified_prime)
        primitive_root = stringified_prime[0:large_prime_len//2]
        self._file_writer(self.public_key_file_name, "\n\t Primitive Root: \n")
        self._file_writer(self.public_key_file_name, primitive_root)
        return large_prime, int(primitive_root)


    def generate_public_key(self):
        large_prime, primitive_root = self._generate_primitive_root()
        primitive_power = math.pow(primitive_root, self.private_key)
        public_key = primitive_power % large_prime 
        self._file_writer(self.public_key_file_name, "\n\t Public Key: \n")
        self._file_writer(self.public_key_file_name, str(public_key))
        return public_key

ff = PublicKeyGen(50)
# gf = ff.generate_large_prime()
public_key = ff.generate_public_key()
# print("\n\t GF: ", gf, len(str(gf)))
print("\n\t public_key: ",public_key, len(str(public_key)))
