


import random
import math


class EncryptionAlgorithm:
    def __init__(self, private_key: int, plain_message_file_name:str):
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"
        self.encoded_message_file_name = "./files/encoded_message.txt"
        self.plain_message = plain_message_file_name
        self.secret_key_file_name = "./files/secret_key.txt" 
        

    def _file_helper(self, file_name:str, file_mode:str, content=""):
        """Read file containing message to be encrypted or decrypted"""
        if file_mode == "r":
            with open(file_name, "r")as file_content:
                file_content.read()
            return file_content
        elif file_mode == "rl":
            with open(file_name, "r")as file_content:
                file_content_list = file_content.readlines()
            return file_content_list
        else:
            with open(file_name, "+a")as file_handle:
                file_handle.write(content)

    def _get_line_prop(self, read_line_data:list, key_word: str):
        seen_pub = False
        for l in read_line_data:
            if seen_pub or l.lower().__contains__(key_word):
                seen_pub = True
                if seen_pub and ":" not in l:
                    return l
                    # print("\n\t GF: ", l)
    
    def _encode_plaintext_chars(self):
        plain_text = self._file_helper(file_mode="r", file_name=self.plain_message)
        for char in plain_text:
            char_to_write = char
            if char != " ":
                char_to_code = ord(char)
                char_to_write = char_to_code
            self._file_helper(file_mode="a+", file_name=self.encoded_message_file_name, content=char_to_write)
    
    def _secret_key_generator(self):
        public_key_content = self._file_helper(file_mode="rl",file_name=self.public_key_file_name)
        large_prime = self._get_line_prop(public_key_content, "prime")
        public_key = self._get_line_prop(public_key_content, "public")
        public_key_power = math.pow(public_key, self.private_key)
        secret_key = public_key_power % large_prime 
        self._file_helper(self.secret_key_file_name, "\n\t Secret Key: \n")
        self._file_helper(self.secret_key_file_name, str(secret_key))



    def encrypt_message(self):
        large_prime, primitive_root = self._generate_primitive_root()
        primitive_power = math.pow(primitive_root, self.private_key)
        public_key = primitive_power % large_prime 
        self._file_helper(self.public_key_file_name, "\n\t Public Key: \n")
        self._file_helper(self.public_key_file_name, str(public_key))
        return public_key

plain_message_file_name = "./files/plain_message.txt"
public_key_file_name = "./files/public_keys.txt"
private_key = 200
ff = EncryptionAlgorithm(plain_message_file_name=plain_message_file_name, private_key=private_key)
gf = ff._file_helper(file_mode="rl",file_name=public_key_file_name)


# public_key = ff.generate_public_key()
# print("\n\t ascii_letters: ", ord("E"))
# print("\n\t public_key: ",public_key, len(str(public_key)))
