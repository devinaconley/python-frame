"""
data models
"""

import datetime
from typing import Optional, Literal
from pydantic import BaseModel


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
    value: Optional[str]
    data: Optional[str]


class Transaction(BaseModel):
    chainId: str
    method: Literal['eth_sendTransaction']
    params: EthTransactionParams


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
