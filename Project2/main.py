from src.loader import load_png_image
from src.chunks import read_all_chunks, print_all_chunks
from src.rsa_math import generate_keypair, rsa_encrypt_number, rsa_decrypt_number
from src.cbc import cbc_encrypt, cbc_decrypt
from src.ecb import ecb_encrypt, ecb_decrypt


def main():

    print("=== SZYBKI TEST ALGORYTMÓW RSA ===")
    
    # 1. Generowanie krótkiego klucza (dla szybkości testu)
    public_key, private_key = generate_keypair(key_size=256)
    
    # 2. Przygotowanie testowych danych
    # Zwykły tekst zamieniony na surowe bajty (tak samo jak zrobimy to z pikselami)
    original_data = b"To jest tajna wiadomosc testowa dla naszego RSA!"
    print(f"\nOryginalne dane: {original_data}")

    # ----------------------------------------
    # 3. Test trybu ECB
    # ----------------------------------------
    print("\n--- TEST ECB ---")
    encrypted_ecb = ecb_encrypt(original_data, public_key)
    decrypted_ecb = ecb_decrypt(encrypted_ecb, private_key)
    
    # Pokazujemy tylko początek szyfrogramu (hex format jest czytelny dla ludzi)
    print(f"Szyfrogram (poczatek): {encrypted_ecb.hex()[:40]}...")
    print(f"Po deszyfrowaniu:      {decrypted_ecb}")
    
    # Upewniamy się asercją, że proces jest w 100% odwracalny
    if original_data == decrypted_ecb:
        print("[SUKCES] Tryb ECB dziala idealnie!")
    else:
        print("[BLAD] Tryb ECB psuje dane!")

    # ----------------------------------------
    # 4. Test trybu CBC
    # ----------------------------------------
    print("\n--- TEST CBC ---")
    # Pamiętaj, że CBC szyfruje też zwracając wygenerowany wektor inicjujący (IV)
    encrypted_cbc, iv = cbc_encrypt(original_data, public_key)
    decrypted_cbc = cbc_decrypt(encrypted_cbc, private_key, iv)
    
    print(f"Szyfrogram (poczatek): {encrypted_cbc.hex()[:40]}...")
    print(f"Po deszyfrowaniu:      {decrypted_cbc}")
    
    if original_data == decrypted_cbc:
        print("[SUKCES] Tryb CBC dziala idealnie!")
    else:
        print("[BLAD] Tryb CBC psuje dane!")

if __name__ == "__main__":
    main()