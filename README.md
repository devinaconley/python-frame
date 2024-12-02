# framelib

lightweight library for building farcaster frames using python and flask

- easily render frames that conform to the farcaster specification
- parse and verify frame action messages using neynar or hubs
- query user profile info from warpcast
- on-chain frame transactions
- eip-712 signatures
- mint tokens


## quickstart

install `framelib` from pip
```
pip install framelib
```

simple example
```python
from flask import Flask, url_for
from framelib import frame

app = Flask(__name__)

@app.route('/')
def home():
    return frame(
        image='https://framelib.s3.us-east-1.amazonaws.com/framelib_logo.png',
        button1='next',
        post_url=url_for('second_page', _external=True),
    )
```

## examples

see a complete example using python + flask + vercel [here](https://github.com/devinaconley/python-frames/tree/main/examples/simple)

for an example that uses on-chain frame transactions, see the [weth frame](https://github.com/devinaconley/python-frames/tree/main/examples/transaction)

and for a more advanced example involving multiplayer games, supabase integration, dynamic image rendering, and more,
see [rock paper scissors](https://github.com/devinaconley/rock-paper-scissors)


## roadmap

upcoming features and improvements
- ~~mint actions~~
- ~~eip 712 signatures~~
- generated library documentation
- ~~dynamic image rendering tools~~
- compatibility with other web frameworks
- state signing
- **frames v2 support**
