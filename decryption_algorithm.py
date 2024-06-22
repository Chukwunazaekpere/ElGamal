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
import logging
logger = logging.getLogger(__name__)
log_date = datetime.now()
logging.basicConfig(level=logging.INFO)


class ElgamalDecryptionAlgorithm:
    def __init__(self, private_key: int):
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"
        self.encrypted_message_file = "./files/encrypted_message.txt"
        self.decrypted_message_file = "./files/decrypted_message.txt"
        self.secret_key = "" 
        self.secret_key_file_name = "./files/secret_key.txt" 
        self.encrypter_public_key = "" 
        self.large_prime = "" 
        self.decryption_dictionary = {} #dictionary where plain-character is key & encrypted character is the value. This is to reduce the extra time taken for excrypting plain characters that have been encrypted already



    def _file_helper(self, file_name:str, file_mode:str, content=""):
        """Read file containing message to be encrypted or decrypted"""
        if file_mode == "r":
            with open(file_name, "r")as file_content:
                content = file_content.read()
            return content
        elif file_mode == "rl":
            with open(file_name, "r")as file_content:
                file_content_list = file_content.readlines()
            return file_content_list
        elif file_mode == "w":
            with open(file_name, "w")as file_handle:
                file_handle.write(str(content))
        else:
            with open(file_name, "+a")as file_handle:
                file_handle.write(str(content))

    def _get_modulo_inverse(self, inv_val:int, mod_val:int):
        """Get modulo inverse of val"""
        logging.info(msg=f"\n\t {datetime.now()} Generating modulo inverse")
        count = 2
        while count < mod_val:
            # print("\n\t count: ", count)
            val = inv_val*count % mod_val
            if val == 1:
                modulo_inverse = count
                return modulo_inverse
            count+=1
        return 1


    def _get_line_prop(self, read_line_data:list, key_word: str):
        seen_pub = False
        for l in read_line_data:
            if seen_pub or l.lower().__contains__(key_word):
                seen_pub = True
                if seen_pub and ":" not in l:
                    return l
                    # print("\n\t GF: ", l)
    
    def _secret_key_generator(self):
        """Geenerates the secret key that was used during encryption"""
        logging.info(msg="\n\t ElGamalEncryptionAlgorithm is generating the secret key used in encryption...")
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
        logging.info(msg="\n\t Secret key used in encrypting has been successfully generated...")

        
    def decrypt(self):
        try:
            logging.info(msg=f"\n\t Decryption started: {datetime.now()}")
            self._secret_key_generator()
            encrypted_text = self._file_helper(file_mode="r", file_name=self.encrypted_message_file)
            self._file_helper(file_mode="w", file_name=self.decrypted_message_file, content="")
            char_to_decrypt = ""
            logging.info(msg=f"\n\t Generating Secret key inverse......")
            secret_key_inverse = self._get_modulo_inverse(inv_val=self.secret_key, mod_val=self.large_prime)
            # print("\n\t secret_key_inverse: ", secret_key_inverse)
            forbidden_char = [ "-"]
            for char in encrypted_text:
                if char not in forbidden_char:
                    char_to_decrypt+=char
                    # print("\n\t if-char_to_decrypt: ", char_to_decrypt)
                else:
                    plain_char = char_to_decrypt
                    if char != " " and char_to_decrypt != " ":
                        try:
                            plain_char = self.decryption_dictionary[char_to_decrypt]
                        except:
                            unicode_char = (int(char_to_decrypt)*int(secret_key_inverse)) % self.large_prime
                            # print("\n\t if-unicode_char: ", unicode_char)
                            plain_char = chr(unicode_char)
                            self.decryption_dictionary[char_to_decrypt] = plain_char
                    self._file_helper(file_mode="a+", file_name=self.decrypted_message_file, content=f"{f"{plain_char} \n" if char == "." else plain_char}")
                    char_to_decrypt = ""
            logging.info(msg=f"\n\t Decryption has been successfully finished: {datetime.now()}")
        except:
            logging.info(msg=f"\n\t Something went wrong, during decryption. Are you sure you have passed the same private key, used during key generation?")
        

private_key = 7 # Provide private key used, during key generation
elgamal = ElgamalDecryptionAlgorithm( private_key=private_key)
decrypt = ff.decrypt()


