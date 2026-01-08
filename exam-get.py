import requests

# 요청할 URL
url = "https://jsonplaceholder.typicode.com/posts/1"

# GET 요청 보내기
response = requests.get(url)

# 응답 객체 출력 (상태코드 확인용)
print(response)          # <Response [200]>

# 상태코드만 보고 싶을 때
print(response.status_code)  # 200

# JSON 응답 내용 확인
print(response.json())
