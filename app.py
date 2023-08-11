from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bs4 import BeautifulSoup
import certifi
import requests
import jwt
import datetime
import hashlib
import re

app = Flask(__name__)
ca = certifi.where()
client = MongoClient('mongodb+srv://seungitnow:tmd123@cluster0.xyzecw1.mongodb.net/?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbseungitnow
SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth')
def token_received_home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        return render_template('index.html')
    
@app.route('/video',methods=["GET"])
def video_page():
    return render_template('write.html')

@app.route('/home', methods=["GET"])
def return_video_list():
    mode = request.args['mode']

    if (mode == 'work'):
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
        'tag': tag_list,
        'video_id' : video_id
    }

    mode = request.form['req_mode']
    if (mode == 'work'):
        db.work_videos.insert_one(doc)
    else:
        db.rest_videos.insert_one(doc)

    return jsonify({'msg': '동영상 추가 성공!'})

@app.route('/insert/video/', methods=["GET"])
def insert_render():
    return render_template('temp.html')

def search_id(url):
    id_from_url = ''

    if url:
        regex = re.compile(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*')
        matches = regex.match(url)
    if matches:
        id_from_url += matches.group(7)
    return id_from_url

def get_nick_by_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    nick = payload['nick']
    return nick

@app.route('/video/insert', methods=["POST"])
def video_insert() :
    
    video_url = request.form["video_url"]
    mode_name = request.form['mode']
    tags = request.form['tags']
    
    video_id = search_id(video_url)
    thumbnail_url= f'https://img.youtube.com/vi/{video_id}/mqdefault.jpg'
    # nick = get_nick_by_token(request.cookies.get('mytoken'))
    
    doc = {
        "thumbnail_url" : thumbnail_url,
	 	"title" : "this is title",
	 	"tags" : list(tags.split(",")),
	 	"video_id" : video_id,
        # "writer" : nick  
    }
    
    if (mode_name == "rest") :
        db.rest_videos.insert_one(doc)
    else :
        db.work_videos.insert_one(doc)
    return jsonify({"result": "ok"})
    
## 승일님과 겹칠수도    

@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nickname_receive = request.form['nickname_give']

    id_check = db.user.find_one({'id': id_receive})

    if id_check is None:
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nickname_receive})

        return jsonify({'result': 'success'})
    
    else:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디가 존재합니다.'})

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/api/nick', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})


def search_id(url):
    id_from_url = ''

    if url:
        regex = re.compile(r'^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#\&\?]*).*')
        matches = regex.match(url)
        if matches:
            id_from_url += matches.group(7)
    return id_from_url

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)