python -m venv env
call env/scripts/activate
python manage.py makemigrations
python manage.py migrate
python manage.py runserver