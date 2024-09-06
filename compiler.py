from flask import Flask, request, jsonify
import subprocess
import os
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def run_code(language, code):
    temp_filename = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{language}") as temp_file:
            temp_file.write(code.encode())
            temp_filename = temp_file.name

        if language == 'python':
            result = subprocess.run(['python', temp_filename], capture_output=True, text=True)
        elif language == 'cpp':
            compile_result = subprocess.run(['g++', '-o', 'main', temp_filename], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return '', compile_result.stderr
            result = subprocess.run(['./main'], capture_output=True, text=True)
        elif language == 'php':
            result = subprocess.run(['php', temp_filename], capture_output=True, text=True)
        elif language == 'javascript':
            result = subprocess.run(['node', temp_filename], capture_output=True, text=True)
        elif language == 'c':
            compile_result = subprocess.run(['gcc', '-o', 'main', temp_filename], capture_output=True, text=True)
            if compile_result.returncode != 0:
                return '', compile_result.stderr
            result = subprocess.run(['./main'], capture_output=True, text=True)
        else:
            return 'Unsupported language', ''

        return result.stdout, result.stderr
    finally:
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
        if os.path.exists('main'):
            os.remove('main')


@app.route('/run', methods=['POST'])
def run_code_endpoint():
    data = request.json
    language = data.get('language')
    code = data.get('code')

    if not language or not code:
        return jsonify({'stdout': '', 'stderr': 'Missing language or code'}), 400

    stdout, stderr = run_code(language, code)
    return jsonify({'stdout': stdout, 'stderr': stderr})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
