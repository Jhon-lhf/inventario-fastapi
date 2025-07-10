# 📦 API de Inventario - FastAPI

Bienvenido a mi primer proyecto backend usando **FastAPI**: una **API RESTful** para la gestión de productos, movimientos de stock, ventas, usuarios y reportes. Diseñada con enfoque modular y buenas prácticas, ideal para sistemas empresariales o educativos.

---

## 🚀 Funcionalidades

- ✅ Registro e inicio de sesión con **JWT**
- ✅ Gestión de usuarios y control de roles (`admin`, `vendedor`, `cliente`)
- ✅ CRUD de productos (con carga de imágenes)
- ✅ Movimientos de inventario (entradas y salidas)
- ✅ Gestión de ventas (detalle por producto)
- ✅ Reportes en **CSV/Excel** de inventario y ventas
- ✅ Filtros por usuario, tipo, fechas, producto
- ✅ Desactivación lógica de usuarios
- ✅ Roles configurables y actualizables

---

## 🧰 Tecnologías utilizadas

- **FastAPI** – Framework principal
- **SQLAlchemy** – ORM para manejo de base de datos
- **Alembic** – Control de versiones y migraciones
- **SQLite** – Base de datos local para desarrollo
- **Pydantic** – Validación de datos
- **JWT** – Autenticación segura
- **Uvicorn** – Servidor ASGI para desarrollo
---

## 📁 Estructura del proyecto

fast_api_inventario/
│
├── main.py # Punto de entrada de la aplicación
├── app/ # Lógica de la aplicación
│ ├── core/ # Configuración, seguridad, dependencias
│ ├── crud/ # Lógica de negocio (incluye reportes)
│ ├── models/ # Modelos SQLAlchemy
│ ├── routers/ # Endpoints agrupados
│ ├── schemas/ # Esquemas Pydantic
│ ├── database.py # Conexión a la base de datos
├── alembic/ # Carpeta de migraciones generadas por Alembic
├── alembic.ini # Configuración de Alembic
├── requirements.txt # Dependencias del proyecto
└── README.md # Este archivo


---

## 🔐 Roles y permisos

| Acción                         | Admin | Vendedor | Cliente |
|-------------------------------|:-----:|:--------:|:-------:|
| Ver productos                 | ✅    | ✅       | ✅      |
| Crear productos               | ✅    | ✅       | ❌      |
| Registrar movimientos         | ✅    | ✅       | ❌      |
| Ver historial de inventario   | ✅    | ✅       | ✅      |
| Registrar ventas              | ✅    | ✅       | ❌      |
| Ver ventas                    | ✅    | ✅       | ✅      |
| Ver usuarios                  | ✅    | ❌       | ❌      |
| Cambiar rol / activar usuario | ✅    | ❌       | ❌      |

---

## ⚙️ Instalación y ejecución

### 1. Clona el repositorio

```bash
git clone https://github.com/TU_USUARIO/inventario-fastapi.git
cd inventario-fastapi

2. Crea un entorno virtual

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

3. Instala dependencias

pip install -r requirements.txt

4. Ejecutar migraciones con Alembic

alembic upgrade head

5. Iniciar la aplicación

uvicorn main:app --reload


La API estará disponible en:
📍 http://localhost:8000

Documentación interactiva:
📚 http://localhost:8000/docs


⚠️ Notas

. Los endpoints de reportes requieren token JWT en la cabecera Authorization: Bearer <token>.

. Se implementa activación/desactivación lógica con el campo is_active.

. Todos los filtros están soportados vía query params para movimientos y ventas.



👤 Autor
Jhonatan Hernández
💻 Backend Developer en formación
📧 [jhonloveshisfamily@gmail.com]