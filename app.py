from implementation.public_key_generator import ElGamalPublicKeyGen
from implementation.encryption_algorithm import ElGamalEncryptionAlgorithm
from implementation.decryption_algorithm import ElgamalDecryptionAlgorithm

def main():

    private_key = 7
    plain_message_file_name = "./files/plain_message.txt"

    # Create a new public key
    key_generator = ElGamalPublicKeyGen(private_key=private_key)
    key_generator.generate_public_key()

    # Encrypt message

    message_encryptor = ElGamalEncryptionAlgorithm(plain_message_file_name=plain_message_file_name, private_key=private_key)
    message_encryptor.encrypt_message()

    # Decrypt Message
    message_decryptor = ElgamalDecryptionAlgorithm(private_key=private_key)
    message_decryptor.decrypt_message()


if __name__ == "__main__":
    main()
