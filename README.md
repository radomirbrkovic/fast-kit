# ⚡ FastKit

FastKit is a lightweight starter admin panel for web applications built with [FastAPI](https://fastapi.tiangolo.com/).
The UI is based on the beautiful [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/) template.

It provides a solid foundation with features that most apps need out-of-the-box, so you can focus on building what makes your project unique.

Use FastKit if you want to quickly scaffold an admin interface for your FastAPI application, manage users and roles, and have multi-language support out of the box.

## ✨ Features

- 🔐 User & Role Management – authentication, user accounts, and role-based permissions
- 📄 Public Pages – create and manage basic pages for your app
- 📊 Dashboard – modern Bootstrap 5 admin interface
- ✉️ Mail Support – send emails via SMTP or other mail services (configurable)
- 🌍 Multi-language Support – translations via JSON files for different languages
- ⚡ FastAPI – async backend with automatic OpenAPI docs
- 🗄️ Database-Agnostic – support for PostgreSQL, MySQL, SQLite, and MongoDB
- 🛠️ CLI Tool – manage project setup, dependencies, migrations, seeders, and server

## 🖼️ FastKit Admin Panel

![Login](static/assets/img/screenshots/login.png)
![Users](static/assets/img/screenshots/users.png)
![Edit user](static/assets/img/screenshots/edit-user.png)
![Create page](static/assets/img/screenshots/create-page.png)

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – modern async Python web framework 
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM (if you’re using it)  
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/getting-started/introduction/) – frontend UI

## 📁 File structure
```
fast-kit/
├── app
│   ├── infrastructure
│   │   └── database
│   │       └── connections
│   ├── middlewares
│   ├── migrations
│   │   └── versions
│   ├── models
│   ├── repositories
│   │   └── admin
│   ├── routers
│   │   ├── admin
│   │   └── api
│   ├── schemas
│   │   └── admin
│   ├── seeders
│   ├── services
│   │   └── admin
│   └── tests
│       └── unit
│           └── admin
├── static
│   └── assets
│       ├── css
│       ├── fonts
│       ├── img
│       │   └── screenshots
│       └── js
├── templates
│   └── admin
│       ├── auth
│       ├── emails
│       ├── pages
│       ├── partials
│       └── users
├── tools
│   └── cli
└── translations


```



## 🚀 Getting Started

### 1. Clone the repository
```
git clone https://github.com/radomirbrkovic/fast-kit.git
cd fast-kit
```

### 2. Run setup script

This will automatically:

- Create and activate the virtual environment

- Copy the .env file

- Install all dependencies
```
./tools/cli/setup.sh
```


### 3. Apply migrations

```
fastkit migrate
```


### 4. Run seeders

This will create a default admin user you can use to log in.

```
fastkit seed
```


### 5. Start the development server
```
fastkit run
```



Open in browser:
👉 http://localhost:8000

- Swagger UI → http://localhost:8000/docs
- Admin → http://localhost:8000/admin

## ⚡ CLI Tool

FastKit comes with a command-line tool to simplify common tasks:

| Command                  | Description                              |
| ------------------------ | ---------------------------------------- |
| `fastkit install`        | Install Python dependencies              |
| `fastkit run`            | Run FastAPI development server           |
| `fastkit makemigrations` | Generate Alembic migrations              |
| `fastkit migrate`        | Apply database migrations                |
| `fastkit rollback`       | Rollback last migration                  |
| `fastkit seed`           | Run seeders (creates default admin user) |
| `fastkit update`         | Pull latest project updates from git     |


⚠️ Note: Seeders and migrations will automatically detect the database driver from .env and work with PostgreSQL, MySQL, SQLite, or MongoDB (seeders only for MongoDB; migrations are SQL-only).

## 📝 License

This project is licensed under the [MIT License](https://opensource.org/license/MIT).