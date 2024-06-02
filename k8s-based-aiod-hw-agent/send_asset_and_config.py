import requests
import json
import base64
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

class DataEncryptorSender:
    def __init__(self, public_key_path, config_path, comp_asset_url, credential_url, cert_path):
        self.public_key_path = public_key_path
        self.config_path = config_path
        self.comp_asset_url = comp_asset_url
        self.credential_url = credential_url
        self.cert_path = cert_path
        self.public_key = self.load_public_key()
        self.headers = {'Authorization': 'Bearer your-auth-token'}


    def load_public_key(self):
        with open(self.public_key_path, "rb") as public_key_file:
            return serialization.load_pem_public_key(public_key_file.read())

    def read_text_blob(self):
        with open(self.config_path, "r") as config_file:
            return config_file.read()

    def generate_aes_key(self):
        return os.urandom(32)  # AES-256 key

    def encrypt_blob(self, text_blob, aes_key):
        iv = os.urandom(16)  # AES block size is 16 bytes
        cipher = Cipher(algorithms.AES(aes_key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(text_blob.encode()) + padder.finalize()

        encrypted_blob = encryptor.update(padded_data) + encryptor.finalize()
        return iv, encrypted_blob

    def encrypt_aes_key(self, aes_key):
        return self.public_key.encrypt(
            aes_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    def base64_encode(self, data):
        return base64.urlsafe_b64encode(data).decode()

    def send_computational_asset(self, payload):
        response = requests.post(self.comp_asset_url, json=payload, headers=self.headers, verify=False)
        print("Computational Asset Status Code:", response.status_code)
        print("Computational Asset Response JSON:", response.json())
        return response

    def send_encrypted_blob(self, encrypted_key_b64, encrypted_blob_b64):
        blob_payload = {
            'encrypted_key': encrypted_key_b64,
            'blob': encrypted_blob_b64
        }
        response = requests.post(self.credential_url, json=blob_payload, headers=self.headers, verify=False)
        print("Encrypted Blob Status Code:", response.status_code)
        print("Encrypted Blob Response JSON:", response.json())
        return response

    def process_and_send(self, comp_asset_payload):
        text_blob = self.read_text_blob()
        aes_key = self.generate_aes_key()
        iv, encrypted_blob = self.encrypt_blob(text_blob, aes_key)
        encrypted_key = self.encrypt_aes_key(aes_key)

        encrypted_blob_b64 = self.base64_encode(iv + encrypted_blob)
        encrypted_key_b64 = self.base64_encode(encrypted_key)

        self.send_computational_asset(comp_asset_payload)
        self.send_encrypted_blob(encrypted_key_b64, encrypted_blob_b64)

