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

restart.%: SERVICE=$*
restart.%:
	docker-compose restart $(SERVICE)

logs.%: SERVICE=$*
logs.%:
	docker-compose logs -f --tail 100 $(SERVICE)

stop:
	docker-compose stop
start-testing:
	ab -n 10000 -c 20 -t 600 http://localhost/python36/ &
	ab -n 10000 -c 20 -t 600 http://localhost/python35/ &
	ab -n 10000 -m POST -c 20 -t 600 http://localhost/python35/ &
	ab -n 10000 -c 20 -t 600 http://localhost/php/ &
	ab -n 10000 -m PATCH -c 20 -t 600 http://localhost/php/ &
