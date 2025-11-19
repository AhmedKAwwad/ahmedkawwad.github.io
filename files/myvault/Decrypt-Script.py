import base64
import hashlib
from cryptography.fernet import Fernet, InvalidToken
from cryptography.exceptions import InvalidKey

def generate_key(password):
    password_bytes = password.encode('utf-8')
    key = hashlib.sha256(password_bytes).digest()
    return base64.urlsafe_b64encode(key)

def try_decrypt(encrypted_data, password, cipher):
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        return True, decrypted_data
    except (InvalidToken, InvalidKey):
        return False, None
    except Exception:
        return False, None

def decrypt_file(file_name):
    try:
        # Read the encrypted file content
        with open(file_name, 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        
        # Read passwords from combinations.txt
        with open('combinations.txt', 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f]
        
        print(f"Starting brute force with {len(passwords)} combinations...")
        
        for i, password in enumerate(passwords):
            # Show progress every 1000 attempts
            if i % 1000 == 0:
                print(f"Tried {i} passwords...", end='\r')
            
            key = generate_key(password)
            cipher = Fernet(key)
            success, decrypted_data = try_decrypt(encrypted_data, password, cipher)
            
            if success:
                print(f"\nSuccess! Password found: {password}")
                # Save the decrypted content
                output_file_name = file_name.replace('encrypted_', 'decrypted_')
                with open(output_file_name, 'wb') as decrypted_file:
                    decrypted_file.write(decrypted_data)
                print(f"Decrypted file saved as '{output_file_name}'")
                return True
                
        print("\nDecryption failed: No valid password found in combinations.txt")
        return False
            
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found!")
        return False
    except Exception as e:
        print(f"Unexpected error during decryption: {str(e)}")
        return False

def main():
    file_name = input("Enter the encrypted file name to decrypt: ")
    decrypt_file(file_name)

if __name__ == "__main__":
    main() 