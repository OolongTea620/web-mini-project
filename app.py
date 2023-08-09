from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)

ca = certifi.where()

DB_URL=''
client = MongoClient(DB_URL,tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


# 로직 추가

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)