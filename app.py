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

@app.route('/video/<string:mode>')
def mode_type_render(mode):
    mode_name = "빈둥" if mode == "rest" else "일"
    return render_template('videos.html', mode_name=mode_name)

@app.route('/video/insert', methods=["POST"])
def video_insert() :
    video_receive = request.form['video_give']

    doc = {
        
    }
    

# @app.route("/bucket", methods=["POST"])
# def bucket_post():
#     bucket_receive = request.form['bucket_give']
    
#     bucket_list = list(db.bucket.find({}, {'_id': False}))
#     count = len(bucket_list) + 1
#     doc = {
#         'num': count,
#         'bucket' :bucket_receive,
#         'done' : 0 
#     }
#     db.bucket.insert_one(doc)

#     return jsonify({'result': '✉ 버킷 저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)