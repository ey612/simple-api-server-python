import requests

# 요청할 URL
url = "https://jsonplaceholder.typicode.com/posts"

# 서버로 보낼 데이터 (payload)
# payload = {
#     "title": "foo",
#     "body": "bar",
#     "userId": 1
# }

sports = {
    "title": "Archery",
    "body": "양궁",
    "userId": 1
}

# POST 요청 (json=payload → 자동으로 JSON 변환 + Content-Type 설정)
response = requests.post(url, json=sports)

# 응답 상태 코드 출력
print(response.status_code)   # 201

# 서버가 돌려준 JSON 데이터 출력
print(response.json())        # 생성된 데이터 정보
