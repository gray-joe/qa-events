from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# PostgreSQL database configuration
db_conn = psycopg2.connect(
    database="events",
    user="user",
    password="password",
    host="db"
)

@app.route('/github', methods=['POST'])
def github_webhook():
    data = request.get_json()
    json_data = jsonify(data).data
    timestamp = datetime.utcnow()

    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO github (timestamp, data) VALUES (%s, %s)", (timestamp, json_data))
    db_conn.commit()
    cursor.close()

    return "Webhook received and processed", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
