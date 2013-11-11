help:
	@echo "make help     -- print this help"
	@echo "make generate -- regenerate the json"
	@echo "make update   -- upload the json and index.html to s3"

generate:
	python generate.py

update:
	s3cmd put index.html s3://wheelofshame/index.html
	s3cmd put results.json s3://wheelofshame/results.json
