from flask import Flask, request, jsonify
from flask_cors import CORS
from dlms_reader import read_dlms_meter

app = Flask(__name__)
CORS(app)

@app.route('/read-meter', methods=['POST'])
def read_meter():
    try:
        data = request.get_json()
        result = read_dlms_meter(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
