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
"""

from datetime import datetime
import math
from .base_class import BaseClass


class ElgamalDecryptionAlgorithm(BaseClass):
    def __init__(self, private_key: int):
        super().__init__()
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"
        self.encrypted_message_file = "./files/encrypted_message.txt"
        self.decrypted_message_file = "./files/decrypted_message.txt"
        self.secret_key = "" 
        self.secret_key_file_name = "./files/secret_key.txt" 
        self.encrypter_public_key = "" 
        self.large_prime = "" 
        self.decryption_dictionary = {} #dictionary where plain-character is key & encrypted character is the value. This is to reduce the extra time taken for excrypting plain characters that have been encrypted already


    def _get_modulo_inverse(self, inv_val:int, mod_val:int):
        """Get modulo inverse of val"""
        self.log_info(f"\n\t {datetime.now()} Generating modulo inverse")
        count = 2
        while count < mod_val:
            val = inv_val*count % mod_val
            if val == 1:
                modulo_inverse = count
                return modulo_inverse
            count+=1
        return 1
    
    def _secret_key_generator(self):
        """Geenerates the secret key that was used during encryption"""
        self.log_info("\n\t ElGamalEncryptionAlgorithm is generating the secret key used in encryption...")
        public_key_content = self._file_helper(file_mode="rl",file_name=self.public_key_file_name)
        large_prime = self._get_line_prop(public_key_content, "prime")
        encrypter_public_key = self._get_line_prop(public_key_content, "encrypter")# public key generated during encryption
        encrypter_public_key_int = int(encrypter_public_key)
        # print("\n\t encrypter_public_key_int: ", encrypter_public_key_int)
        large_prime_int = int(large_prime)
        # print("\n\t large_prime_int: ", large_prime_int)
        encrypter_public_key_power = math.pow(encrypter_public_key_int, self.private_key)
        secret_key = int(encrypter_public_key_power) % large_prime_int

        secret_key_int = int(str(secret_key))
        self._file_helper(file_name=self.secret_key_file_name, file_mode="a+", content=f"\n\t Secret Key During Decryption:\n {str(secret_key)}",)
        self.secret_key = secret_key_int
        self.encrypter_public_key = encrypter_public_key_int
        self.large_prime = large_prime_int
        self.log_info("\n\t Secret key used in encrypting has been successfully generated...")

    def required_char(self, char:str, plain_char: str):
        req_char = ""
        if char == '.':
            req_char = f"{plain_char} \n"
        else:
            req_char = plain_char
        return req_char
    
    
    def decrypt_message(self):
        try:
            self.log_info(f"\n\t Decryption started: {datetime.now()}")
            self._secret_key_generator()
            encrypted_text = self._file_helper(file_mode="r", file_name=self.encrypted_message_file)
            self._file_helper(file_mode="w", file_name=self.decrypted_message_file, content="")
            char_to_decrypt = ""
            self.log_info(f"\n\t Generating Secret key inverse......")
            secret_key_inverse = self._get_modulo_inverse(inv_val=self.secret_key, mod_val=self.large_prime)
            forbidden_char = [ "-"]
            for char in encrypted_text:
                if char not in forbidden_char:
                    char_to_decrypt+=char
                else:
                    plain_char = char_to_decrypt
                    if char != " " and char_to_decrypt != " ":
                        try:
                            plain_char = self.decryption_dictionary[char_to_decrypt]
                        except:
                            unicode_char = (int(char_to_decrypt)*int(secret_key_inverse)) % self.large_prime
                            plain_char = chr(unicode_char)
                            self.decryption_dictionary[char_to_decrypt] = plain_char
                    self._file_helper(file_mode="a+", file_name=self.decrypted_message_file, content=self.required_char(char=char, plain_char=plain_char))
                    char_to_decrypt = ""
            self.log_info(f"\n\t Decryption has been successfully finished: {datetime.now()}")
        except:
            self.log_info(f"\n\t Something went wrong, during decryption. Are you sure you have passed the same private key, used during key generation?")

