# Avalon
An avalon jackbox-esque web app which handles nightphase automatically

## Dev Setup

```bash
python3.6 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mkdir tmp
python manage.py migrate
python manage.py runserver
```
