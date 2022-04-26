# MedicalLocation

need start psql server:

``
$ systemctl start postgresql.service
``

create db 

For apload in db
````
$psql dbname<dumpfile
````

````
$cd app/medical_location/
$python3 manage.py runserver 8000
````

open in brovser: http://127.0.0.1:8000/index