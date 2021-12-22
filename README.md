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
### Librerías de pyhton
- py2neo
- psycopg2
- flask
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
