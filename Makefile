PORT=8080

build :
	docker build --tag toonify app

run :
	docker run -p 9090:$(PORT) -e PORT=$(PORT) toonify

push :
	docker tag toonify gcr.io/toonify/hellotoon
	docker push gcr.io/toonify/hellotoon

deploy :
	gcloud run deploy --image gcr.io/toonify/hellotoon --platform managed