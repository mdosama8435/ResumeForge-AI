install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

test:
	pytest

lint:
	flake8 .

format:
	black .

clean:
	rm -rf __pycache__ outputs uploads
