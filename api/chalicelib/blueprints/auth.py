from chalice import Blueprint

from chalicelib.services.cognito_service import sign_in, sign_up, confirm_sign_up

auth = Blueprint(__name__)


@auth.route('/auth', methods=['POST'])
def authorize():
    return sign_in(auth.current_request.json_body)


@auth.route('/sign-up', methods=['POST'])
def sing_up():
    return sign_up(auth.current_request.json_body)


@auth.route('/confirm-sign-up', methods=['POST'])
def confirm_sing_up():
    return confirm_sign_up(auth.current_request.json_body)