import json

from chalice.test import Client

#
# code below will work if the problems with decorator 'on_sqs_message' will be fixed
#
from api.app import app


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


def test_handle_sqs_detections():
    with Client(app.app) as client:
        event = client.events.generate_sqs_event(message_bodies=[json.dumps(
            [
                {
                    "Confidence": 90.54900360107422,
                    "DetectedText": "IT'S",
                    "Id": 0,
                    "Type": "LINE"
                },
                {
                    "Confidence": 59.411651611328125,
                    "DetectedText": "I",
                    "Id": 1,
                    "Type": "LINE"
                },
                {
                    "Confidence": 92.76634979248047,
                    "DetectedText": "MONDAY",
                    "Id": 2,
                    "Type": "LINE"
                },
                {
                    "Confidence": 96.7636489868164,
                    "DetectedText": "but keep",
                    "Id": 3,
                    "Type": "LINE"
                },
                {
                    "Confidence": 99.47185516357422,
                    "DetectedText": "Smiling",
                    "Id": 4,
                    "Type": "LINE"
                },
                {
                    "Confidence": 90.54900360107422,
                    "DetectedText": "IT'S",
                    "Id": 5,
                    "ParentId": 0,
                    "Type": "WORD"
                },
                {
                    "Confidence": 92.76634979248047,
                    "DetectedText": "MONDAY",
                    "Id": 7,
                    "ParentId": 2,
                    "Type": "WORD"
                },
                {
                    "Confidence": 59.411651611328125,
                    "DetectedText": "I",
                    "Id": 6,
                    "ParentId": 1,
                    "Type": "WORD"
                },
                {
                    "Confidence": 95.33189392089844,
                    "DetectedText": "but",
                    "Id": 8,
                    "ParentId": 3,
                    "Type": "WORD"
                },
                {
                    "Confidence": 98.1954116821289,
                    "DetectedText": "keep",
                    "Id": 9,
                    "ParentId": 3,
                    "Type": "WORD"
                },
                {
                    "Confidence": 99.47185516357422,
                    "DetectedText": "Smiling",
                    "Id": 10,
                    "ParentId": 4,
                    "Type": "WORD"
                }
            ]
        )],
            queue_name='test-response-queue'
        )
        response = client.lambda_.invoke('handle_sqs_detections', event)
        assert response.payload is None