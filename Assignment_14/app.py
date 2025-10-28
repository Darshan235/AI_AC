from flask import Flask, request, send_from_directory, redirect, url_for

app = Flask(__name__, static_folder='.')

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('.', '14_1.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('index'))
    username = (request.form.get('username') or '').strip()
    password = (request.form.get('password') or '').strip()
    if not username or not password:
        return "Username and password are required.", 400
    print("Login successful for user:", username)
    return f"Login successful: {username}", 200

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)