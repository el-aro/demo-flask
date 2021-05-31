# RESTful Demo

Ejemplo minimo de una app implementando REST, usa unicamente una tabla llamada Personas.


## Cargando Variables de Entorno (Linux).

Hay un archivo nombrado ".env" en este directorio con variables de entorno, poner los valores correctos y luego correr:

Production env.

    $ export $(cat .env | xargs)


## Dependencias

Las librerias necesarias se encuentran en el archivo "requirements.txt", para instalar usar

    $ pip install -r requirements.txt

Altamente recomendado usar un virtualenv

## Probar la app.

Una vez ejecutado los pasos anteriores podremos correr de manera local con el siguiente comando.

    $ python main.py

A continuación nos enseñara en consola nuestro server de pruebas corriendo en el puerto 5000.