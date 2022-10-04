## Initialization

### Install Geospatial Database (Mac)

```bash
brew install postgres
brew install postgis
brew install gdal
brew install libgeoip
```

### Create postgis extension
Open you db administrator (I use pgAdmin4)
Open query tool and add the following
```bash
create extension postgis;
```
Then press run (for better instructions see my blog)

#### Create .env for local PostgreSQL database
```
LOCAL_DB_NAME=name-of-the-database
LOCAL_DB_USER=db-user-name
LOCAL_DB_PASSWORD=db-password
LOCAL_DB_HOST=host-you-want-to-use
LOCAL_DB_PORT=post-you-want-to-use
```

#### Create a virtual environment
``` python
python3 -m venv venv-location
source venv-location/bin/activate 
```

#### Install requirements.txt
```python
pip install -r requirements.txt
```

#### Migrate models
```python
python manage.py makemigrations
python manage.py migrate
````

#### Run
```python
python manage.py runserver
```
