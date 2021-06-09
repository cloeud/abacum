# Prueba técnica para Abacum
_Esta aplicación ha sido desarrollada como solución a la prueba técnica planteada por la empresa Abacum. Espero que esta guía pueda ayudar a los revisores, para que su tarea no sea demasiado pesada_

## Herramientas utilizadas para el desarrollo
¿Qué se ha utilizado para el desarrollo de la API?
* **Python**: está basada en el lenguaje Python para el desarrollo, en concreto se ha usado la versión 3.9.4.
* **Django**: se ha utilizado este framework entre otros motivos por su amplia comunidad y por la estructuración de los diferentes scripts que ofrece, en concreto se ha usado la versión 3.2.2
* **MySQL**: Por último, se ha optado por este tipo de base de datos ya que vamos a tratar con una cantidad de datos elevada donde necesitaremos un ágil tratamiento de los datos.

## Pre-requisitos
Antes de interactuar con la API se deben tener instalados en el sistema Python 3, MySQL y por útltimo una serie de paquetes que serán necesarios. Para ello se ha creado el archivo requirements.txt y podemos ejecutar en un terminal:
```
pip install -r requirements.txt 
```

## Construcción de la base de datos
Para la construcción de la base de datos se ha desarrollado el script **manageCSV.py**, que se compone de dos partes:
1. La primera parte trata de la creación del usuario _myuser_, junto con la base de datos _abacum_ que usaremos en este proyecto. En esta primera parte se pedirá la contraseña de root de MySQL, necesaria para las acciones previamente descritas. Por último, se lanzarán los comandos para las migraciones necesarias de la base de datos de Django.
2. La segunda parte se centra en la inserción de los datos del documento CSV, que se volcarán en la tabla _transactions_. Para optimizar el tratamiento de los datos se ha utilizado la librería _pandas_.

Para ejecutar el script nos situaremos en el directorio principal donde se encuentra y mediante un terminal ejecturaremos:
```
python manageCSV.py
```
Tras ejecutarlo nos preguntará si queremos ejecutar la primera parte del script, es decir, la creación de la base de datos _abacum_ para nuestro proyecto. Tras responder que sí (_yes_) nos pedirá la clave de root para MySQL que hemos establecido en nuestro sistema. Tras la inserción procederá a crear el usuario _myuser_, la base de datos _abacum_ y los permisos correspondientes junto con las migraciones antes comentadas.
En cuanto complete las migraciones nos preguntará si queremos importar los datos del CSV a la base de datos que acabamos de crear, volvemos a responder que sí (_yes_) y se procederá la carga de datos a la tabla _transactions_ dentro de nuestro proyecto. El proceso puede demorarse unos 25 segundos debido al volumen de datos.
Esto completaría el proceso de creación de la base de datos junto con la inserción de los datos del CSV.

## API
Siguiendo los pasos anteriores ya se tendría la base de datos con todos los datos importados. Sólo faltaría ejecutar el siguiente comando en la carpeta principal:
```
python manage.py runserver
```
Y la API ya estaría lista para usar, en este caso en la dirección _http://127.0.0.1:8000/_.
En los siguientes apartados se detallarán los diferentes endpoints con los que podremos interactuar con la API y así obtener datos de distintas formas.
Los siguientes endpoints se han desarrollado siguiendo los ejemplos de obtención de datos que se daban en el enunciado de la prueba técnica.

### /csvdata
El endpoint _csv_ se ha desarrollado para realizar la inserción en la base de datos que se creó  previamente con el archivo **manageCSV.py**. Es decir, que tal y como se pidió en las tareas a realizar en la prueba técnica, se ofrece una alternativa para importar los datos del archivo CSV a la base de datos mediante un endpoint en lugar de usar la línea de comandos con un script.
Si los datos van a ser importados con este método, es posible entonces saltarse el último paso del script manageCSV.py que hemos visto previamente. ¿Cómo es posible saltar ese paso? Simplemente respondiendo un _no_ en la última pregunta que hacía referencia a la importación de los datos del CSV a la base de datos _abacum_. Aunque no habría ningún tipo de problema si emplea un método y luego otro, ya que en ambos casos se eliminan todos los datos que hubiera previamente en _transactions_.

Si utilizáramos _curl_ para interactuar con nuestra API mediante línea de comandos ejecutaríamos:
```
curl -X POST -H 'Content-Type: application/json' -d '{"url": "https://raw.githubusercontent.com/abacum-io/abacum-recruitment-test/master/backed-python/support-files/sample-data.csv"}' http://127.0.0.1:8000/csvdata/
```

Donde se ha habilitado el campo _url_ para especificar la ruta donde se encuentra el archivo CSV.
El proceso de inserción dura aproximadamente lo mismo que con el anterior proceso, es decir unos 25 segundos.

