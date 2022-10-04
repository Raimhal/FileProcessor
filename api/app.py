from chalice import Chalice

from chalicelib.blueprints.events import events
from chalicelib.blueprints.auth import auth
from chalicelib.blueprints.sender import sender

from dotenv import load_dotenv
load_dotenv()

app = Chalice(app_name='api')
app.register_blueprint(auth)
app.register_blueprint(sender)
app.register_blueprint(events)

# app >> /send_file >> s3 >> sqs >> text detection >