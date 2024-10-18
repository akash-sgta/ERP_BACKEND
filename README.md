# ERP_BACKEND
ERP system backend on Django
___
### Steps to configure:
    1.  Create virtual environment
```commandline
python -m venv venv
```
    2.  Activate virtual environment (Windows)
```commandline
venv\Scripts\activate
```
    2.  Activate virtual environment (UNIX)
```commandline
source venv/bin/activate
```
    3.  Install from requirement.txt
```commandline
pip install -r mms/requirements.txt
```
## Projects
    1.  Medical Management System

___
### <u>M</u>edical <u>M</u>anagement <u>S</u>ystem
```commandline
python mms/manage.py makemigrations profile staff util patient
```
```commandline
python mms/manage.py migrate
```
```commandline
python mms/manage.py runserver 127.0.0.1:8000
```