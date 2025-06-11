from cryptography.fernet import Fernet
import os
import base64
import settings as s
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SimpleEncryption:
    def __init__(self, password: str = "default_game_password"):
        """
        Inicjalizuje szyfrowanie z hasłem.
        W prawdziwej aplikacji hasło powinno być bezpiecznie przechowywane.
        """
        self.password = password.encode()
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)

    def _generate_key(self):
        """Generuje klucz szyfrowania na podstawie hasła"""
        salt = s.DB_SECRET.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key

    def encrypt_text(self, text: str) -> str:
        """Szyfruje tekst i zwraca jako string"""
        if not text:
            return ""
        encrypted_data = self.cipher.encrypt(text.encode())
        return base64.urlsafe_b64encode(encrypted_data).decode()

    def decrypt_text(self, encrypted_text: str) -> str:
        """Deszyfruje tekst"""
        if not encrypted_text:
            return ""
        try:
            encrypted_data = base64.urlsafe_b64decode(encrypted_text.encode())
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            print(f"Błąd deszyfrowania: {e}")
            return ""


encryptor = SimpleEncryption()
