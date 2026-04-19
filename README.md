
# ⚡ DjangoForge

> **One command. Full Django setup. Ready to code.**

DjangoForge sets up a complete Django project in seconds — virtual environment, DRF, CORS, dotenv, .gitignore, requirements.txt, and a beautiful welcome page. All automatically.

---

## 🚀 Installation

```bash
pip install djangoforge
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

Then open **http://127.0.0.1:8000** — DjangoForge welcome page milega! 🎉

---

## 🛠️ settings.py auto-configuration

DjangoForge automatically adds:
- `rest_framework` and `corsheaders` to `INSTALLED_APPS`
- `CorsMiddleware` at top of `MIDDLEWARE`
- `REST_FRAMEWORK` config
- `CORS_ALLOWED_ORIGINS` for localhost:3000 and localhost:5173
- `load_dotenv()` for .env support

---

Made with ❤️ by DjangoForge
=======
# djangoforge
>>>>>>> dbcd5fc8ed90081457ad9ed6e3a1a5bc2fa3082f
