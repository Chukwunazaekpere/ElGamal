"""
Author: Chukwunazaekpere Emmanuel Obioma
Written for: Group 3
Nationality: Biafran
Email-1: chukwunazaekpere.obioma@ue-germany.de 
Email-2: ceo.naza.tech@gmail.com
************************************************
Course: Software Optimisation
Written: June 15th 2024
Due: June 30th 2024
========================== Major Problem ==========================
A major problem here, is finding the primitive root of the computed prime.
A primitive root m, of a prime number z, is one, such that:
m mod z, m^2 mod z, m^3 mod z ... ... m^(z-1) mod z, gives numbers that are unique 
"""


import random
from datetime import datetime
import math
import logging
logger = logging.getLogger(__name__)
log_date = datetime.now()
logging.basicConfig(level=logging.INFO)

class ElGamalPublicKeyGen:
    def __init__(self, private_key: int):
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"

    def _file_writer(self, file_name:str, file_mode="a+", content=""):
        """Read file containing message to be encrypted or decrypted"""
        if file_mode == "w":
            with open(file_name, "w")as file_handle:
                file_handle.write(content)
        else:
            with open(file_name, "+a")as file_handle:
                file_handle.write(content)

    def _generate_large_prime(self):
        count = 2
        rand = random.getrandbits(25)
        while count <= 10:
            if rand % count == 0:
                rand+=1
                count = 1
            count+=1
        logging.info(msg=f"\n\t Large prime, was successfully generated...")
        return rand
    

    def _generate_primitive_root(self):
        large_prime = self._generate_large_prime()
        self._file_writer(file_name=self.public_key_file_name, content=f"\n\t Large Prime:\n {large_prime}")
        power = 1
        index = 1
        primitive_root_list = []
        primitive_root = 0
        stop_iteration = False
        while index < large_prime:
            while power <= large_prime-1:
                try:
                    index_pow = math.pow(index, power)
                    factor = int(index_pow) % large_prime
                    if factor not in primitive_root_list:
                        primitive_root_list.append(factor)
                    else:
                        primitive_root_list = []
                        power = 1
                        break
                    power+=1
                except OverflowError:
                    stop_iteration = True
                    break
            if stop_iteration or len(primitive_root_list) == large_prime-1:
                primitive_root = index
                break # rather than finding all the primitive roots for the given prime, we take the first value that satisfies the condition of a primitive root
            index+=1
        self._file_writer(file_name=self.public_key_file_name, content=f"\n\t Primitive Root:\n {primitive_root}")
        logging.info(msg=f"\n\t Primitive root: {primitive_root}, was found...")
        return large_prime, int(primitive_root)


    def generate_public_key(self):
        self._file_writer(file_mode="w", file_name=self.public_key_file_name, content="")
        large_prime, primitive_root = self._generate_primitive_root()
        primitive_power = math.pow(primitive_root, self.private_key)
        public_key = int(primitive_power) % large_prime 
        self._file_writer(file_name=self.public_key_file_name, content=f"\n\t Generator Public Key:\n {str(public_key)}")
        logging.info(msg=f"\n\t Public key: {public_key}, was successfully generated...")
        return public_key


private_key = 7
elgamal = ElGamalPublicKeyGen(private_key=private_key)
public_key = elgamal.generate_public_key()
