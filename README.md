# Powerflex_Backend


## install dependencies

```bash
pip install -r requirements.txt
```

## Start App

```bash
python manage.py runserver
```

## Add Module

```bash
python manage.py startapp users
```

## Add Migration

```bash
python manage.py makemigrations
python manage.py makemigrations users
```

## Run Migration

```bash
python manage.py migrate
```

## Reset migration

```bash
python manage.py flush
```

## Create User 

```bash
python manage.py createsuperuser
```

## Export data

```bash
python manage.py export_faqs

```
## Load data

```bash
python manage.py loaddata product/fixtures/category.json
python manage.py loaddata product/fixtures/brand.json
python manage.py loaddata product/fixtures/product.json
python manage.py loaddata product/fixtures/appliance_category.json
python manage.py loaddata product/fixtures/appliance.json
python manage.py loaddata product/fixtures/band.json
python manage.py loaddata setting/fixtures/data.json
python manage.py loaddata cms/fixtures/faq_fixture.json
```


