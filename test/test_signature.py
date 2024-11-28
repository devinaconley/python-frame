"""
test cases for frame signature requests and verification
"""

# lib
from pydantic import BaseModel
from flask import Flask

# src
from framelib import signature, Address

app = Flask(__name__)


class TestSignature(object):

    def test_signature_request(self):
        class Message(BaseModel):
            message: str
            timestamp: int

        msg = Message(message='hello world', timestamp=1234567890)

        with app.app_context():
            res = signature(1, msg, domain='myprotocol')

            assert res.status_code == 200
            assert res.json['chainId'] == 'eip155:1'
            assert res.json['method'] == 'eth_signTypedData_v4'
            assert res.json['params']['domain']['name'] == 'myprotocol'
            assert res.json['params']['domain']['chainId'] == 1
            assert 'salt' not in res.json['params']['domain']
            assert 'verifyingContract' not in res.json['params']['domain']

            assert len(res.json['params']['types']) == 1
            assert res.json['params']['types']['Message'] == [
                {'name': 'message', 'type': 'string'},
                {'name': 'timestamp', 'type': 'uint256'}
            ]
            assert res.json['params']['primaryType'] == 'Message'
            assert res.json['params']['message'] == {'message': 'hello world', 'timestamp': 1234567890}

    def test_signature_request_nested(self):
        class User(BaseModel):
            name: str

        class Message(BaseModel):
            message: str
            timestamp: int
            sender: User
            recipient: User

        msg = Message(
            message='hello bob',
            timestamp=1234567890,
            sender=User(name='alice'),
            recipient=User(name='bob')
        )

        with app.app_context():
            res = signature(
                8453,
                msg,
                domain='another_app',
                version='v3',
                contract='0x1234567890abcdef1234567890abcdef12345678',
                salt='0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef',
            )

            assert res.status_code == 200
            assert res.json['chainId'] == 'eip155:8453'
            assert res.json['method'] == 'eth_signTypedData_v4'
            assert res.json['params']['domain']['name'] == 'another_app'
            assert res.json['params']['domain']['version'] == 'v3'
            assert res.json['params']['domain']['chainId'] == 8453
            assert res.json['params']['domain']['verifyingContract'] \
                   == '0x1234567890abcdef1234567890abcdef12345678'
            assert res.json['params']['domain']['salt'] \
                   == '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef'

            assert len(res.json['params']['types']) == 2
            assert res.json['params']['types']['Message'] == [
                {'name': 'message', 'type': 'string'},
                {'name': 'timestamp', 'type': 'uint256'},
                {'name': 'sender', 'type': 'User'},
                {'name': 'recipient', 'type': 'User'}
            ]
            assert res.json['params']['types']['User'] == [
                {'name': 'name', 'type': 'string'}
            ]
            assert res.json['params']['primaryType'] == 'Message'
            assert res.json['params']['message'] == {
                'message': 'hello bob',
                'timestamp': 1234567890,
                'sender': {'name': 'alice'},
                'recipient': {'name': 'bob'}
            }

    def test_signature_request_eth(self):
        class Approval(BaseModel):
            token: Address
            limit: int
            expiry: int

        msg = Approval(
            token='0x4200000000000000000000000000000000000006',
            limit=int(500e18),
            expiry=1234567890
        )

        with app.app_context():
            res = signature(
                8453,
                msg,
                domain='gasless_exchange',
                contract='0x1234567890abcdef1234567890abcdef12345678',
            )

            assert res.status_code == 200
            assert res.json['chainId'] == 'eip155:8453'
            assert res.json['method'] == 'eth_signTypedData_v4'
            assert res.json['params']['domain']['name'] == 'gasless_exchange'
            assert res.json['params']['domain']['chainId'] == 8453
            assert res.json['params']['domain']['verifyingContract'] \
                   == '0x1234567890abcdef1234567890abcdef12345678'
            assert 'salt' not in res.json['params']['domain']
            assert 'version' not in res.json['params']['domain']

            assert len(res.json['params']['types']) == 1
            assert res.json['params']['types']['Approval'] == [
                {'name': 'token', 'type': 'address'},
                {'name': 'limit', 'type': 'uint256'},
                {'name': 'expiry', 'type': 'uint256'}
            ]
            assert res.json['params']['primaryType'] == 'Approval'
            assert res.json['params']['message'] == {
                'token': '0x4200000000000000000000000000000000000006',
                'limit': 500e18,
                'expiry': 1234567890
            }
