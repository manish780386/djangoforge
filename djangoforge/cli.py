import os
import sys
import subprocess
import venv
import argparse

# ─── Colors for terminal ──────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def log(msg):   print(f"{GREEN}  ✔  {msg}{RESET}")
def info(msg):  print(f"{CYAN}  ➤  {msg}{RESET}")
def warn(msg):  print(f"{YELLOW}  ⚠  {msg}{RESET}")
def error(msg): print(f"{RED}  ✘  {msg}{RESET}")

BANNER = f"""
{CYAN}{BOLD}
  ██████╗      ██╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
  ██╔══██╗     ██║██╔══██╗████╗  ██║██╔════╝ ██╔═══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
  ██║  ██║     ██║███████║██╔██╗ ██║██║  ███╗██║   ██║█████╗  ██║   ██║██████╔╝██║  ███╗█████╗
  ██║  ██║██   ██║██╔══██║██║╚██╗██║██║   ██║██║   ██║██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
  ██████╔╝╚█████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
  ╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
{RESET}
{BOLD}              ⚡  Django + DRF + CORS + Env — One Command Setup  ⚡{RESET}
"""

# ─── File Templates ───────────────────────────────────────────────────────────

def get_settings_patch():
    return '''
# ════════════════════════════════════════════════
# ⚡ DjangoForge Auto-Configuration
# ════════════════════════════════════════════════
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)
DEBUG = os.environ.get("DEBUG", "True") == "True"

INSTALLED_APPS += [
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}
# ════════════════════════════════════════════════
'''

ENV_TEMPLATE = """\
# ⚡ DjangoForge Generated .env
SECRET_KEY=your-very-secret-key-change-this-in-production
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
"""

GITIGNORE_TEMPLATE = """\
# ⚡ DjangoForge Generated .gitignore

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg
*.egg-info/
dist/
build/
*.whl

# Virtual Environment
venv/
env/
.venv/

# Django
*.log
*.pot
db.sqlite3
media/
staticfiles/

# Environment Variables
.env
.env.*
!.env.example

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
"""

