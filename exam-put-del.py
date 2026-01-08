import requests

# ------------------------------
# PUT (게시글 ID 1 업데이트)
# ------------------------------
put_url = "https://jsonplaceholder.typicode.com/posts/1"

update_data = {
    "id": 1,
    "userId": 1,
    "title": "간단하게 수정된 제목",
    "body": "간단하게 수정된 내용"
}

# PUT 요청
put_response = requests.put(put_url, json=update_data)

# PUT 결과 출력
print(
    f"PUT Status: {put_response.status_code}, "
    f"Updated Title: {put_response.json().get('title')}"
)

# ------------------------------
# DELETE (게시글 ID 1 삭제)
# ------------------------------
delete_url = "https://jsonplaceholder.typicode.com/posts/1"

# DELETE 요청
delete_response = requests.delete(delete_url)

# DELETE 결과 출력
print(f"DELETE Status: {delete_response.status_code}")  # 성공 시 200
