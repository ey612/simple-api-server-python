import pytest
import requests


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


@pytest.fixture
def sample_post_payload():
    return {
        "title": "My Test Post",
        "body": "This is the body of the test post.",
        "userId": 1
    }


@pytest.fixture
def created_post(base_url, sample_post_payload):
    create_url = f"{base_url}/posts"
    response = requests.post(create_url, json=sample_post_payload)
    assert response.status_code == 201

    created_data = response.json()
    print(f"\n[Setup] Created post ID: {created_data['id']}")

    yield created_data

    post_id = created_data["id"]
    delete_url = f"{base_url}/posts/{post_id}"
    del_response = requests.delete(delete_url)
    print(
        f"[Teardown] Deleted post ID: {post_id}, "
        f"Status: {del_response.status_code}"
    )


def test_get_created_post(base_url, created_post):
    post_id = created_post["id"]
    get_url = f"{base_url}/posts/{post_id}"
    response = requests.get(get_url)

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)
    assert "id" in data
    assert "title" in data
    assert "body" in data
    assert "userId" in data
    assert data["title"]
    assert data["body"]
