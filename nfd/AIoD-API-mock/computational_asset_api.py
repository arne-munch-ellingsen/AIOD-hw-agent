from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
