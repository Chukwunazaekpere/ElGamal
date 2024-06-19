


import math


class EncryptionAlgorithm:
    def __init__(self, private_key: int, plain_message_file_name:str):
        self.private_key = private_key
        self.public_key_file_name = "./files/public_keys.txt"
        self.encoded_message_file_name = "./files/encoded_message.txt"
        self.encrypted_message_file = "./files/encrypted_message.txt"
        self.plain_message = plain_message_file_name
        self.secret_key_file_name = "./files/secret_key.txt" 
        self.secret_key = "" 
        self.primitive_root = ""
        self.public_key = "" 
        self.large_prime = "" 


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
        print("\n\t large_prime: ", large_prime)

        public_key = self._get_line_prop(public_key_content, "public")
        print("\n\t public_key: ", public_key)

        primitive_root = self._get_line_prop(public_key_content, "primitive")
        print("\n\t primitive_root: ", primitive_root)

        public_key_power = math.pow(float(public_key), float(self.private_key))
        secret_key = public_key_power % large_prime 
        self._file_helper(self.public_key_file_name, f"\n\t Secret Key:\n {str(secret_key)}")
        self.secret_key = secret_key
        self.public_key = public_key
        self.large_prime = large_prime
        self.primitive_root = primitive_root

    def _generate_encrypter_public_key(self):
        self._secret_key_generator()
        primitive_power = math.pow(self.primitive_root, self.private_key)
        public_key = primitive_power % self.large_prime 
        self._file_helper(self.public_key_file_name, f"\n\t Encrypter Public Key:\n {str(public_key)}")
        return public_key



    def encrypt_message(self):
        self._encode_plaintext_chars() # Encode characters in plain text
        encoded_message_file = self._file_helper(file_mode="r", file_name=self.encoded_message_file_name)
        self._generate_encrypter_public_key()
        print("\n\t secret-key: ", self.secret_key)
        for encoded_char in encoded_message_file:
            encrypted_char = self.secret_key*encoded_char % self.large_prime
            self._file_helper(file_mode="a+", file_name=self.encrypted_message_file, content=encrypted_char)
        

plain_message_file_name = "./files/plain_message.txt"
private_key = 200
ff = EncryptionAlgorithm(plain_message_file_name=plain_message_file_name, private_key=private_key)
gf = ff.encrypt_message()


# public_key = ff.generate_public_key()
# print("\n\t ascii_letters: ", ord("E"))
# print("\n\t public_key: ",public_key, len(str(public_key)))
