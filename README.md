# Midilarity
## Final Base de Datos 2
## Tema
- Creamos, poblamos y hacemos queries con archivos midi, comparando similitudes entre canciones, el feeling de cada una y más!
## Integrantes
- Spitzner, Agustín - Legajo 60142
- Donikian, Gastón - Legajo 60067
- Espina, Segundo ' Legajo 60150
## Dependencias
- python
- docker
- neo4j
- postgres

### Librerías de pyhton
- py2neo
- psycopg2
- flask
- flask_swagger_ui
- fastapi
- apiflask
## Compilación
- Instalar las dependencias de pyhton con los comandos:

```bash
$ pip3 install py2neo
```
```bash
$ pip3 install psycopg2
```
```bash
$ pip3 install flask
```
```bash
$ pip3 install apiflask
```
```bash
$ pip3 install fastapi
```
```bash
$ pip3 install flask_swagger_ui
```

## Ejecución
### Correr postgres y Neo4j
- Ejecutar estos comandos:

```bash
$ docker pull postgres
```

```bash
$ docker run --name Mypostgres -e POSTGRES_PASSWORD=<mysecretpassword> -p 5432:5432 -d postgres
```

```bash
$ docker pull neo4j
```

```bash
$ docker run --name Myneo4j -p 7474:7474 -p 7687:7687 --env=NEO4J_AUTH=none -d neo4j
```
- Abrir un web browser para acceder a la interfaz Web de Neo4j: http://localhost:7474/browser
- En el símbolo $, ejecutar :server connect (elegir No Authentication en Authentication type)

### Correr api
- Entrar al archivo psql_connection.py, cambiar la linea 75, donde dice:
con = psycopg2.connect(database="tp_midi", user="segundo", password="admin", host="localhost", port="5432")
- y llenarla con los datos de la base de datos de uno
    
- Parado en la carpeta del proyecto, correr el siguiente comando:
```bash
$ python3 api.py
```
- La api corre por default en el puerto 5001
- Se puede ver la documentación de la api en la url: http://localhost:5001/api/docs

### Queries de la api

#### 1. Obtener el feeling de un artista particular
```
http://localhost:5001/artist_feeling?artist=artist_name
```
donde artist_name es el nombre del artista del que quiero conocer el feeling

#### 2. Ver si hay relación entre intensidad y tensión
```
http://localhost:5001/intensity_ratio
```
#### 3. Obtener la sequencia de acordes mas popular en la base de datos
```
http://localhost:5001/popular_sequence
```
#### 4. Obtener los artistas positivos en la base de datos
```
http://localhost:5001/positive_artists
```
#### 5. Obtener canciones similares a una elegida
```
http://localhost:5001/similar?title=my_title&artist=my_artist

donde my_artist y My_title son el nombre del artista y la canción que quiero buscar similares
```
#### 6. Obtener canciones que son de un cierto feeling
```
http://localhost:5001/song_by_feeling?feeling=my_feeling
```
Donde my_feeling ouede ser o "positive" o "negative"
#### 7. Obtener todas las canciones
```
http://localhost:5001/songs
```
#### 8. Obtener datos de canción específica
```
http://localhost:5001/songs?title=my_title&artist=my_artist
```

donde my_artist y my_title son el nombre del artista y la canción que quiero buscar

#### 9. Insertar canción

con curl sería asi:
```
curl -X POST "http://localhost:5001/songs" -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "artist=queen" -F "file=@Queen_-_Radio_Ga_Ga.mid;type=audio/midi"
```
en este ejemplo, el artista es queen, y el archivo es un midi de radio gaga

#### 10. Conseguir las pistas de una canción

```
http://localhost:5001/tracks?title=my_title&artist=my_artist
```

donde my_artist y my_title son el nombre del artista y la canción que quiero buscar
