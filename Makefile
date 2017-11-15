build-images:
	@echo "**** Build docker images ****"
	docker-compose build --force-rm

start-containers:
	@echo "**** Start docker containers ****"
	docker-compose up
