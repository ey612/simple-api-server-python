import requests

def test_get_postman():
    
    # 테스트할 API 주소
    url = 'http://localhost:4444/users'
    
    # 서버에 GET 요청 보내기
    response = requests.get(url)
    
    # ----------------------------
    # 상태 코드 검증
    # ----------------------------

    # 3️⃣ HTTP 상태 코드 확인
    # 200이면 "요청 성공"
    
    assert response.status_code == 200, '확인 필요'
    
    # ----------------------------
    # 응답 본문(JSON) 검증
    # ----------------------------

    # 4️⃣ 서버가 준 응답을 JSON으로 변환
    # dict 형태로 변환됨
    # ⭐⭐⭐ 이 한줄이 바로 역직렬화(deserialization) 다
    data = response.json()
    print(data)

    # 5️⃣ 응답 타입 확인
    # JSON 객체인지(dict) 확인
    assert isinstance(data, dict)

    # # 6️⃣ 필수 key가 존재하는지 확인
    # assert "title" in data
    # assert "body" in data  