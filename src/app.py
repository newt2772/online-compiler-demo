from flask import Flask, render_template, request, jsonify
import subprocess
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.form.get('code', '')
    
    if not code:
        return jsonify({'success': False, 'output': 'No code provided'})
    
    try:
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as src_file:
            src_file.write(code.encode())
            src_path = src_file.name
        exec_path = src_path + '.out'
        
        # Compile the code
        compile_result = subprocess.run(
            ['g++', src_path, '-o', exec_path],
            capture_output=True,
            text=True
        )
        
        if compile_result.returncode != 0:
            return jsonify({
                'success': False,
                'output': compile_result.stderr
            })
        
        # Run the compiled program
        run_result = subprocess.run(
            [exec_path],
            capture_output=True,
            text=True,
            timeout=5  # 5 second timeout for safety
        )
        
        return jsonify({
            'success': True,
            'output': run_result.stdout
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'output': 'Error: Program timed out (possible infinite loop)'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'output': f'Error: {str(e)}'
        })
    finally:
        # Clean up temporary files
        for f in [src_path, exec_path]:
            if f and os.path.exists(f):
                os.remove(f)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)