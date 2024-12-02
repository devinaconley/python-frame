"""
main entry point for example framelib flask app
"""
import os
from flask import Flask, url_for, jsonify
from framelib import frame, message, validate_message_or_mock, validate_message_or_mock_neynar, error

app = Flask(__name__)


@app.errorhandler(ValueError)
def handle_invalid_usage(e):
    print(f'error: {e}')
    return error(text=str(e), status=403)


@app.route('/', methods=['GET', 'POST'])
def home():
    # initial frame
    return frame(
        image='https://framelib.s3.us-east-1.amazonaws.com/framelib_logo.png',
        aspect_ratio='1:1',
        button1='hello \U0001F44B',
        post_url=url_for('second_page', _external=True),
        button2='github',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-frames'
    )


@app.route('/page2', methods=['POST'])
def second_page():
    # parse frame message
    msg = message()
    print(f'received frame message: {msg}')

    # validate frame message with neynar
    api_key = os.getenv('NEYNAR_KEY')
    msg_neynar = validate_message_or_mock_neynar(msg, api_key, mock=_vercel_local())
    print(f'validated frame message, fid: {msg_neynar.interactor.fid}, button: {msg_neynar.tapped_button}')

    # second page frame
    return frame(
        image='https://framelib.s3.us-east-1.amazonaws.com/framelib_logo.png',
        aspect_ratio='1:1',
        button1='back \U0001F519',
        post_url=url_for('home', _external=True),
        input_text=f'hello {msg_neynar.interactor.username}!',
        button2='github',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-frames'
    )


def _vercel_local() -> bool:
    vercel_env = os.getenv('VERCEL_ENV')
    return vercel_env is None or vercel_env == 'development'
