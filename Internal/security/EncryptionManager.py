import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class EncryptionManager:
    @staticmethod
    def _generate_key(password: str, salt: bytes):
        """Transformă parola într-o cheie binară de 32 bytes folosind PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def encrypt_to_file(file_path: str, data_dict: dict, password: str):
        """Criptează un dicționar și îl salvează ca fișier binar."""
        # 1. Transformăm dicționarul în text JSON
        import json
        json_data = json.dumps(data_dict)

        # 2. Generăm un 'salt' unic pentru acest fișier
        salt = os.urandom(16)
        key = EncryptionManager._generate_key(password, salt)
        fernet = Fernet(key)

        # 3. Criptăm datele
        encrypted_content = fernet.encrypt(json_data.encode())

        # 4. Salvăm SALT + DATE CRIPTATE (sarea e necesară pentru decriptare)
        with open(file_path, "wb") as f:
            f.write(salt + encrypted_content)

    @staticmethod
    def decrypt_from_file(file_path: str, password: str):
        """Citește un fișier criptat și returnează dicționarul original."""
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "rb") as f:
            bundle = f.read()

        # Separăm sarea (primii 16 bytes) de conținut
        salt = bundle[:16]
        encrypted_content = bundle[16:]

        try:
            key = EncryptionManager._generate_key(password, salt)
            fernet = Fernet(key)
            decrypted_json = fernet.decrypt(encrypted_content).decode()
            import json
            return json.loads(decrypted_json)
        except Exception:
            # Dacă parola e greșită, Fernet va arunca o eroare
            return None