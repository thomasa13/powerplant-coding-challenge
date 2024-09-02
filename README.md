# How to install the application

## Docker (requires docker)
`docker build . -t powerplant-coding-challenge`
`docker run -p 8888:8888 powerplant-coding-challenge`

## Makefile (requires python & make)
`python -m venv .venv`
`source .venv/bin/activate`
`make install`
`make start`

## Manually (requires python)
`python -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
`echo "HOST=0.0.0.0\nPORT=8888\nDEBUG=False" > .env`
`python app.py`

# How to run the tests

## Docker
`docker exec powerplant-coding-challenge python -m pytest tests/unit/*`

## Makefile
`make unit_test`

## Manually
`python -m pytest tests/unit/*`