"""
methods to call neynar api
"""

# lib
import os
import requests

# src
from .models import FrameMessage, NeynarValidatedMessage, NeynarInteractor, NeynarProfile, NeynarBio, \
    NeynarButton, NeynarInput, NeynarState, NeynarTransaction


def get_frame_message(msg: str, api_key: str) -> NeynarValidatedMessage:
    if not api_key:
        raise ValueError('neynar api key not set')
    url = 'https://api.neynar.com/v2/farcaster/frame/validate'
    body = {
        'cast_reaction_context': False,  # TODO
        'follow_context': False,
        'signer_context': False,
        'message_bytes_in_hex': msg
    }
    headers = {
        'accept': 'application/json',
        'api_key': api_key,
        'content-type': 'application/json'
    }

    res = requests.post(url, json=body, headers=headers)
    if res.status_code != 200:
        raise ValueError(f'neynar error [{res.status_code}] {res.text}')

    if res.status_code != 200:
        raise ValueError(f'failed to validate message with neynar: {res.text}')
    body = res.json()
    if not body['valid']:
        raise ValueError('frame action message is invalid')

    action = NeynarValidatedMessage(**body['action'])

    return action


def validate_message(msg: FrameMessage, api_key: str) -> NeynarValidatedMessage:
    action = get_frame_message(msg.trustedData.messageBytes, api_key)

    if msg.untrustedData.fid != action.interactor.fid:
        raise ValueError(f'fid does not match: {msg.untrustedData.fid} {action.interactor.fid}')

    if msg.untrustedData.buttonIndex != action.tapped_button.index:
        raise ValueError(f'button index does not match: {msg.untrustedData.buttonIndex} {action.tapped_button.index}')

    if msg.untrustedData.inputText is not None and msg.untrustedData.inputText != action.input.text:
        raise ValueError(f'text input does not match: {msg.untrustedData.inputText} {action.input.text}')

    if msg.untrustedData.state is not None and msg.untrustedData.state != action.state.serialized:
        raise ValueError(f'state does not match: {msg.untrustedData.state} {action.state.serialized}')

    return action


def validate_message_or_mock(msg: FrameMessage, api_key: str, mock: bool = False) -> NeynarValidatedMessage:
    if mock:
        # mock
        # TODO option to populate with warpcast profile
        return NeynarValidatedMessage(
            object='validated_frame_action',
            interactor=NeynarInteractor(
                object='user',
                fid=msg.untrustedData.fid,
                username=f'username {msg.untrustedData.fid}',
                display_name=f'display name {msg.untrustedData.fid}',
                pfp_url='',
                profile=NeynarProfile(bio=NeynarBio(text='')),
                follower_count=0,
                following_count=0,
                verifications=['0x'],
                active_status='',
            ),
            tapped_button=NeynarButton(index=msg.untrustedData.buttonIndex),
            input=NeynarInput(text=msg.untrustedData.inputText or ''),  # TODO set model to None if missing
            state=NeynarState(serialized=msg.untrustedData.state or ''),
            transaction=NeynarTransaction(hash=msg.untrustedData.transactionId or ''),
            url=msg.untrustedData.url,
            timestamp=msg.untrustedData.timestamp,
            cast={}
        )

    return validate_message(msg, api_key)
