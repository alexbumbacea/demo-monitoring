up-detached:
	docker-compose up -d
logs:
	docker-compose logs -f --tail 100

sh.%: SERVICE=$*
sh.%:
	@echo 'Starting shell on $(SERVICE)'
	docker-compose exec $(SERVICE) sh

build.%: SERVICE=$*
build.%:
	docker-compose build $(SERVICE)

logs.%: SERVICE=$*
logs.%:
	docker-compose logs -f --tail 100 $(SERVICE)