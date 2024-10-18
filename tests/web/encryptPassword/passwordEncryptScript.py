from cryptography.fernet import Fernet

# Generate a key (do this once and store the key securely)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt the password
password = "user12345"
encrypted_password = cipher_suite.encrypt(password.encode())

# Save the key and encrypted password securely
with open("secret.key", "wb") as key_file:
    key_file.write(key)
with open("password.enc", "wb") as password_file:
    password_file.write(encrypted_password)

print(f"Encrypted Password: {encrypted_password}")
