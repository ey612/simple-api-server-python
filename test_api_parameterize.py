# 이 파일 하나로 설명 가능한 것:
# 1) pytest.mark.parametrize 기본 개념
# 2) 같은 테스트를 여러 데이터로 반복 실행하는 방법
# 3) API GET / POST 테스트에 parameterize 적용하는 방법

import pytest
import requests


# =========================================
# 1️⃣ parameterize 가장 기본 예제 (API 아님)
# =========================================
# 목적:
# - parameterize 문법 자체를 이해하기
#
# 의미:
# - test_addition 함수가
#   아래 데이터 개수만큼 "자동 반복 실행"됨
@pytest.mark.parametrize(
    "input1, input2, expected",
    [
        (1, 2, 3),     # 첫 번째 테스트 실행
        (5, 5, 10),    # 두 번째 테스트 실행
        (-1, 1, 0),    # 세 번째 테스트 실행
    ]
)
def test_addition(input1, input2, expected):
    # 같은 테스트 로직을
    # 입력값만 바꿔서 여러 번 실행
    assert input1 + input2 == expected


# =========================================
# 2️⃣ API 테스트용 base_url Fixture
# =========================================
# 여러 API 테스트에서 공통으로 쓰는 URL
@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


# =========================================
# 3️⃣ parameterize + GET API 테스트
# =========================================
# 목적:
# - 게시글 ID를 여러 개 바꿔가며 GET 요청 테스트
# - 응답의 userId가 기대값과 같은지 검증
#
# 이 테스트는 아래 데이터 개수만큼 반복 실행됨
@pytest.mark.parametrize(
    "post_id, expected_user_id",
    [
        (1, 1),    # post_id=1 → userId=1 기대
        (2, 1),    # post_id=2 → userId=1 기대
        (11, 2),   # post_id=11 → userId=2 기대
    ]
)
def test_get_post_check_userid(base_url, post_id, expected_user_id):

    # GET 요청 보내기
    response = requests.get(f"{base_url}/posts/{post_id}")

    # 상태 코드 검증
    assert response.status_code == 200

    # JSON 응답 파싱 (역직렬화)
    data = response.json()

    # 핵심 값 검증
    assert data["userId"] == expected_user_id


# =========================================
# 4️⃣ parameterize + POST API 테스트
# =========================================
# 목적:
# - 다양한 입력 데이터로 POST 요청 테스트
# - 상태 코드와 응답 내용을 함께 검증
#
# post_payload:
#   서버로 보낼 JSON 데이터
# expected_status_code:
#   기대하는 HTTP 상태 코드
# expected_title:
#   응답에 포함될 title 값
@pytest.mark.parametrize(
    "post_payload, expected_status_code, expected_title",
    [
        # 테스트 케이스 1: 정상 데이터
        (
            {
                "title": "My First Post",
                "body": "This is the content.",
                "userId": 1,
            },
            201,
            "My First Post",
        ),

        # 테스트 케이스 2: 또 다른 정상 데이터
        (
            {
                "title": "Another Test",
                "body": "More content here.",
                "userId": 5,
            },
            201,
            "Another Test",
        ),

        # 필요하면 여기 아래에
        # - 빈 값
        # - 잘못된 타입
        # 같은 케이스도 계속 추가 가능
    ]
)
def test_create_post_with_data(
    base_url,
    post_payload,
    expected_status_code,
    expected_title,
):
    """
    다양한 데이터로 POST 요청을 보내고
    응답이 기대한 대로 오는지 검증한다
    """

    # POST 요청 보내기
    response = requests.post(
        f"{base_url}/posts",
        json=post_payload
    )

    # 1️⃣ 상태 코드 검증
    assert response.status_code == expected_status_code

    # 2️⃣ 정상 생성(201)인 경우에만
    # 응답 Body 추가 검증
    if response.status_code == 201:
        response_json = response.json()

        # 서버가 돌려준 값 검증
        assert response_json["title"] == expected_title
        assert response_json["body"] == post_payload["body"]
        assert response_json["userId"] == post_payload["userId"]

        # 서버가 자동 생성한 id 존재 여부 확인
        assert "id" in response_json
