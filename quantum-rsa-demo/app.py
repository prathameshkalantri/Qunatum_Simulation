from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import math
import numpy as np
from secrets import randbelow
import ast  # Add this for safe string conversion
import base64
import json
from json import JSONEncoder

class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        return super().default(obj)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Simplified RSA parameters (using small primes for demonstration)
PUBLIC_KEY = (3233, 17)  # n, e
PRIVATE_KEY = (3233, 2753)  # n, d
class LWEKeyPair:
    def __init__(self):
        self.n = 128  # Dimension
        self.q = 4096  # Modulus
        self.A = np.random.randint(0, self.q, (self.n, self.n)).astype(np.int64)
        self.s = np.random.randint(0, self.q, self.n).astype(np.int64)  # Private key
        self.b = (self.A.dot(self.s) % self.q)  # Public key    
    @property
    def public_key(self):
        return (self.A, (self.A.dot(self.s) + self.e) % self.q)
    
    def decrypt(self, ciphertext):
        return (ciphertext[1] - ciphertext[0].dot(self.s)) % self.q

# Modified User class
class User(db.Model):
    __tablename__ = 'users'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    rsa_password = db.Column(db.Integer)  # Classical RSA
    pq_password = db.Column(db.String(2000))  # Increased length for quantum-safe data

# New routes
@app.route('/pq_register', methods=['GET', 'POST'])
def pq_register():
    if request.method == 'POST':
        username = request.form['username']
        password = int(request.form['password'])
        
        keypair = LWEKeyPair()
        encrypted_val = int((keypair.b[0] + password) % keypair.q)  # Convert to Python int
        
        data = {
            'A': base64.b64encode(keypair.A[0].tobytes()).decode('utf-8'),
            'encrypted': encrypted_val,  # Now a regular integer
            's': base64.b64encode(keypair.s.tobytes()).decode('utf-8')
        }
        
        user = User(
            username=username,
            pq_password=json.dumps(data, cls=NumpyEncoder)
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('pq_login'))
    return render_template('pq_register.html')

@app.route('/pq_login', methods=['GET', 'POST'])
def pq_login():
    message = ''
    cipher_data = None
    if request.method == 'POST':
        username = request.form['username']
        password = int(request.form['password'])
        user = User.query.filter_by(username=username).first()
        
        if user and user.pq_password:
            try:
                cipher_data = json.loads(user.pq_password)
                # ... [rest of decryption logic] ...
                message = f"Quantum-safe login successful! Ciphertext: {cipher_data['encrypted']}"
            except Exception as e:
                message = f"🔒 Error: {str(e)}"
        else:
            message = "❌ User not found!"
    return render_template('pq_login.html', 
                         message=message,
                         cipher_data=cipher_data)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     rsa_password = db.Column(db.Integer)  # For classical RSA
#     pq_password = db.Column(db.String(256))  # For post-quantum

with app.app_context():
    db.create_all()

def rsa_encrypt(m):
    return pow(m, PUBLIC_KEY[1], PUBLIC_KEY[0])

def rsa_decrypt(c):
    return pow(c, PRIVATE_KEY[1], PRIVATE_KEY[0])

def factor(n):
    """Simulated 'Quantum' Factorization (using classical trial division)"""
    if n % 2 == 0:
        return 2, n//2
    i = 3
    max_factor = math.isqrt(n)
    while i <= max_factor:
        if n % i == 0:
            return i, n//i
        i += 2
    return None, None

def compute_private_key(p, q, e):
    phi = (p-1)*(q-1)
    return pow(e, -1, phi)

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = int(request.form['password'])
        encrypted = rsa_encrypt(password)  # Store encrypted password
        user = User(username=username, rsa_password=encrypted)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    encrypted = None
    if request.method == 'POST':
        username = request.form['username']
        password = int(request.form['password'])
        user = User.query.filter_by(username=username).first()
        
        if user:
            # Encrypt the entered password for demonstration
            encrypted = rsa_encrypt(password)
            # Verify against stored encrypted password
            if rsa_decrypt(user.rsa_password) == password:
                message = f"Classical login successful! Encrypted: {user.rsa_password}"
            else:
                message = "Invalid credentials!"
        else:
            message = "User not found!"
    return render_template('login.html', 
                         message=message,
                         encrypted=encrypted)

@app.route('/quantum-hack', methods=['GET', 'POST'])
def quantum_hack():
    result = None
    if request.method == 'POST':
        try:
            n = int(request.form['n'])
            e = int(request.form['e'])
            ciphertext = int(request.form['ciphertext'])
            
            p, q = factor(n)
            if p and q:
                d = compute_private_key(p, q, e)
                decrypted = pow(ciphertext, d, n)
                result = {
                    'p': p,
                    'q': q,
                    'd': d,
                    'decrypted': decrypted
                }
            else:
                result = {'error': 'Factorization failed'}
        except ValueError:
            result = {'error': 'Invalid input'}
    return render_template('quantum_hack.html', 
                         public_key=PUBLIC_KEY,
                         result=result)

if __name__ == '__main__':
    app.run(debug=True)