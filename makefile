install:
	@if [ ! -f .env ]; then\
        echo "HOST=0.0.0.0\nPORT=8888\nDEBUG=False" > .env;\
    fi
	@pip install -r requirements.txt

compile_requirements:
	@pip-compile

start:
	@python app.py

unit_test:
	@python -m pytest tests/unit/*