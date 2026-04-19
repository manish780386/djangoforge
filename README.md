# ⚡ DjangoForge

> **One command. Full Django setup. Ready to code.**

DjangoForge sets up a complete Django project in seconds — virtual environment, DRF, CORS, dotenv, .gitignore, requirements.txt, and a beautiful welcome page. All automatically.

---

## 🚀 Installation

```bash
pip install django-forgekit
```

## ⚡ Usage

```bash
djangoforge myproject
```

That's it. One command.

---

## ✅ What gets created?

```
myproject/
├── venv/                  ← Virtual environment (auto-created)
├── myproject/
│   ├── settings.py        ← DRF + CORS + dotenv configured
│   ├── urls.py            ← Welcome page routed
│   └── welcome.py         ← DjangoForge branded welcome view
├── manage.py
├── .env                   ← Environment variables
├── .gitignore             ← Git ignore rules
└── requirements.txt       ← All dependencies
```

---

## 📦 Auto-installed packages

| Package | Purpose |
|---|---|
| Django | Web framework |
| djangorestframework | REST API support |
| django-cors-headers | CORS configuration |
| python-dotenv | .env file support |

---

## ▶️ After setup

```bash
cd myproject

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate

python manage.py migrate
python manage.py runserver
```

Open **http://127.0.0.1:8000** —  

---

## 🛠️ Auto-configured in settings.py

| Setting | Value |
|---|---|
| `INSTALLED_APPS` | `rest_framework`, `corsheaders` added |
| `MIDDLEWARE` | `CorsMiddleware` added at top |
| `CORS_ALLOWED_ORIGINS` | localhost:3000, localhost:5173 |
| `REST_FRAMEWORK` | Default permission & auth classes |
| `load_dotenv()` | .env file loaded automatically |

---

## 👨‍💻 Author

Made with ❤️ by **Manish Dange**

GitHub: [manishdange](https://github.com/manish780386/)