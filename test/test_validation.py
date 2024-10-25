"""
test cases for frame message validation
"""

# lib
import os
from dotenv import load_dotenv
import pytest

# src
from framelib import validate_message
from framelib.neynar import get_frame_message
from framelib.hub import get_message

load_dotenv()

class TestValidateMessageNeynar(object):

    def test_button_1(self):
        # example signed message from fid 8268 clicking button 1
        msg = '0a4e080d10cc4018cbe1a230200182013f0a2068747470733a2f2f707974686f6e2d6672616d652e76657263656c2e6170702f10011a1908cc401214000000000000000000000000000000000000000112140101bf04a2e61cb24c9a66c047ac5ed175e1bed8180122403feee9d0c1392c1e5bc7bca49850f83735c53b4f60c88959ffc271123e333a196e963d15619125e6034acda36076c709182daa5625e4affe6df21866c204830828013220ad4520314a78bc4317c604a3324ebc25bd8215c3ac38342fd790b7905c291bd1'
        action = get_frame_message(msg, os.getenv('NEYNAR_KEY'))
        assert action.tapped_button.index == 1
        assert action.interactor.fid == 8268
        assert action.input is None


class TestValidateMessageHub(object):

    def test_button_1(self):
        # example signed message from fid 8268 clicking button 1
        msg = '0a4e080d10cc4018cbe1a230200182013f0a2068747470733a2f2f707974686f6e2d6672616d652e76657263656c2e6170702f10011a1908cc401214000000000000000000000000000000000000000112140101bf04a2e61cb24c9a66c047ac5ed175e1bed8180122403feee9d0c1392c1e5bc7bca49850f83735c53b4f60c88959ffc271123e333a196e963d15619125e6034acda36076c709182daa5625e4affe6df21866c204830828013220ad4520314a78bc4317c604a3324ebc25bd8215c3ac38342fd790b7905c291bd1'
        action = get_message(msg, 'https://nemes.farcaster.xyz:2281')  # public read only
        assert action.data.frameActionBody.buttonIndex == 1
        assert action.data.fid == 8268
        assert action.data.network == 'FARCASTER_NETWORK_MAINNET'
        assert action.data.frameActionBody.inputText == ''

    def test_button_1_neynar(self):
        # example signed message from fid 8268 clicking button 1
        msg = '0a4e080d10cc4018cbe1a230200182013f0a2068747470733a2f2f707974686f6e2d6672616d652e76657263656c2e6170702f10011a1908cc401214000000000000000000000000000000000000000112140101bf04a2e61cb24c9a66c047ac5ed175e1bed8180122403feee9d0c1392c1e5bc7bca49850f83735c53b4f60c88959ffc271123e333a196e963d15619125e6034acda36076c709182daa5625e4affe6df21866c204830828013220ad4520314a78bc4317c604a3324ebc25bd8215c3ac38342fd790b7905c291bd1'
        action = get_message(msg, 'https://hub-api.neynar.com', api_key=os.getenv('NEYNAR_KEY'))
        assert action.data.frameActionBody.buttonIndex == 1
        assert action.data.fid == 8268
        assert action.data.network == 'FARCASTER_NETWORK_MAINNET'
        assert action.data.frameActionBody.inputText == ''
