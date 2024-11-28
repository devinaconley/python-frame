"""
data models
"""

import datetime
from typing import Optional, Literal
from pydantic import BaseModel, SerializeAsAny
from eth_utils import is_address


# ---- frame message ----

class CastId(BaseModel):
    fid: int
    hash: str


class FrameAction(BaseModel):
    url: str
    buttonIndex: int
    inputText: Optional[str] = None
    state: Optional[str] = None
    transactionId: Optional[str] = None
    address: Optional[str] = None
    castId: CastId


class UntrustedData(FrameAction):
    # note: this untrusted message seems to collapse the ValidatedDate and FrameAction fields
    fid: int
    messageHash: str
    timestamp: int
    network: int


class TrustedData(BaseModel):
    messageBytes: str


class FrameMessage(BaseModel):
    untrustedData: UntrustedData
    trustedData: TrustedData


# ---- frame transaction ----

class EthTransactionParams(BaseModel):
    abi: list[dict]
    to: str
    value: Optional[str] = None
    data: Optional[str] = None


class Transaction(BaseModel):
    chainId: str
    method: Literal['eth_sendTransaction']
    params: EthTransactionParams


# ---- signature ----

class Address(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value, info):
        if not is_address(value):
            raise ValueError('invalid ethereum address')
        return value


class Bytes32(str):
    pass


class Bytes(str):
    pass


class Eip712Domain(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    chainId: Optional[int] = None
    verifyingContract: Optional[Address] = None
    salt: Optional[str] = None


class Eip712TypeField(BaseModel):
    name: str
    type: str


class Eip712Params(BaseModel):
    domain: Eip712Domain
    types: dict[str, list[Eip712TypeField]]
    primaryType: str
    message: SerializeAsAny[BaseModel]


class Signature(BaseModel):
    chainId: str
    method: Literal['eth_signTypedData_v4']
    params: Eip712Params


# ---- frame error ----

class FrameError(BaseModel):
    message: str


# ---- hub ----

class ValidatedData(BaseModel):
    type: str
    fid: int
    timestamp: datetime.datetime
    network: str
    frameActionBody: FrameAction


class ValidatedMessage(BaseModel):
    data: ValidatedData
    hash: str
    hashScheme: str
    signature: str
    signatureScheme: str
    signer: str


# ---- neynar ----

class NeynarViewer(BaseModel):
    following: bool
    followed_by: bool


class NeynarBio(BaseModel):
    text: str
    mentioned_profiles: Optional[list[str]] = []


class NeynarProfile(BaseModel):
    bio: NeynarBio


class NeynarInteractor(BaseModel):
    object: str
    fid: int
    username: str
    display_name: str
    custody_address: Optional[str] = None
    pfp_url: str
    profile: NeynarProfile
    follower_count: int
    following_count: int
    verifications: list[str]
    viewer_context: Optional[NeynarViewer] = None


class NeynarButton(BaseModel):
    title: Optional[str] = None
    index: int
    action_type: Optional[str] = None


class NeynarInput(BaseModel):
    text: str


class NeynarState(BaseModel):
    serialized: str


class NeynarTransaction(BaseModel):
    hash: str


class NeynarValidatedMessage(BaseModel):
    object: str
    interactor: NeynarInteractor
    tapped_button: NeynarButton
    input: Optional[NeynarInput] = None
    state: Optional[NeynarState] = None
    url: str
    cast: dict
    timestamp: datetime.datetime
    transaction: Optional[NeynarTransaction] = None


# ---- warpcast ----

class Pfp(BaseModel):
    url: str
    verified: bool


class WarpBio(BaseModel):
    text: str
    mentions: Optional[list[str]] = []
    channelMentions: Optional[list[str]] = []


class WarpLocation(BaseModel):
    placeId: str
    description: str


class WarpProfile(BaseModel):
    bio: WarpBio
    location: WarpLocation


class User(BaseModel):
    fid: int
    username: Optional[str] = None
    displayName: str
    pfp: Optional[Pfp] = None
    profile: WarpProfile
    followerCount: int
    followingCount: int
    activeOnFcNetwork: bool
