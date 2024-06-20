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


import math
class ElgamalDecryptionAlgorithm:
    def __init__(self, private_key: int):
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"
        self.encrypted_message_file = "./files/encrypted_message.txt"
        self.decrypted_message_file = "./files/encrypted_message.txt"
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
        public_key_content = self._file_helper(file_mode="rl",file_name=self.public_key_file_name)
        large_prime = self._get_line_prop(public_key_content, "prime")
        encrypter_public_key = self._get_line_prop(public_key_content, "encrypter")# public key generated during encryption
        encrypter_public_key_int = int(encrypter_public_key)
        print("\n\t encrypter_public_key_int: ", encrypter_public_key_int)
        large_prime_int = int(large_prime)
        print("\n\t large_prime_int: ", large_prime_int)

        encrypter_public_key_power = math.pow(encrypter_public_key_int, self.private_key)
        secret_key = int(encrypter_public_key_power) % large_prime_int
        print("\n\t secret_key: ", secret_key)

        secret_key_int = int(str(secret_key))
        self._file_helper(file_name=self.secret_key_file_name, file_mode="a+", content=f"\n\t Secret Key During Decryption:\n {str(secret_key)}",)
        self.secret_key = secret_key_int
        self.encrypter_public_key = encrypter_public_key_int
        self.large_prime = large_prime_int

        
    def decrypt(self):
        self._secret_key_generator()
        encrypted_text = self._file_helper(file_mode="r", file_name=self.encrypted_message)
        self._file_helper(file_mode="w", file_name=self.encrypted_message_file, content="")
        char_to_decrypt = ""
        for char in encrypted_text:
            char_to_write = str(char)
            if char != "-":
                char_to_decrypt+=char
            elif char == " ":
                plain_char = ""
                try:
                    plain_char = self.decryption_dictionary[char_to_decrypt]
                except:
                    unicode_char = (char_to_decrypt/self.secret_key) % self.large_prime
                    plain_char = chr(unicode_char)
                    self.decryption_dictionary[char_to_decrypt] = plain_char
                self._file_helper(file_mode="a+", file_name=self.encrypted_message_file, content=f"{f"{plain_char} \n" if char == "." else plain_char}-")
            return char_to_write
        

encrypted_message_file_name = "./files/encrypted_message.txt"
private_key = 3 # Provide private key used, during key generation
ff = ElgamalDecryptionAlgorithm( private_key=private_key)
gf = ff.decrypt()


