"""
test cases for frame minting logic
"""

# src
from framelib import mint


class TestTransaction(object):

    def test_mint(self):
        target = mint(7777777, '0x060f3edd18c47f59bd23d063bbeb9aa4a8fec6df')
        assert target == 'eip155:7777777:0x060f3edd18c47f59bd23d063bbeb9aa4a8fec6df'

    def test_mint_with_id(self):
        target = mint(7777777, '0x060f3edd18c47f59bd23d063bbeb9aa4a8fec6df', token_id=1234)
        assert target == 'eip155:7777777:0x060f3edd18c47f59bd23d063bbeb9aa4a8fec6df:1234'
