from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)

ca = certifi.where()

DB_URL='mongodb+srv://sparta:test@cluster0.gbxhkwc.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(DB_URL,tlsCAFile=ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video',methods=["GET"])
def video_page():
    return render_template('form.html')


# 로직 추가

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)