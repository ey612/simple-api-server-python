# test_api_with_fixture.py
# pytest + requests + fixture 예제
# 목적:
# - fixture가 뭔지
# - 왜 쓰는지
# - setup / teardown이 어떻게 되는지
# 를 한 번에 이해하기

import pytest
import requests


# ================================
# 1️⃣ base_url Fixture
# ================================
# fixture란?
# → 테스트에서 공통으로 쓰는 "준비물"을 미리 만들어주는 함수
#
# 이 fixture는
# - API의 기본 URL을 제공함
# - scope="session" 이므로
#   pytest 전체 실행 동안 딱 1번만 만들어짐
@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


# ================================
# 2️⃣ sample_post_payload Fixture
# ================================
# 테스트용으로 사용할 "게시글 데이터"
# 매번 테스트 함수에서 dict를 직접 만들기 귀찮으니까
# fixture로 빼놓은 것
@pytest.fixture
def sample_post_payload():
    return {
        "title": "My Test Post",
        "body": "This is the body of the test post.",
        "userId": 1
    }


# ================================
# 3️⃣ created_post Fixture (Setup + Teardown)
# ================================
# 이 fixture는 조금 고급 개념
#
# 하는 일:
# - Setup 단계: 게시글 생성 (POST)
# - 테스트에 생성된 데이터 전달
# - Teardown 단계: 테스트 끝나면 게시글 삭제 (DELETE)
#
# yield 기준:
# - yield 이전 → Setup
# - yield 이후 → Teardown
@pytest.fixture
def created_post(base_url, sample_post_payload):

    # ---------- Setup ----------
    # 테스트 전에 게시글 생성
    create_url = f"{base_url}/posts"

    response = requests.post(create_url, json=sample_post_payload)

    # 게시글 생성 성공 여부 확인
    assert response.status_code == 201

    # 생성된 게시글 데이터(JSON → dict)
    created_data = response.json()

    print(f"\n[Setup] Created post ID: {created_data['id']}")

    
    # teardown안할거면 아래 주석 풀어서 그냥 return으로 끝내면 됨
    # return created_data
    yield created_data
    # yield:
    # 이 값을 테스트 함수로 넘겨줌

    # ---------- Teardown ----------
    # 테스트가 끝난 뒤 자동 실행
    post_id = created_data["id"]
    delete_url = f"{base_url}/posts/{post_id}"

    del_response = requests.delete(delete_url)

    print(
        f"[Teardown] Deleted post ID: {post_id}, "
        f"Status: {del_response.status_code}"
    )

    # 실제 서비스라면 아래처럼 검증 가능
    # assert del_response.status_code == 200


# ================================
# 4️⃣ 실제 테스트 함수
# ================================
# created_post fixture를 매개변수로 받으면
# pytest가 알아서:
# - fixture 실행
# - yield 값 주입
# - 테스트 종료 후 teardown 실행
def test_get_created_post(base_url, created_post):

    # fixture에서 넘겨받은 게시글 ID
    post_id = created_post["id"]

    # 조회 API URL
    get_url = f"{base_url}/posts/{post_id}"
    # 하드코딩된 이유 설명 ✅✅⭐⭐ 현재 base_url 기준으로 해당 요청은 mock을 뱉고 있기 때문
    # get_url = f"{base_url}/posts/100"

    # GET 요청
    response = requests.get(get_url)

    # 상태 코드 검증
    
    
    assert response.status_code == 200
    # 지금 우리가 쓰는 json홀더place의 api res가 post요청시 mock으로 postId를 뱉고 있어서
    # 실제로 그 postId로 조회하면 404가 뜨고 있음.
    #
    # assert response.status_code == 404

    # 응답 JSON 파싱 (역직렬화)
    data = response.json()

    # ----------------------------
    # 응답 검증
    # ----------------------------

    # 타입 확인
    assert isinstance(data, dict)

    # key 존재 여부
    assert "id" in data
    assert "title" in data
    assert "body" in data
    assert "userId" in data

    # 값이 비어있지 않은지 확인
    assert data["title"]
    assert data["body"]
