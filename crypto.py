import base64
import binascii
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


# credit goes to https://www.quickprogrammingtips.com/python/aes-256-encryption-and-decryption-in-python.html

class AES256:
    BLOCK_SIZE = 16

    def __init__(self, password):
        self.key = hashlib.sha256(password.encode('utf-8')).digest()

    def encrypt_text(self, cleartext):
        cleartext = self.add_padding(cleartext)
        clearbytes = cleartext.encode("utf-8")
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(clearbytes))

    def decrypt_text(self, base64cipherbytes):
        enc = base64.b64decode(base64cipherbytes)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.remove_padding(cipher.decrypt(enc[16:])).decode("utf-8")

    def encrypt_bytes(self, clearbytes):
        cleartext = clearbytes.decode("utf-8")
        return self.encrypt_text(cleartext)

    def decrypt_bytes(self, base64cipherbytes):
        cleartext = self.decrypt_text(base64cipherbytes)
        return bytes(cleartext, 'utf-8')

    def add_padding(self, s):
        return s + (AES256.BLOCK_SIZE - len(s) % AES256.BLOCK_SIZE) * chr(AES256.BLOCK_SIZE - len(s) % AES256.BLOCK_SIZE)

    def remove_padding(self, s):
        return s[:-ord(s[len(s) - 1:])]
