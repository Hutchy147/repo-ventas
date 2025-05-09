🛒 Sistema de Ventas - API REST con Flask
Este proyecto es un sistema de ventas desarrollado como API REST utilizando Flask y MySQL, con un enfoque modular para gestionar productos, clientes, proveedores, categorías y ventas. Cada módulo fue implementado en ramas separadas por distintos integrantes del equipo, lo que permitió un desarrollo organizado y colaborativo.

🚀 ¿Qué funcionalidades incluye?
Gestión de productos (stock, precio actual, modificación)

Gestión de clientes

Gestión de proveedores

Gestión de categorías (para organizar productos)

Registro de ventas

⚙️ Pasos para ejecutar el proyecto en otro dispositivo
Asegurate de tener una base de datos MySQL funcionando antes de iniciar.

1️⃣ Instalar herramientas necesarias
Visual Studio Code

Python 3.11+

MySQL Server 

Postman 

flask

2️⃣ Clonar el repositorio
bash
Copiar
Editar
git clone <https://github.com/Hutchy147/repo-ventas>
cd <carpeta-del-proyecto>
3️⃣ Crear y activar un entorno virtual
git bash
Copiar
Editar
python -m venv venv
# En Windows
venv\Scripts\activate
# En Linux/Mac
source venv/bin/activate
4️⃣ Instalar dependencias
pip install -r requirements.txt
5️⃣ Configurar la base de datos
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://usuario:contraseña@localhost/ventas_db"
Luego creá la base de datos y dejá que Flask cree las tablas automáticamente al iniciar.
6️⃣ Ejecutar el proyecto
python app.py
El servidor quedará corriendo en http://localhost:5000
🛠️ Tecnologías utilizadas
Python 3.11

Flask

Flask-SQLAlchemy

MySQL

PyMySQL

Postman (para pruebas)

Git y GitHub (para control de versiones)

📋 Instrucciones de uso
Para hacer pruebas, usá Postman apuntando a rutas como:

GET /api/products/

POST /api/products/

PUT /api/products/<id>/stock

PUT /api/products/<id>/precio

DELETE /api/products/<id>

Cada módulo tiene sus propias rutas organizadas por blueprints, por ejemplo:

/api/clients/

/api/suppliers/

/api/sales/

/api/categories/

👥 Integrantes del equipo y contribuciones
Nombre	Rama	Contribución
Franco Villarroel:	"sales"	Desarrollo completo del módulo de ventas, incluyendo rutas y lógica interna
Leandro Briceño:	"suppliers"	Implementación del módulo de proveedores con su CRUD correspondiente
Tomás Muñoz:	"category"	Diseño y desarrollo del sistema de categorías de productos
Mateo Gómez:	"product, clients"	CRUD completo de productos y clientes, además de gestión de stock y precio
