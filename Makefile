.DEFAULT_GOAL := run

.PHONY: prod push run down

registry = ghcr.io/snoensoftware
image = nrk-subtitles

prod:
	docker build . -f docker/fastapi/Dockerfile --target=runner -t $(registry)/$(image)

push: prod
	docker push $(registry)/$(image)

run: prod
	docker-compose up -d

down:
	docker-compose down
