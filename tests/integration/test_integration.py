import json

import pytest
from chalice.test import Client

import app

def test_send_file():
    with Client(app.app) as client:
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

#
# code below will work if the problems with decorator 'on_sqs_message' will be fixed
#

def test_handle_sqs_message():
    with Client(app.app) as client:
        event = client.events.generate_sqs_event(message_bodies=[json.dumps(
                {
                    "fileUrl": "https://www.befunky.com/images/wp/wp-2018-05-Add-Text-To-Photos-37.jpg?auto=avif,webp&format=jpg&width=1150&crop=16:9"
                })],
            queue_name='test-queue'
        )
        response = client.lambda_.invoke('handle_sqs_message', event)
        assert response.payload is None