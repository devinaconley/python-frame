"""
main entry point for example framelib flask app
"""
import os
import time
from io import BytesIO

from flask import Flask, url_for, jsonify, request, make_response
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

from framelib import (
    frame,
    message,
    signature,
    validate_message_or_mock,
    validate_message_or_mock_neynar,
    error,
    Address
)

app = Flask(__name__)


@app.errorhandler(ValueError)
def handle_invalid_usage(e):
    print(f'error: {e}')
    return error(text=str(e), status=403)


@app.route('/', methods=['GET', 'POST'])
def page_home():
    # initial frame
    return frame(
        image=url_for(
            'render_image',
            title='framelib',
            msg='lightweight library for building farcaster frames\nin python\n\nby @conley',
            _external=True
        ),
        button1='hello \U0001F44B',
        post_url=url_for('page_hello', _external=True),
        button2='github',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-framelib'
    )


@app.route('/hello', methods=['POST'])
def page_hello():
    # parse frame message
    msg = message()
    print(f'received frame message: {msg}')

    # check input
    if msg.untrustedData.buttonIndex == 2:
        print('invalid button input')
        return error('wrong button!')  # popup message to user

    # validate frame message with neynar
    api_key = os.getenv('NEYNAR_KEY')
    msg_neynar = validate_message_or_mock_neynar(msg, api_key, mock=_vercel_local())
    print(f'validated frame message, fid: {msg_neynar.interactor.fid}, button: {msg_neynar.tapped_button}')

    # validate frame message with hub (alternative)
    # msg_hub = validate_message_or_mock(msg, 'https://nemes.farcaster.xyz:2281', mock=_vercel_local())
    # print(f'validated frame message hub, fid: {msg_hub.data.fid}, button: {msg_hub.data.frameActionBody.buttonIndex}')

    return frame(
        image=url_for('render_image', title='hello', msg=f'hello {msg_neynar.interactor.username}!', _external=True),
        button1='\U00002B05 home ',
        post_url=url_for('page_home', _external=True),
        button2='signature \U000027A1',
        button2_target=url_for('page_signature', _external=True)
    )


@app.route('/signature', methods=['POST'])
def page_signature():
    # parse and validate frame message
    api_key = os.getenv('NEYNAR_KEY')
    msg = validate_message_or_mock_neynar(message(), api_key, mock=_vercel_local())
    print(f'verified frame message: {msg}')

    return frame(
        image=url_for('render_image', title='signature', msg=f'sign an eip-712 message!', _external=True),
        button1='hello \U0001F519',
        button1_target=url_for('page_hello', _external=True),
        post_url=url_for('handle_signature', _external=True),
        input_text=f'enter a message to sign',
        button2='\U00002712',
        button2_action='tx',
        button2_target=url_for('handle_signature', _external=True),
        button3='puzzle \U000027A1',
        button3_target=url_for('page_puzzle', _external=True)
    )


class User(BaseModel):
    name: str
    address: Address


class Message(BaseModel):
    timestamp: int
    user: User
    text: str


@app.route('/signature/target', methods=['POST'])
def handle_signature():
    msg = message()
    print(msg)

    if msg.untrustedData.transactionId is not None:
        sig = msg.untrustedData.transactionId
        print(f'received eip-712 signature: {sig}')
        # note: verify signature here

        return frame(
            image=url_for('render_image', title='signature', msg='thanks for signing.', _external=True),
            button1='hello \U0001F519',
            button1_target=url_for('page_hello', _external=True),
            post_url=url_for('handle_signature', _external=True),
            button2='puzzle \U000027A1',
            button2_target=url_for('page_puzzle', _external=True)
        )

    api_key = os.getenv('NEYNAR_KEY')
    msg_neynar = validate_message_or_mock_neynar(msg, api_key, mock=_vercel_local())

    # setup eip-712 signature
    payload = Message(
        timestamp=int(time.time()),
        user=User(
            name=msg_neynar.interactor.username,
            address=msg.untrustedData.address),
        text=msg.untrustedData.inputText
    )
    return signature(8453, payload, domain='playground', version='v1')


@app.route('/puzzle', methods=['POST'])
def page_puzzle():
    # parse frame message
    msg = message()
    print(f'received frame message: {msg}')

    # check input
    if msg.untrustedData.inputText:
        if msg.untrustedData.inputText.lower() != 'build':
            return error('secret is incorrect!')  # popup message to user
        else:
            return frame(
                image=url_for('render_image', title='puzzle', msg='[the secret is build]', _external=True),
                button1='signature \U0001F519',
                post_url=url_for('page_signature', _external=True),
                button2='links \U000027A1',
                button2_target=url_for('page_link', _external=True)
            )

    return frame(
        image=url_for('render_image', title='puzzle', msg='20 8 5 19 5 3 18 5 20 9 19 2 21 9 12 4', _external=True),
        button1='signature \U0001F519',
        button1_target=url_for('page_signature', _external=True),
        post_url=url_for('page_puzzle', _external=True),
        input_text=f'enter the secret',
        button2='\U0001F512',
        button3='links \U000027A1',
        button3_target=url_for('page_link', _external=True)
    )


@app.route('/link', methods=['POST'])
def page_link():
    return frame(
        image=_github_preview_image(),
        button1='puzzle \U0001F519',
        post_url=url_for('page_puzzle', _external=True),
        button2='github \U0001F680',
        button2_action='link',
        button2_target='https://github.com/devinaconley/python-framelib'
    )


@app.route('/image')
def render_image():
    title = request.args.get('title', default='')
    msg = request.args.get('msg', default='')

    # setup image background
    image = Image.new('RGB', (764, 400), color=(211, 211, 211))
    draw = ImageDraw.Draw(image)

    # write text
    font = ImageFont.truetype('DejaVuSansMono-Bold.ttf', 36)
    draw.text((10, 10), title, fill=(0, 0, 0), font=font)
    y = 80
    for m in msg.split('\n'):
        font = ImageFont.truetype('DejaVuSansMono.ttf', 20)
        draw.text((10, y), m, fill=(0, 0, 0), font=font)
        y += 25

    # encode image response
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    png_image_bytes = buffer.getvalue()
    buffer.close()

    res = make_response(png_image_bytes)
    res.headers.set('Content-Type', 'image/png')
    return res


def _github_preview_image() -> str:
    hour = int((time.time() // 3600) * 3600)  # github throttles if you invalidate image cache too much
    return f'https://opengraph.githubassets.com/{hour}/devinaconley/python-frames'


def _vercel_local() -> bool:
    vercel_env = os.getenv('VERCEL_ENV')
    return vercel_env is None or vercel_env == 'development'