### /data
Con el endpoint _/data_ se tendrá acceso a todos los datos del archivo CSV al que se le ha añadido un identificador como clave primaria. El resto de datos de la base de datos lo conforman las diferentes columnas que se encontraban en el CSV; es decir, date, account y amount. 
Accediendo a este endpoint podremos añadir nuevos datos (especificando los 3 datos ya comentados), listar los ya creados, acceder a través del _id_ a ellos individualmente
Si utilizamos _curl_ para interactuar con nuestras API mediante línea de comandos ejecutaríamos:
```
curl http://127.0.0.1:8000/api/data
```
Con ese comando se obtendrían todas las entradas que hay en la base de datos (11716 para ser exactos). No sería una práctica recomendable el querer obtener todos los datos a la vez, pero se ha desarrollado esa extensión _/data_ para que puedan utilizarse los métodos GET, POST, PUT y DELETE. Por lo que podemos añadir entradas nuevas, eliminarlas o incluso modificar datos. Para obtener un dato particular o ya sea para modificarlo o eliminarlo se usará el identificador _id_ por lo que con _api/data/1_ accederíamos a la primera entrada de la base de datos.

### /year
Con el endpoint _/year_ se accederá al balance de todas las cuentas durante el año. Los resultados están ordenados por el número de cuenta de menor a mayor. Un ejemplo de uso sería el siguiente:
```
curl http://127.0.0.1:8000/api/year
```

### /yearaccount
Con el endpoint _/yearaccount_ se obtendrá el mismo balance que con el endpoint anterior, pero en este caso se deberá especificar la cuenta de la que se quieren obtener los resultados. Un ejemplo de uso sería el siguiente:
```
curl "http://127.0.0.1:8000/api/yearaccount?account=68100000"
```

### /monthly
Con el endpoint _/monthly_ se accederá al balance mensual de todas las cuentas durante el año. Los resultados están ordenados por el número de cuenta de menor a mayor y dentro de cada cuenta, por el númeor de mes de enero a diciembre (excluyendo los meses donde no haya ninguna cantidad asignada). Un ejemplo de uso sería el siguiente:
```
curl http://127.0.0.1:8000/api/monthly
```

### /monthlyaccount
Con el endpoint _/monthlyaccount_ se obtendrá el mismo balance que con el endpoint anterior, pero en este caso se deberá especificar la cuenta de la que se quieren obtener los resultados. Un ejemplo de uso sería el siguiente:
```
curl "http://127.0.0.1:8000/api/monthlyaccount?account=68100000"
```

### /month
Con el endpoint _/month_ se accederá al balance mensual de todas las cuentas especificando el mes del que se quiere obtener dicho balance. Los resultados están ordenados por el número de cuenta de menor a mayor . Un ejemplo de uso sería el siguiente:
```
curl "http://127.0.0.1:8000/api/month?month=3"
```

### /monthyaccount
Con el endpoint _/monthaccount_ se obtendrá el mismo balance que con el endpoint anterior, pero en este caso se deberá especificar también la cuenta de la que se quieren obtener los resultados. Un ejemplo de uso sería el siguiente:
```
curl "http://127.0.0.1:8000/api/monthaccount?account=68100000&month=5"
```

## Posibles mejoras
Hay bastante margen de mejora para esta API, y por ello quería plasmar algunas ideas que se podrían llevar a cabo en caso de ampliación o mejora:
* _Especificar año_: Esta API se ha desarrollado siguiendo las pautas de la prueba técnica y los datos ofrecidos en el archivo CSV. Al ser todos los datos del año 2020 y al no hacer ninguna mención respecto a que hubiera que realizar una clasificación por año, ya sea para mostrar los resultados o especificando el año en forma de variable, la API da por hecho que todos los datos introducidos pertenecerán al mismo año. Por ello una posible mejora podría ser añadir nuevos endpoints o recoger una variable con el año del que se quieren obtener los resultados de los endpoints ya desarrolados.
* _Nuevos endpoints que ofrezcan datos al usuario_: Además de los endpoints ya creados, podrían desarrollarse nuevos para ofrecer una API más completa al usuario. Por ejemplo, para obtener el balance de un periodo específico por cuenta, donde se especifique la fecha inicial y la fecha final.
* _Depurar respuesta de errores_: Para este proyecto se ha tratado de comprobar que los parámetros que se pasan en los distintos enpoints tengan un formato correcto, devolviendo un tipo de respuesta HTTP 400 (bad request) ó 204 (no content) en cada caso. Aún así, podría especificarse algún tipo de mensaje para cada caso, con la idea de que la comprobación de errores sea más explícita para el usuario que use la API. Además se podrían añadir nuevas comprobaciones en cada caso.
* _Uso de Docker_: Otra posible mejora sería el uso de docker en esta API, con lo que se llegaría a un nivel de encapsulamiento muy útil y sobretodo muy práctico para el usuario que vaya a probar la API.
* _Nuevos tests_: Aunque en este proyecto se incluyen varios test de comprobación de todos los endpoints que ofrecen datos de balance, podrían desarrollarse nuevos tests con mayor número de datos y diferentes casos. Así se tendría un API mucho más robusta.

## Simplemente gracias
No quería despedir este documento sin expresar mi gratitud, no sólo por darme la oportunidad, sino también por haber tenido tanto interés en mi perfil. Cada pequeño o gran proyecto en el que me veo envuelto me hace crecer como profesional, además siempre descubro algo nuevo ya sea con el framework django o con el lenguaje de programación python en general, y esto me hace querer seguir aprendiendo y madurando cada vez más como desarrollador.