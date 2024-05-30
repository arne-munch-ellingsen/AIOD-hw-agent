from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64
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
        operating_system = description.get('General_properties', {}).get('operating_system')
        num_cpus = description.get('HW_Technical_properties', {}).get('CPU', {}).get('num_cpus')
        accelerator_type = description.get('HW_Technical_properties', {}).get('Accelerator', {}).get('type')
        print(f"platform={platform}, name={name}, operating_system={operating_system}, num_cpus={num_cpus}, accelerator_type={accelerator_type}", flush=True)

        # Create a response object
        response = {
            'platform': platform,
            'name': name,
            'operating_system': operating_system,
            'num_cpus': num_cpus,
            'accelerator_type': accelerator_type
        }
        print(f"returned json is {jsonify(response)}", flush=True)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/receive_k8s_credentials', methods=['POST'])
def receive_k8s_credentials():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not validate_token(auth_header):
        return jsonify({'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        encrypted_credentials_b64 = data.get('credentials')
        encrypted_credentials = base64.urlsafe_b64decode(encrypted_credentials_b64)

        decrypted_credentials = private_key.decrypt(
            encrypted_credentials,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        k8s_credentials = json.loads(decrypted_credentials.decode())

        # Securely store the Kubernetes credentials (e.g., in a secrets manager, this is just a mock-up)
        store_k8s_credentials(k8s_credentials)

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
