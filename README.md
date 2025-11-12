# Django Product Catalog


A minimal Django app demonstrating models, admin-driven data entry, and a search/filter UI by description, category, and tags.

AI was used to get comfortable with Django since it is new to me 

## Requirements
- Python 3.10+
- Django (see requirements.txt)


## Setup
```bash
source .venv/bin/activate
pip install -r requirements.txt
cd remarcable
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver