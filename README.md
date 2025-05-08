# API para la Gestión de GitHub

## **Introducción**
Esta API permite la gestión de recursos de GitHub mediante un conjunto de endpoints diseñados para facilitar la interacción con los repositorios, usuarios y otros elementos clave de GitHub.

## **Características**
- Autenticación mediante tokens de acceso.

## **Requisitos Previos(Local)**
- **Python** v13.0.0.
- **Git** instalado en la máquina.
- Cuenta de GitHub con permisos de acceso (en caso de ser necesaria).
- **Elasticsearch** 8.18.0
- **Kibana 8.18.0**
- **Docker 25.0.3**

## **Instalación**
1. Clona el repositorio:
   ```bash
   git clone https://github.com/N1c0lasD4z4H/Proyecto_GrupoASD
2. Crear un entorno virtual 
    ```bash
    python -m venv .venv

    #Activar el entorno virtual
    .venv\Scripts\activate
    #Verificar que el entorno virtual se activo
    python which
3. Instalar dependencias
    ```bash
    #Actualizar el pip
    python -m pip install --upgrade pip
    # instalar el archivo requiriments
    pip install -r requirements.txt
## **Configuración**
1. Crea un archivo **.env** en la raiz del proyecto y configura las siguientes variables
    ```bash
    # Configura los permisos del token para accceder a los datos(admin,user,repo) 
   GITHUB_TOKEN=tu_token_de_acceso_de_github
   ELASTICSEARCH_URL=https://localhost:9200
   ELASTICSEARCH_USER=tu_usuario
   ELASTICSEARCH_PASSWORD=tu_contraseña(revisa el paso de autenticación)
## **Ejecución**
- Inicia el API ejecutando el siguiente comando:
    ```bash
    uvicorn main:app --reload
## **Endpoints**
Usar un cliente REST para probar el api
- directamente desde la documentacion fastapi http://127.0.0.1:8000/docs
- Thunder Client(extensión VSCODE)

### Repositorios 
- Descripción: Lista los repositorios del usuario autenticado.
- Get http://127.0.0.1:8000/github/user/N1c0lasD4z4H/repos

### Actividad repositorios
- Descripción: Muestra la actividad del repositorio en ultimo commit y actividad por semana.
- Get http://127.0.0.1:8000/github/N1c0lasD4z4H/Proyecto_GrupoASD/activity
### Actividad de usuario en repositorios
- Descripción: Lista los repositorios de un usuario, muestra # commits y muestra la fecha del ultimo commit realizado en cada uno de estos.
- Get http://127.0.0.1:8000/github/users/N1c0lasD4z4H/commits
### Pull Request 
- Descripción: Lista la cantidad de pull request con solicitud de cambios y aceptados segun la etiqueta de un repositorio en especifico
- Get http://127.0.0.1:8000/github/repos/NicoDazaHernandez/Request-etiquetas/pulls/stats

### Plantilla Pull requests
- Descripcion: Lista los repositorios con/sin plantilla 
- Get http://127.0.0.1:8000/github/users/N1c0lasD4z4H/check-pull-request-templates 

### Organizaciones o usuario
- Descripición: Lista los repositorios de una organizacion o usuario
- Get http://127.0.0.1:8000/github/org/N1c0lasD4z4H/repos

## *Activación Pruebas Unitarias*
- Descripcion: Codigo Para poder ejecutar las pruebas Unitarias, Mayor al 90% de covertura
 ```bash
   pytest --cov
   =app --cov-fail-under=90y
```
## **Autenticación**
#### Autenticación Local(Por unica vez):
El usuario debe tener instalado elastisearch y kibana versiones 8.18.0
- Ubicarse en la carpeta de elastisearch a través de la terminal
- Ejecutar el comando
  ```bash
    bin\elasticsearch
-  Es esta misma terminal es donde arrojara las credenciales del administrador(token, usuario y contraseña)
- debe detener el elastisearch desde la terminal previamente vista y volverlo a ejectutar.  
-Luego debera abrir otra terminal y ubicarse en la carpeta de kibana  
- Ejecutar el comando
  ```bash
    bin\kibana
- Debera ingresar a  kibana en el siguiente puerto http://localhost:5601 ya en el puerto debera ingresar el token y posteriormente validar las credenciales 
- Ya realizados estos pasos al  ejecutar nuevamente elasticsearch y kibana solo se solicitara las credenciales para acceder a kibana .
### Autenticacion Usuario: 
- Un usuario que necesita acceder a Elasticsearch puede recibir credenciales (como usuario y contraseña) de un administrador del sistema. Este administrador previamente configura los permisos y roles adecuados para el usuario en la plataforma. Al iniciar sesión con estas credenciales, el usuario podrá realizar las acciones permitidas según los permisos asignados, como consultar índices, realizar búsquedas o generar informes, sin afectar configuraciones críticas del sistema.