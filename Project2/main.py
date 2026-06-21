from src.loader import load_png_image
from src.chunks import read_all_chunks, print_all_chunks
from src.rsa_math import generate_keypair, rsa_encrypt_number, rsa_decrypt_number


def main():

    image_path = './test.png'  
    image_bytes = load_png_image(image_path)

    print("\n--- 1. Scanning file structure ---")
    chunks = read_all_chunks(image_bytes)
    print_all_chunks(chunks, image_bytes)

    print("\n--- 2. RSA Key Generation ---")
    public_key, private_key = generate_keypair(key_size=512)
    print(f"Public Key: {public_key}")
    print(f"Private Key: {private_key}")

    print("\n--- 3. RSA Encryption and Decryption of a Sample Number ---")
    sample_number = 123456789
    encrypted_number = rsa_encrypt_number(sample_number, public_key)
    print(f"Sample Number: {sample_number}")
    print(f"Encrypted Number: {encrypted_number}")
    decrypted_number = rsa_decrypt_number(encrypted_number, private_key)
    print(f"Decrypted Number: {decrypted_number}")

if __name__ == "__main__":
    main()