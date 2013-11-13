help:
	@echo "make help     -- print this help"
	@echo "make generate -- regenerate the json"
	@echo "make update   -- upload the json and index.html to s3"

generate:
	python generate.py

update:
	s3cmd put index.html s3://wheelpackages/index.html  --cf-invalidate \
	--add-header='Cache-Control: max-age=30' \
	--add-header='Date: `date -u +"%a, %d %b %Y %H:%M:%S GMT"`'
	s3cmd put results.json s3://wheelpackages/results.json  --cf-invalidate \
	--add-header='Cache-Control: max-age=30' \
	--add-header='Date: `date -u +"%a, %d %b %Y %H:%M:%S GMT"`'
