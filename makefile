up:
	docker-compose up
down:
	docker-compose down
test:
	python manage.py test
makemigrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
run:
	python manage.py runserver