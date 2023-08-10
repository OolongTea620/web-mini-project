from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bs4 import BeautifulSoup
import certifi, requests, time

app = Flask(__name__)

ca = certifi.where()

DB_URL='mongodb+srv://seungitnow:tmd123@cluster0.qg1bilm.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(DB_URL,tlsCAFile=ca)
db = client.dbseungitnow

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/home', methods=["GET"])
def return_video_list():
    # 서버 PC에서 로컬 시각 측정 후 그에 맞는 로직 실행
    hour = time.localtime(time.time()).tm_hour
    if (9 <= hour & hour <= 17):
        is_working_time = True
    else:
        is_working_time = False
    
    if (is_working_time):
        video_list = list(db.work_videos.find({}, {'_id': False}))
    else:
        video_list = list(db.rest_videos.find({}, {'_id': False}))

    return jsonify({'res_videoList': video_list})

@app.route('/home', methods=["POST"])
def add_videos():
    video_url = request.form['req_url']
    # 동영상 ID 추출 후 썸네일 주소 추출
    video_id = search_id(video_url)
    thumbnail_url = 'https://img.youtube.com/vi/%s/hqdefault.jpg'%video_id
    # 동영상 제목 크롤링
    response = requests.get(video_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.select_one('meta[itemprop="name"][content]')['content']

    doc = {
        'thumbnail_url': thumbnail_url,
        'title': title
    }

    mode = request.form['req_mode']
    if (mode == 'work'):
        db.work_videos.insert_one(doc)
    else:
        db.rest_videos.insert_one(doc)

    return jsonify({'msg': '성공!'})

# 로직 추가

def search_id(url):
    start_index = url.find('=')
    last_index = url.find('&')
    id_from_url = ''

    if last_index == -1:
        id_from_url = url[start_index + 1:]
    else:
        id_from_url = url[start_index + 1:last_index]
    
    return id_from_url

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)