# NBA-Forecaster
Este proyecto trata de proporcionar, a través de técnicas de Webscrapping, estadisticas sobre un equipo elegido de la NBA. También ofrece un pronostico en términos de probabilidad acerca del próximo partido basado en las cuotas que las casas de apuestas ofrecen.
## Requirements y config
Se ofrecen, por comodidad, dos ficheros para lanzar el programa. Requirements alberga todas las librerias y sus respectivas versiones necesarias. En el fichero de config se debera escribir la clave de acceso a la Api en la primera linea. Si se quisiera lanzar el programa sin correr la imagen de Docker habria que instalar las librerias del fichero requirements a mano, mediante el siguiente comando:
>pip install -r requirements.txt
## Docker.
Para lanzar la imagen de docker habrá que seguir los siguientes pasos:
1. Crear la imagen: 
- El punto indica que se cogen todos los archivos del directorio en el que nos encontramos. Podemos llamar a la imagen como queramos, teniendo en cuenta que al ejecutarla tendremos que usar ese nombre.
>docker build . -t 'nombre con el que quieras llamarlo'
2. Una vez que tengamos la imagen creada tendremos que elegir un path absoluto del directorio al que queramos que se linkee el contenedor de docker
para que podamos ver la salida del programa.
- absolute_path = ['path del directorio de salida host']. En el caso en el que no exista el directorio que queremos linkear lo crea.
- Es importante mantener la estructura del siguiente comando. En particular el path tras ':' no debera ser alterado ya que es el directorio interno del contenedor.
>docker run -i -v absolute_path:/out 'nombre con el que hayas llamado a la imagen'.
## Directorio Out
Será necesario tener una directorio vacio llamado out en el directorio de trabajo.


