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

## Load data

```bash
python manage.py loaddata product/fixtures/category.json
python manage.py loaddata product/fixtures/brand.json
python manage.py loaddata product/fixtures/product.json
python manage.py loaddata setting/fixtures/data.json
```


