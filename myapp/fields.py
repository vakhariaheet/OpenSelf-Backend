from django.db import models
from cryptography.fernet import Fernet

salt = b'qy-_4bzx9wkM7g7x63YCic_GOTbPT-EZFKYiHj65DbA='  
cipher_suit = Fernet(salt)


# Create Encryption Field
class EncryptionField(models.TextField):  
    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        self.cipher_suite = cipher_suit      
    
    # Decrypts data read from the database.
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        decrypted_value = self.cipher_suite.decrypt(value.encode()).decode()
        return decrypted_value  

    # Converts values to their Python representation, including decryption.
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, bytes):
            value = value.decode()
        decrypted_value = self.cipher_suite.decrypt(value.encode()).decode()
        return decrypted_value

    # Encrypts data before saving it to the database.
    def get_prep_value(self, value):
        if value is None:
            return value
        encrypted_value = self.cipher_suite.encrypt(value.encode()).decode()
        return encrypted_value

