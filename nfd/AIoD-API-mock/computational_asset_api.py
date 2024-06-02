from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding
import json

app = Flask(__name__)

# Load the private key
with open("private_key.pem", "rb") as private_key_file:
    private_key = serialization.load_pem_private_key(
        private_key_file.read(),
        password=None,
    )

@app.route('/computational_asset', methods=['POST'])
def computational_asset():
    print("Received HW agent meta data", flush=True)
    try:
        # Get data from request
        data = request.get_json()

        # Extract parameters
        platform = data.get('platform')
        name = data.get('name')
        description_str = data.get('description')

        # Validate the inputs (optional)
        if not platform or not name or not description_str:
            return jsonify({'error': 'Missing required parameter(s)'}), 400

        # Convert the description string to a JSON object
        description = json.loads(description_str)

        # Extract additional properties from description
        print("Received computational_asset:")
        print(description_str)

        # Create a response object
        response = {
            'platform': platform,
            'name': name
        }
        print(f"returned json is {jsonify(response)}", flush=True)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/k8s_credentials', methods=['POST'])
def k8s_credentials():
    print("In receive_k8s_credentials", flush=True)
    auth_header = request.headers.get('Authorization')
    if not auth_header or not validate_token(auth_header):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        print("In receive_k8s_credentials, get the request data", flush=True)
        data = request.get_json()
        encrypted_key_b64 = data.get('encrypted_key')
        encrypted_blob_b64 = data.get('blob')
        encrypted_key = base64.urlsafe_b64decode(encrypted_key_b64)
        encrypted_blob = base64.urlsafe_b64decode(encrypted_blob_b64)

        iv = encrypted_blob[:16]
        encrypted_data = encrypted_blob[16:]

        # Decrypt the AES key with the private RSA key
        decrypted_aes_key = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print("In receive_k8s_credentials, decrypt the request data", flush=True)
        # Decrypt the text blob using the decrypted AES key
        cipher = Cipher(algorithms.AES(decrypted_aes_key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Unpad the decrypted data
        unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(padded_data) + unpadder.finalize()
        decrypted_text = decrypted_data.decode()

        # Securely store the decrypted text blob
        store_k8s_credentials(decrypted_text)

        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def validate_token(token):
    # Implement your token validation logic here
    return True

def store_k8s_credentials(credentials):
    # Implement secure storage logic here
    print(f"Storing credentials securely: {credentials}", flush=True)

if __name__ == '__main__':
    # Replace with paths to your actual certificate and key files
    app.run(ssl_context=('cert.pem', 'private_key.pem'))
