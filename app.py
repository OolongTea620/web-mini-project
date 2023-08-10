from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bs4 import BeautifulSoup
import certifi, requests

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
    mode = request.args['mode']

    if (mode == 'work'):
        video_list = list(db.work_videosss.find({}, {'_id': False}))
    else:
        video_list = list(db.rest_videosss.find({}, {'_id': False}))

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
    # 태그 1차 가공 : 구분
    tag_text = request.form['req_tag']
    tags = tag_text.split(';')
    # 태그 2차 가공 : 공백 제거
    tag_list = []
    for tag in tags:
        new_tag = tag.replace(" ", "")
        tag_list.append(new_tag)
    
    tag_list.pop()

    doc = {
        'thumbnail_url': thumbnail_url,
        'title': title,
        'tag': tag_list
    }

    mode = request.form['req_mode']
    if (mode == 'work'):
        db.work_videosss.insert_one(doc)
    else:
        db.rest_videosss.insert_one(doc)

    return jsonify({'msg': '동영상 추가 성공!'})

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