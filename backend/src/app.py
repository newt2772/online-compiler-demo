from flask import Flask, request, jsonify, render_template
import subprocess
import os
import tempfile
import resource

app = Flask(__name__)

# Security configurations
app.config['MAX_INPUT_LENGTH'] = 10000  # 10KB max
app.config['COMPILE_TIMEOUT'] = 10  # seconds
app.config['EXECUTION_TIMEOUT'] = 5  # seconds
app.config['MEMORY_LIMIT'] = 256 * 1024 * 1024  # 256MB

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.form.get('code', '')[:app.config['MAX_INPUT_LENGTH']]
    user_input = request.form.get('input', '')[:app.config['MAX_INPUT_LENGTH']]
    
    if not code:
        return jsonify({'success': False, 'output': 'No code provided'})

    # Create temp files
    src_file = tempfile.NamedTemporaryFile(suffix='.cpp', delete=False)
    input_file = tempfile.NamedTemporaryFile(delete=False)
    exec_path = src_file.name + '.out'
    
    try:
        # Write files
        with open(src_file.name, 'w') as f:
            f.write(code)
        with open(input_file.name, 'w') as f:
            f.write(user_input)

        # Compile with timeout
        try:
            compile_result = subprocess.run(
                ['g++', src_file.name, '-o', exec_path],
                capture_output=True,
                text=True,
                timeout=app.config['COMPILE_TIMEOUT']
            )
        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'output': f'Compilation timed out after {app.config["COMPILE_TIMEOUT"]}s'
            })

        if compile_result.returncode != 0:
            return jsonify({
                'success': False,
                'output': compile_result.stderr
            })

        # Execute with limits
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (app.config['EXECUTION_TIMEOUT'], app.config['EXECUTION_TIMEOUT']))
            resource.setrlimit(resource.RLIMIT_AS, (app.config['MEMORY_LIMIT'], app.config['MEMORY_LIMIT']))

            run_result = subprocess.run(
                [exec_path],
                stdin=open(input_file.name),
                capture_output=True,
                text=True,
                timeout=app.config['EXECUTION_TIMEOUT']
            )
            
            return jsonify({
                'success': True,
                'output': run_result.stdout,
                'error': run_result.stderr
            })

        except subprocess.TimeoutExpired:
            return jsonify({
                'success': False,
                'output': f'Execution timed out after {app.config["EXECUTION_TIMEOUT"]}s'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'output': f'Runtime error: {str(e)}'
            })

    finally:
        # Cleanup
        for f in [src_file.name, input_file.name, exec_path]:
            try:
                if os.path.exists(f):
                    os.unlink(f)
            except:
                pass

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)