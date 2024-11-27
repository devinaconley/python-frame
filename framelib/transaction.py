"""
methods for frame transactions
"""

# lib
from eth_abi import encode
from eth_utils import is_address, function_signature_to_4byte_selector, function_abi_to_4byte_selector
from flask import jsonify, Response

# src
from .models import Transaction, EthTransactionParams


def transaction(
        chain_id: int,
        contract: str,
        abi: list[dict],
        value: str = None,
        function_signature: str = None,
        function_arguments: list = None
) -> Response:
    if not is_address(contract):
        raise ValueError(f'invalid contract address {contract}')

    # encode transaction calldata
    data = None
    if function_signature:
        fx_abi = None
        for a in abi:
            if 'name' not in a:
                continue
            if function_signature_to_4byte_selector(function_signature) == function_abi_to_4byte_selector(a):
                fx_abi = a
                break
        if fx_abi is None:
            raise ValueError(f'method {function_signature} not found in abi')

        data = '0x' + function_abi_to_4byte_selector(fx_abi).hex()

        if fx_abi['inputs'] and function_arguments:
            data += encode([i['type'] for i in fx_abi['inputs']], function_arguments).hex()

    # setup frame transaction
    tx = Transaction(
        chainId=f'eip155:{chain_id}',
        method='eth_sendTransaction',
        params=EthTransactionParams(abi=abi, to=contract, value=value, data=data)
    )

    # response
    res = jsonify(tx.model_dump(mode='json', exclude_none=True))
    res.status_code = 200
    return res


def mint(chain_id: int, contract: str, token_id: int = None) -> str:
    if not is_address(contract):
        raise ValueError(f'invalid contract address {contract}')

    target = f'eip155:{chain_id}:{contract}'
    if token_id is not None:
        target += f':{token_id}'

    return target
