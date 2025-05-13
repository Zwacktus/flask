from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Daten speichern
def save_transaction(amount):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER,
            timestamp TEXT
        )
    """)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO transactions (amount, timestamp) VALUES (?, ?)", (amount, timestamp))
    
    conn.commit()
    conn.close()

@app.route("/save_transaction", methods=["POST"])
def receive_transaction():
    data = request.json
    amount = data.get("amount")
    if amount:
        save_transaction(amount)
        return jsonify({"message": "Transaction saved!"}), 200
    return jsonify({"error": "Invalid request"}), 400

@app.route("/transactions", methods=["GET"])
def show_transactions():
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()
    conn.close()

    return jsonify([{"id": row[0], "amount": row[1], "timestamp": row[2]} for row in data])

if __name__ == "__main__":
    app.run(port=8000)
