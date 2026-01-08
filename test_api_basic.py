# test_api_basic.py
# pytest + requests 를 이용한 가장 기본적인 API 테스트 예제

import requests

def test_get_post_by_id():
    """
    이 테스트는
    - 특정 게시글을 조회하는 API를 호출하고
    - 응답이 정상인지
    - 응답 내용이 우리가 기대한 형태인지
    를 검증한다
    """

    # 1️⃣ 테스트할 API 주소
    # posts/1 → id가 1인 게시글 조회
    url = "https://jsonplaceholder.typicode.com/posts/1"

    # 2️⃣ 서버에 GET 요청 보내기
    response = requests.get(url)

    # ----------------------------
    # 상태 코드 검증
    # ----------------------------

    # 3️⃣ HTTP 상태 코드 확인
    # 200이면 "요청 성공"
    assert response.status_code == 200

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

    # 6️⃣ 필수 key가 존재하는지 확인
    assert "id" in data
    assert "userId" in data
    assert "title" in data
    assert "body" in data

    # 7️⃣ 값 검증 (기대값과 비교)
    assert data["id"] == 1
    assert data["userId"] == 1

    # 8️⃣ 값이 비어있지 않은지 확인
    # None 이거나 빈 문자열이면 실패
    assert data["title"]
