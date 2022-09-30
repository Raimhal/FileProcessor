import json

from chalice.test import Client

from app import app


def test_send_file():
    with Client(app) as client:
        response = client.http.post(
            '/send_file',
            headers={'Content-Type': 'application/json'},
            body=json.dumps(
                {
                    "fileUrl": "https://www.befunky.com/images/wp/wp-2018-05-Add-Text-To-Photos-37.jpg?auto=avif,webp&format=jpg&width=1150&crop=16:9"
                })
        )
        assert response.status_code == 200
        assert response.json_body is None
