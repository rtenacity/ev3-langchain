from flask import Flask, request, jsonify
import sys
import traceback
from contextlib import redirect_stdout
import io

app = Flask(__name__)

@app.route('/receive_code', methods=['POST'])
def receive_code():
    code = request.json.get('code', '')
    output = io.StringIO()  # Create an in-memory text stream
        
    try:
        with redirect_stdout(output):
            exec(code)
    except Exception as e:
        output = ''.join(traceback.format_exception(None, e, e.__traceback__))

    return jsonify({'result': output.getvalue()})

if __name__ == '__main__':
    app.run(debug=True)