WELCOME_VIEW = '''\
from django.http import HttpResponse

def welcome(request):
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>DjangoForge</title>
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      min-height: 100vh;
      background: #0d0d0d;
      color: #f0f0f0;
      font-family: 'Space Grotesk', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
    }
    .container { width: 100%; max-width: 720px; }

    /* Header */
    .header {
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 32px;
      padding-bottom: 24px;
      border-bottom: 1px solid #1f1f1f;
    }
    .logo {
      width: 52px; height: 52px;
      background: #1a1a1a;
      border: 1px solid #2a2a2a;
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      font-size: 24px;
    }
    .header-text h1 { font-size: 1.6rem; font-weight: 700; color: #f0f0f0; letter-spacing: -0.5px; }
    .header-text p { font-size: 0.85rem; color: #666; margin-top: 3px; }

    /* Badge */
    .badge {
      display: inline-flex; align-items: center; gap: 7px;
      background: #0d2e1a;
      border: 1px solid #1a5c33;
      border-radius: 20px;
      padding: 5px 14px;
      font-size: 0.78rem; font-weight: 500;
      color: #4ade80;
      margin-bottom: 24px;
    }
    .dot { width: 7px; height: 7px; border-radius: 50%; background: #4ade80; animation: blink 1.4s ease-in-out infinite; }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

    /* Feature grid */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      margin-bottom: 24px;
    }
    .card {
      background: #141414;
      border: 1px solid #1f1f1f;
      border-radius: 12px;
      padding: 16px 14px;
      transition: border-color 0.2s, background 0.2s;
    }
    .card:hover { background: #1a1a1a; border-color: #2f2f2f; }
    .card .icon { font-size: 1.3rem; margin-bottom: 8px; display: block; }
    .card .name { font-size: 0.82rem; font-weight: 600; color: #e0e0e0; }
    .card .desc { font-size: 0.72rem; color: #555; margin-top: 3px; }

    /* Steps */
    .steps {
      background: #111;
      border: 1px solid #1f1f1f;
      border-radius: 14px;
      padding: 22px 24px;
      margin-bottom: 24px;
    }
    .steps-title {
      font-size: 0.7rem; font-weight: 600;
      color: #444;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 16px;
    }
    .step { display: flex; gap: 12px; align-items: flex-start; margin-bottom: 12px; }
    .step:last-child { margin-bottom: 0; }
    .step-num {
      width: 22px; height: 22px;
      border-radius: 50%;
      background: #1a2e4a;
      border: 1px solid #1e4080;
      color: #60a5fa;
      font-size: 0.72rem; font-weight: 700;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; margin-top: 1px;
    }
    .step-text { font-size: 0.83rem; color: #888; line-height: 1.6; }
    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      background: #1a1a1a;
      border: 1px solid #2a2a2a;
      border-radius: 5px;
      padding: 1px 7px;
      color: #a3e635;
    }

    /* Footer */
    .footer {
      text-align: center;
      font-size: 0.72rem;
      color: #333;
      padding-top: 20px;
      border-top: 1px solid #1a1a1a;
      letter-spacing: 1px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="logo">⚡</div>
      <div class="header-text">
        <h1>DjangoForge</h1>
        <p>Forge your backend instantly</p>
      </div>
    </div>

    <div class="badge">
      <div class="dot"></div>
      Server running
    </div>

    <div class="grid">
      <div class="card"><span class="icon">🐍</span><div class="name">Django</div><div class="desc">Web framework</div></div>
      <div class="card"><span class="icon">🔌</span><div class="name">DRF</div><div class="desc">REST APIs</div></div>
      <div class="card"><span class="icon">🌐</span><div class="name">CORS</div><div class="desc">Cross origin</div></div>
      <div class="card"><span class="icon">🔐</span><div class="name">.env</div><div class="desc">Secrets safe</div></div>
      <div class="card"><span class="icon">📦</span><div class="name">Venv</div><div class="desc">Isolated env</div></div>
      <div class="card"><span class="icon">🚫</span><div class="name">.gitignore</div><div class="desc">Git ready</div></div>
    </div>

    <div class="steps">
      <div class="steps-title">Next steps</div>
      <div class="step"><div class="step-num">1</div><div class="step-text">Run migrations — <code>python manage.py migrate</code></div></div>
      <div class="step"><div class="step-num">2</div><div class="step-text">Create admin user — <code>python manage.py createsuperuser</code></div></div>
      <div class="step"><div class="step-num">3</div><div class="step-text">Update <code>.env</code> with a strong <code>SECRET_KEY</code> before production</div></div>
      <div class="step"><div class="step-num">4</div><div class="step-text">Open Django admin panel at <code>/admin</code></div></div>
    </div>

    <div class="footer">Built with ⚡ DjangoForge &nbsp;·&nbsp; Happy coding!</div>
  </div>
</body>
</html>
"""
    return HttpResponse(html)
'''

URLS_CONTENT = """\
from django.contrib import admin
from django.urls import path
from .welcome import welcome

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", welcome),
]
"""

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_venv_paths(venv_dir):
    if sys.platform == "win32":
        pip          = os.path.join(venv_dir, "Scripts", "pip.exe")
        python       = os.path.join(venv_dir, "Scripts", "python.exe")
        django_admin = os.path.join(venv_dir, "Scripts", "django-admin.exe")
    else:
        pip          = os.path.join(venv_dir, "bin", "pip")
        python       = os.path.join(venv_dir, "bin", "python")
        django_admin = os.path.join(venv_dir, "bin", "django-admin")
    return pip, python, django_admin


def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        error(f"Failed: {' '.join(str(c) for c in cmd)}")
        print(result.stderr)
        sys.exit(1)
    return result


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ─── Main Setup ───────────────────────────────────────────────────────────────

