# app.py
# 가장 심플한 파이썬 API 서버 (Flask)
# 실행하면: http://localhost:5000/ 로 접속 시 "Hello, World!" 반환

''' 
flask : 파이썬으로 웹 애플리케이션을 만들 때 사용되는 프레임 워크
간단한 코드 몇 줄만으로 서버를 띄우고 API를 만들 수 있음
'''
from flask import Flask, jsonify, request, make_response
import json
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
#TODO : @app.route('/hello', methods = ['GET']) 차이 ?

@app.get("/")
def hello():
    return "Hello, World!"

#회원가입 

@app.route('/sign-up', methods=['POST'])
def sign_up():
    user = request.json
    response = {
        'name': user['name'],
        'password': user['password']
    }
    return jsonify(response), 200

# 게시글 등록
@app.post('/posts')
def post_posts():
    posts = request.json
    response = {
        'title': posts['title'],
        'body': posts['body']
    }
    return jsonify(response), 201

# 댓글 등록 (다른 방법으로도 post 가능)
@app.post('/comments')
def post_comments():
    comment = request.json
    response_data = {
        'message' : '댓글이 정상적으로 등록되었습니다.',
        'comment': comment.get('comment','제목 없음')
    }
    # return jsonify(response), 201
        
    # 직접 Response 객체 만들기
    response = make_response(
        json.dumps(response_data, ensure_ascii=False),
        201
    )
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response


# if __name__ == "__main__":
#     # host=0.0.0.0 : 외부(다른 PC/컨테이너)에서도 접근 가능하게 열고 싶을 때
#     # 로컬에서만이면 기본값(127.0.0.1) 써도 됨
#     app.run(host="0.0.0.0", port=5000, debug=True)