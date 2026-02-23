import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class EncryptionManager:
    @staticmethod
    def _generate_key(password: str, salt: bytes):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    @staticmethod
    def encrypt_to_file(file_path: str, data_dict: dict, password: str):
        import json
        json_data = json.dumps(data_dict)

        salt = os.urandom(16)
        key = EncryptionManager._generate_key(password, salt)
        fernet = Fernet(key)
        encrypted_content = fernet.encrypt(json_data.encode())
        with open(file_path, "wb") as f:
            f.write(salt + encrypted_content)

    @staticmethod
    def decrypt_from_file(file_path: str, password: str):
        if not os.path.exists(file_path):
            return {}
        with open(file_path, "rb") as f:
            bundle = f.read()
        salt = bundle[:16]
        encrypted_content = bundle[16:]

        try:
            key = EncryptionManager._generate_key(password, salt)
            fernet = Fernet(key)
            decrypted_json = fernet.decrypt(encrypted_content).decode()
            import json
            return json.loads(decrypted_json)
        except Exception as e:
            print(e)
            return None