import requests

# 요청할 기본 URL
# 아직 ?userId=1 같은 건 안 붙어 있음
url = "https://jsonplaceholder.typicode.com/comments"

# Query Parameter를 dict 형태로 정의
# key=value → userId=1
params = {
    "postId": 1
}

# GET 요청 보내기
# params에 넣은 값은 requests가 자동으로 URL 뒤에 붙여줌
response = requests.get(url, params=params)

# 실제 요청된 URL 확인
# https://jsonplaceholder.typicode.com/posts?userId=1
print(response.url)

# 응답 상태 코드 확인 (정상: 200)
print(response.status_code)

# 서버가 준 데이터(JSON)를 파이썬 객체로 변환해서 출력
print(response.json())
