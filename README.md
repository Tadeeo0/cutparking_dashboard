# Proyecto Flask - CutParking Dashboard

Este es un proyecto web desarrollado con Flask para la gestión de estacionamientos. El proyecto permite al administrador visualizar el estado de los espacios disponibles, realizar reservas, y mucho más.

## Requisitos

- Python 3.x
- MySQL
- pip

## Instalación y configuración

### 1. Clonar el repositorio

git clone https://github.com/Tadeeo0/cutparking_dashboard.git

cd cutparking_dashboard

2. Crear un entorno virtual

python -m venv venv

3. Activar el entorno virtual

En Windows: venv\Scripts\activate

En MacOS: source venv/bin/activate

5. Instalar las dependencias
   
Una vez que tengas el entorno virtual activado, instala las dependencias del proyecto con:

pip install -r requirements.txt

7. Configurar las variables de entorno
   
Crea un archivo .env en la raíz del proyecto con las siguientes variables:

- DB_USER=your_username
- DB_PASSWORD=your_password
- DB_HOST=localhost
- DB_PORT=330X
- DB_NAME=parking_dashboard

9. Ejecutar la aplicación
    
Finalmente, puedes ejecutar la aplicación de Flask con:

python run.py


