
# Order Management System API

A practical test project built with Django and Django REST Framework for managing orders and order items, complete with role-based access control, testing, and Docker support.

## 🚀 Features

- Role-based user system (`admin`, `customer`)
- API for creating and managing orders and order items
- Product management
- Filtering orders by date and total amount
- Secure access: customers can only access their own orders
- Dockerized setup with PostgreSQL
- Auto-generated API docs (Swagger/OpenAPI)
- Clean code and full test coverage using `pytest`

---

## 🛠️ Tech Stack

- Python 3.11+
- Django 4+
- Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Pytest
- Factory Boy

---

## 📦 Project Structure

```bash
EnergyYar/
└── apps/
    ├── users/             # Custom user model with roles
    ├── orders/            # Order and OrderItem models + APIs
    ├── product/           # Product model
    ├── tests/             # All unit tests and factories
    ├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Getting Started

### 1. Clone the repository

```bash
git clone <your_repo_url>
cd order_system
```

### 2. Create `.env` file

```env
DB_NAME=orders_db
DB_USER=postgres
DB_PASSWORD=postgres
```

### 3. Run the project using Docker

```bash
docker-compose up --build
```

App will be available at: `http://localhost:8000`

---

## 🧪 Running Tests

```bash
docker-compose run web python manage.py test 
```

---

## 📘 API Documentation

After running the app, go to:

```
http://localhost:8000/api/schema/
```

Uses **drf-spectacular** for automatic OpenAPI/Swagger schema generation.

---

## 🔐 Roles & Permissions

| Role     | Description                       | Permissions                  |
|----------|-----------------------------------|------------------------------|
| Admin    | Superuser with full access        | Can manage all orders        |
| Customer | Regular user                      | Can only manage own orders   |

---

## 👤 Default Admin User (optional)

If you want to create a default admin:

```bash
docker-compose run web python manage.py createsuperuser
```

---

## 📄 License

This project is for evaluation purposes only.
