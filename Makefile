run:
	pipenv run celery --app core.celery worker --purge --beat --loglevel INFO --autoscale=0,10 --without-gossip --without-mingle --without-heartbeat & pipenv run ./manage.py runserver