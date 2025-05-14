# Quantum vs Classical Cryptography Simulation

This project is a simplified simulation of both classical and quantum-safe encryption methods. It demonstrates how classical RSA encryption can be broken using basic factoring (simulating a quantum attack), and how a quantum-safe method based on Learning With Errors (LWE) resists such attacks.

The simulation is built with **Python**, **Flask**, and **NumPy**, and is designed for educational purposes. It runs entirely on a standard laptop—no quantum hardware is required.

---

## 🔐 Features

- **RSA Login Simulation**: Passwords are encrypted using RSA and stored in a SQLite database.
- **Quantum Hack Demo**: Simulates factoring of a small RSA modulus to mimic Shor’s algorithm.
- **Quantum-Safe Login (LWE)**: Uses a simplified LWE encryption model to secure passwords against quantum threats.
- **Web Interface**: Flask-based frontend with separate pages for RSA login, quantum hacking, and LWE-based login/register.

---

## 📁 Project Structure

```
├── app.py                      # Main Flask application with all routes
├── classical_app.py           # Standalone classical RSA login demo (optional)
├── quantum_hack.py            # Simulates factoring for quantum attack demo
├── templates/
│   ├── register.html          # Classical RSA register page
│   ├── login.html             # Classical RSA login page
│   ├── pq_register.html       # LWE-based register page
│   ├── pq_login.html          # LWE-based login page
│   ├── quantum_hack.html      # Quantum hacking demo interface
├── users.db                   # SQLite database (auto-created on first run)
└── README.md                  # This file
```

---

## ▶️ How to Run the Simulation

### 1. **Install Dependencies**

Make sure you have Python 3 installed. Then, in your terminal, run:

```bash
pip install flask numpy
```

### 2. **Start the Web App**

Run the app with:

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 💡 How It Works

### 🔒 Classical Login (RSA)
- User registers with a username and numeric password.
- The password is encrypted using a small RSA public key.
- On login, it decrypts the stored value and compares it to the input.

### ⚡ Quantum Hack Simulation
- Mimics Shor’s algorithm by factoring a small RSA modulus (e.g., n = 3233) using classical trial division.
- Recovers RSA private key and decrypts the password.
- Demonstrates how classical RSA becomes vulnerable in a quantum context.

### 🛡️ Quantum-Safe Login (LWE)
- Uses a randomly generated matrix \( A \) and secret vector \( s \) to compute \( b = A \cdot s \mod q \).
- The password is embedded into this structure.
- Without knowing the secret vector, the password cannot be recovered.

---

## 🧪 What You Can Learn

- How RSA works and why it is vulnerable to quantum attacks.
- What Quantum Key Distribution and LWE are, and why they are secure.
- How post-quantum cryptographic models operate differently from classical ones.

---

## 📌 Notes

- This is an educational project — do not use it for real security purposes.
- The RSA keys used are small and insecure by design.
- The LWE implementation is simplified for demonstration and does not include a full decryption path.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 🙋‍♂️ Author

**Prathamesh Bharat Kalantri**  
M.S. in Computer Science  
California State University, Chico
