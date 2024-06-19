


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
        public_key_content = self._file_helper(file_mode="rl",file_name=self.public_key_file_name)
        large_prime = self._get_line_prop(public_key_content, "prime")
        print("\n\t large_prime: ", large_prime)

        public_key = self._get_line_prop(public_key_content, "public")
        print("\n\t public_key: ", public_key)

        primitive_root = self._get_line_prop(public_key_content, "primitive")
        print("\n\t primitive_root: ", primitive_root)
        print("\n\t self.private_key: ", self.private_key)

        pub_key_int = int(public_key.split(".")[0])
        large_prime_int = int(large_prime.split(".")[0])
        primitive_root_int = int(primitive_root.split(".")[0])

        public_key_power = math.pow(pub_key_int, self.private_key)
        secret_key = public_key_power % large_prime_int
        secret_key_int = int(str(secret_key).split(".")[0])
        self._file_helper(self.public_key_file_name, f"\n\t Secret Key:\n {str(secret_key)}")
        self.secret_key = secret_key_int
        self.public_key = pub_key_int
        self.large_prime = large_prime_int
        self.primitive_root = primitive_root_int

    def _generate_encrypter_public_key(self):
        self._secret_key_generator()
        primitive_power = math.pow(self.primitive_root, self.private_key)
        public_key = primitive_power % self.large_prime 
        self._file_helper(self.public_key_file_name, f"\n\t Encrypter Public Key:\n {str(public_key)}")
        return public_key



    def encrypt_message(self):
        encoded_message_file = self._file_helper(file_mode="r", file_name=self.encoded_message_file_name)
        self._generate_encrypter_public_key()
        print("\n\t encoded_char-key: ", self.secret_key)
        print("\n\t encoded_message_file: ", encoded_message_file)
        plain_text = self._file_helper(file_mode="r", file_name=self.plain_message)
        self._file_helper(file_mode="w", file_name=self.encrypted_message_file, content="")
        for char in plain_text:
            char_to_write = str(char)
            if char != " ":
                char_to_write = ord(char)
                # print("\n\t encoded_char-key: ", encoded_char)
                encrypted_char = self.secret_key*char_to_write % self.large_prime
                char_to_write = encrypted_char
            self._file_helper(file_mode="a+", file_name=self.encrypted_message_file, content=f"{char_to_write}-")
        

plain_message_file_name = "./files/plain_message.txt"
private_key = 27
ff = EncryptionAlgorithm(plain_message_file_name=plain_message_file_name, private_key=private_key)
gf = ff.encrypt_message()


# public_key = ff.generate_public_key()
# print("\n\t ascii_letters: ", ord("E"))
# print("\n\t public_key: ",public_key, len(str(public_key)))
