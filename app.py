from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)

ca = certifi.where()

import time

DB_URL='mongodb+srv://seungitnow:tmd123@cluster0.qg1bilm.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(DB_URL,tlsCAFile=ca)
db = client.dbseungitnow

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home', methods=["GET"])
def return_videos():
    hour = time.localtime(time.time()).tm_hour
    if (9 <= hour & hour <= 17):
        is_working_time = True
    else:
        is_working_time = False
    
    if (is_working_time):
        movie_list = list(db.work_videos.find({}, {'_id': False}))
    else:
        movie_list = list(db.rest_videos.find({}, {'_id': False}))

    return jsonify({'videos': movie_list})

# 로직 추가

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)