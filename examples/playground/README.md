# playground python frame

multi-page farcaster frame built with python, framelib, flask, and vercel

this sample frame demonstrates eip-712 signatures, text inputs, message validation, image rendering, and links

## setup

(optional, but recommended) set up a virtual environment (conda or other)
```
conda create -n frame-example python=3.9
conda activate frame-example
```

install dependencies
```
pip install -r requirements.txt
```

setup vercel
```
npm install vercel
```


## development

run local app
```
npx vercel dev
```

you can run the frame debugger provided by [frames.js](https://github.com/framesjs/frames.js) to test locally


## deployment

make sure your project has been pushed to a github repo

import your project to [vercel](https://vercel.com/) with the flask framework

register with [neynar](https://neynar.com/) to get an api key

define the `NEYNAR_KEY` environment variable in your vercel project settings

deploy!
