"""
methods for frame transactions
"""

# lib
from typing import Type
from eth_abi import encode
from eth_utils import is_address, function_signature_to_4byte_selector, function_abi_to_4byte_selector
from flask import jsonify, Response
from pydantic import BaseModel

# src
from .models import Transaction, EthTransactionParams, Address, Bytes, Bytes32, Eip712TypeField, Signature, \
    Eip712Domain, Eip712Params


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


def signature(
    chain_id: int,
    message: BaseModel,
    domain: str = None,
    version: str = None,
    contract: str = None,
    salt: str = None
) -> Response:
    # collect custom types
    def recurse_model_types(model: Type[BaseModel]):
        types_ = {}
        for name_, field_ in model.__annotations__.items():
            if not issubclass(field_, BaseModel):
                continue
            types_ = recurse_model_types(field_)
            types_[field_.__name__] = field_
        types_[model.__name__] = model
        return types_

    types = recurse_model_types(message.__class__)

    primitives = {
        'int': 'uint256',
        'str': 'string',
        'bool': 'bool',
        'Address': 'address',
        'Bytes': 'bytes',
        'Bytes32': 'bytes32'
    }

    # format eip712 type definitions
    eip712_types = {}
    for name, cls in types.items():
        fields = []
        for n, f in cls.__annotations__.items():
            t = f.__name__
            if t in primitives:
                fields.append(Eip712TypeField(name=n, type=primitives[t]))
            elif t in types:
                fields.append(Eip712TypeField(name=n, type=t))
            else:
                raise ValueError(f'unsupported field type {n} {t}')
        eip712_types[name] = fields

    sig = Signature(
        chainId=f'eip155:{chain_id}',
        method='eth_signTypedData_v4',
        params=Eip712Params(
            domain=Eip712Domain(
                name=domain,
                version=version,
                chainId=chain_id,
                verifyingContract=contract,
                salt=salt
            ),
            types=eip712_types,
            primaryType=message.__class__.__name__,
            message=message
        )
    )

    # response
    res = jsonify(sig.model_dump(mode='json', exclude_none=True))
    res.status_code = 200
    return res
