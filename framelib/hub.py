"""
methods to interact with farcaster hub
"""

# lib
import os
import requests

# src
from .models import FrameMessage, ValidatedMessage, ValidatedData, FrameAction, CastId


def get_message(
        msg: str,
        hub: str,
        username: str = None,
        password: str = None,
        api_key: str = None
) -> ValidatedMessage:
    url = f'{hub}/v1/validateMessage'
    headers = {'content-type': 'application/octet-stream'}
    if api_key:
        headers['api_key'] = api_key
    auth = None
    if username:
        auth = (username, password)

    res = requests.post(url, headers=headers, auth=auth, data=bytes.fromhex(msg))
    if res.status_code != 200:
        raise ValueError(f'hub error [{res.status_code}] {res.text}')

    if res.status_code != 200:
        raise ValueError(f'failed to validate message with hub: {res.text}')
    body = res.json()
    if not body['valid']:
        raise ValueError('frame action message is invalid')

    action = ValidatedMessage(**body['message'])

    return action


def validate_message(
        msg: FrameMessage,
        hub: str,
        username: str = None,
        password: str = None,
        api_key: str = None
) -> ValidatedMessage:
    action = get_message(msg.trustedData.messageBytes, hub, username=username, password=password, api_key=api_key)

    if msg.untrustedData.fid != action.data.fid:
        raise ValueError(f'fid does not match: {msg.untrustedData.fid} {action.data.fid}')

    if msg.untrustedData.buttonIndex != action.data.frameActionBody.buttonIndex:
        raise ValueError(
            f'button index does not match: {msg.untrustedData.buttonIndex} {action.data.frameActionBody.buttonIndex}')

    if msg.untrustedData.inputText is not None and msg.untrustedData.inputText != action.data.frameActionBody.inputText:
        raise ValueError(
            f'text input does not match: {msg.untrustedData.inputText} {action.data.frameActionBody.inputText}')

    if msg.untrustedData.state is not None and msg.untrustedData.state != action.data.frameActionBody.state:
        raise ValueError(f'state does not match: {msg.untrustedData.state} {action.data.frameActionBody.state}')

    return action


def validate_message_or_mock(
        msg: FrameMessage,
        hub: str,
        username: str = None,
        password: str = None,
        api_key: str = None,
        mock: bool = False
) -> ValidatedMessage:
    if mock:
        # mock
        return ValidatedMessage(
            data=ValidatedData(
                type='MESSAGE_TYPE_FRAME_ACTION',
                fid=msg.untrustedData.fid,
                timestamp=msg.untrustedData.timestamp,
                network=str(msg.untrustedData.network),
                frameActionBody=FrameAction(
                    url=msg.untrustedData.url,
                    buttonIndex=msg.untrustedData.buttonIndex,
                    castId=msg.untrustedData.castId,
                    inputTest=msg.untrustedData.inputText,
                    state=msg.untrustedData.state,
                    transactionId=msg.untrustedData.transactionId
                )
            ),
            hash=msg.untrustedData.messageHash,
            hashScheme='HASH_SCHEME_BLAKE',
            signature='',
            signatureScheme='SIGNATURE_SCHEME_ED25519',
            signer=''
        )

    return validate_message(msg, hub, username=username, password=password, api_key=api_key)
