# app.py
# 가장 심플한 파이썬 API 서버 (Flask)
# 실행하면: http://localhost:5000/ 로 접속 시 "Hello, World!" 반환

''' 
flask : 파이썬으로 웹 애플리케이션을 만들 때 사용되는 프레임 워크
간단한 코드 몇 줄만으로 서버를 띄우고 API를 만들 수 있음
'''
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# SQLite 설정
# 데이터베이스 파일 위치 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# 경고 메시지 끄기
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

#User 테이블 정의
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# 앱 실행될 때 테이블 생성
with app.app_context():
    db.create_all()

@app.post('/users')
def create_user():
    data = request.json
    
    new_user = User(
        name=data['name'],
        email=data['email']
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email
    }), 201


@app.get('/users')
def get_users():
    users = User.query.all()
    
    result = []
    for user in users:
        result.append({
        'id': user.id,
        'name': user.name,
        'email': user.email
            
        })
    return jsonify(result), 200

@app.get('/users/<int:user_id>')
def get_user(user_id):
    users = User.query.get(user_id)
    
    if users is None:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    
    return jsonify({
        'id': users.id,
        'name': users.name,
        'email': users.email
        
    }),200
    
@app.get('/users/email/<email>')
def get_user_by_email(email):
    users = User.query.filter_by(email=email).first()
    
    if users is None:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    
    
    return jsonify({
        'id': users.id,
        'name': users.name,
        'email': users.email
        
    }),200

if __name__ == '__main__':
    app.run(debug=True)
