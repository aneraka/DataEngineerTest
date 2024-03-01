# <Your-Project-Title>

## Descripción

Es proyecto se desarrola con el fin de poner en practica diferentes herramientas que son usadas en el desarrollo de la ingenieria de datos:

- FASTapi
- Aws S3
- Base de datos (Postgresql)
- Docker
- Formato de archivos AVRO

## Índice

- [Instalación](#instalación)
- [Uso](#uso)
- [Funciones](#funciones)
- [Licencia](#licencia)

## Instalación

Para el buen funcionamiento del proyecto es necesario realizar los siguientes pasos:

- Clone el repositorio
- Una vez clonado configure el archivo .env (Tome de base el archivo env.example)
- - Acceso AWS: Configure el access key en su entorno aws (https://us-east-1.console.aws.amazon.com/iam)
  - S3 Bucket: Cree un bucket en s3
  - FERNET KEY: Cree el key para encriptar el password en base de datos (https://8gwifi.org/fernet.jsp)
  - JWT_KEY: Cree un valor semilla para la generacion del Token
- Ejecucion:
- -  Ubiquese en la carpeta docker
  -  ejecute el comando docker-compose up --build
- Cuando finalice la ejecucion y se esten ejecutando los servicios en docker debe configurar el user y password para la autenticacion en base de datos
- - Usando el FERNET_KEY encripte una contrasena (https://8gwifi.org/fernet.jsp)
  - Conectese a la base de datos e inserte los datos de user y password (encriptada)
  - - Tabla auth.user

## Uso

Ve a la direccion [localhost:1210/docs](http://localhost:1210/docs#/)

## Funciones

- Generacion de token para proporciona seguridad
- Subir archivos a base de datos
- - Almacenamiento archivos origen en S3
  - Almacenamiento en base de datos
  - Control de cambios
- Creacion de archivos AVRO
- - Almacenamiento en S3
- Listado de archivos en S3
- Entrega de informacion
- - Reporte personalizado
  - Reportes especificos

