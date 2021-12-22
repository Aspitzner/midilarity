# Midilarity
## Final Base de Datos 2
## Integrantes
- Spitzner, Agustín - Legajo 60142
- Donikian, Gastón - Legajo 60067
- Espina, Segundo ' Legajo 60150
## Dependencias
- python
- docker
- neo4j
- postgres
- 
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
- Parado en la carpeta del proyecto, correr el siguiente comando:
```bash
$ python3 api.py
```
- La api corre por default en el puerto 5001
- Se puede ver la documentación de la api en la url
`http://localhost:5001/api/docs`
