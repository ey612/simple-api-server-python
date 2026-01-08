import pytest
import requests


@pytest.mark.parametrize(
    "input1, input2, expected",
    [
        (1, 2, 3),
        (5, 5, 10),
        (-1, 1, 0),
    ]
)
def test_addition(input1, input2, expected):
    assert input1 + input2 == expected


@pytest.fixture(scope="session")
def base_url():
    return "https://jsonplaceholder.typicode.com"


@pytest.mark.parametrize(
    "post_id, expected_user_id",
    [
        (1, 1),
        (2, 1),
        (11, 2),
    ]
)
def test_get_post_check_userid(base_url, post_id, expected_user_id):
    response = requests.get(f"{base_url}/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == expected_user_id


@pytest.mark.parametrize(
    "post_payload, expected_status_code, expected_title",
    [
        (
            {
                "title": "My First Post",
                "body": "This is the content.",
                "userId": 1,
            },
            201,
            "My First Post",
        ),
        (
            {
                "title": "Another Test",
                "body": "More content here.",
                "userId": 5,
            },
            201,
            "Another Test",
        ),
    ]
)
def test_create_post_with_data(
    base_url,
    post_payload,
    expected_status_code,
    expected_title,
):
    response = requests.post(
        f"{base_url}/posts",
        json=post_payload
    )

    assert response.status_code == expected_status_code

    if response.status_code == 201:
        response_json = response.json()
        assert response_json["title"] == expected_title
        assert response_json["body"] == post_payload["body"]
        assert response_json["userId"] == post_payload["userId"]
        assert "id" in response_json
