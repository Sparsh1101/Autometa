web: python manage.py runserver 0.0.0.0:$PORT --noreload
web: gunicorn django_project.wsgi:application --log-file - --log-level debug
python manage.py collectstatic --noinput
manage.py migrate