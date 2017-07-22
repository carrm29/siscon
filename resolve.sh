python manage.py shell < check.py

read -p "Deseas que queden sin cambios??? (y para ok/n para hacer una migración)" migrateok

if [ $migrateok = "n" ]
then
    python manage.py shell < rm_badcolumns.py

    python manage.py makemigrations
    sleep 1
    python manage.py migrate

    python manage.py shell < resume_badcolumns.py

    python manage.py makemigrations
    sleep 1
    python manage.py migrate

    echo Deberá funcionar ahora..
else
    echo No se realizaron cambios..
fi
