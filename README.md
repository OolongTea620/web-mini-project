# web-mini-project
웹 미니 프로젝트

### requirements.txt를 이용해서 pip dependency 내려받기


python version : 3.8.6
pip version : 20.2.1

```
python --verion

pip --version
```

❗ 반드시 venv 실행된 상태에서 실행!!!

```
$ pip install -r requirements.txt
```

### 주요 Denpendency 설명

```
Flask==2.3.2 -- 웹서버 프레임워크
pymongo==4.4.1 -- mongoDB 다루기용
dnspython==2.4.1 -- mongoDB 다루기용2
certifi==2023.7.22 -- mongoDB url 접속을 위한 추가 dependency
requests==2.31.0 -- 다른 서버와 통신, 응답을 위한 기능
```