def create_project(project_name: str):
    print(BANNER)

    project_dir = os.path.abspath(project_name)
    venv_dir    = os.path.join(project_dir, "venv")
    inner_dir   = os.path.join(project_dir, project_name)

    print(f"\n{BOLD}  Project : {CYAN}{project_name}{RESET}")
    print(f"{BOLD}  Location: {CYAN}{project_dir}{RESET}\n")

    # 1. Project folder
    os.makedirs(project_dir, exist_ok=True)
    log("Project folder created")

    # 2. Virtual environment
    info("Creating virtual environment...")
    venv.create(venv_dir, with_pip=True)
    log("Virtual environment created → venv/")

    pip, python, django_admin = get_venv_paths(venv_dir)

    # 3. Upgrade pip
    run_cmd([python, "-m", "pip", "install", "--upgrade", "pip"])

    # 4. Install packages
    packages = [
        ("django",              "Django"),
        ("djangorestframework", "Django REST Framework"),
        ("django-cors-headers", "CORS Headers"),
        ("python-dotenv",       "Python Dotenv"),
    ]
    for pkg, label in packages:
        info(f"Installing {label}...")
        run_cmd([pip, "install", pkg])
        log(f"{label} installed")

    # 5. Create Django project
    info("Creating Django project...")
    run_cmd([django_admin, "startproject", project_name, project_dir])
    log("Django project scaffolded")

    # 6. Patch settings.py
    info("Configuring settings.py (DRF + CORS + dotenv)...")
    settings_path = os.path.join(inner_dir, "settings.py")
    with open(settings_path, "a", encoding="utf-8") as f:
        f.write(get_settings_patch())
    log("settings.py configured")

    # 7. Welcome page
    info("Adding DjangoForge welcome page...")
    write_file(os.path.join(inner_dir, "welcome.py"), WELCOME_VIEW)
    write_file(os.path.join(inner_dir, "urls.py"),    URLS_CONTENT)
    log("Welcome page ready")

    # 8. .env
    info("Creating .env file...")
    write_file(os.path.join(project_dir, ".env"), ENV_TEMPLATE)
    log(".env file created")

    # 9. .gitignore
    info("Creating .gitignore...")
    write_file(os.path.join(project_dir, ".gitignore"), GITIGNORE_TEMPLATE)
    log(".gitignore created")

    # 10. requirements.txt
    info("Creating requirements.txt...")
    result = subprocess.run([pip, "freeze"], capture_output=True, text=True)
    write_file(os.path.join(project_dir, "requirements.txt"), result.stdout)
    log("requirements.txt created")

    # ── Done ──────────────────────────────────────────────────────────────────
    print(f"""
{CYAN}{BOLD}
  ════════════════════════════════════════════════════
   ⚡  DjangoForge Setup Complete!
  ════════════════════════════════════════════════════{RESET}

  {BOLD}Project structure:{RESET}
  {project_name}/
  ├── venv/                  ← Virtual environment
  ├── {project_name}/
  │   ├── settings.py        ← DRF + CORS configured ✔
  │   ├── urls.py            ← Welcome page routed  ✔
  │   └── welcome.py         ← DjangoForge page      ✔
  ├── manage.py
  ├── .env                   ← Environment variables ✔
  ├── .gitignore             ← Git ignore rules      ✔
  └── requirements.txt       ← All dependencies      ✔

  {BOLD}Run these commands now:{RESET}

    {CYAN}cd {project_name}{RESET}

    {YELLOW}# Windows:{RESET}
    {CYAN}venv\\Scripts\\activate{RESET}

    {YELLOW}# Mac / Linux:{RESET}
    {CYAN}source venv/bin/activate{RESET}

    {CYAN}python manage.py migrate{RESET}
    {CYAN}python manage.py runserver{RESET}

  {GREEN}{BOLD}Open: http://127.0.0.1:8000  🚀{RESET}
""")


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="djangoforge",
        description="⚡ DjangoForge — Instant Django project setup"
    )
    parser.add_argument("project_name", help="Name of your Django project")
    args = parser.parse_args()

    name = args.project_name.strip()
    if not name.isidentifier():
        error(f"'{name}' is not a valid project name. Use only letters, numbers, underscores.")
        sys.exit(1)

    create_project(name)


if __name__ == "__main__":
    main()