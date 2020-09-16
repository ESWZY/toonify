PORT=8080

build :
	docker build --tag toonify app

run :
	docker run -p 9090:$(PORT) -e PORT=$(PORT) toonify