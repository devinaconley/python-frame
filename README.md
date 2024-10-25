# framelib

lightweight library for building farcaster frames using python and flask

- easily render frames that conform to the farcaster specification
- configurable frame design
- parse frame action messages
- verify the frame action signatures using neynar
- query user profile info from warpcast
- on-chain frame transactions


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
        image='https://opengraph.githubassets.com/0x/devinaconley/python-frames',
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
- mint actions
- eip 712 signatures
- generated library documentation
- dynamic image rendering tools
- compatibility with other web frameworks
- state signing
