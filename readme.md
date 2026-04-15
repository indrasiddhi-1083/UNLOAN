# unloan (Secure OOP Python Structure)

## Structure
- `app/config.py` - configuration module (env-driven).
- `app/models/planner.py` - domain models (dataclasses).
- `app/services/planner_service.py` - planning engine and health score logic.
- `app/services/auth_service.py` - secure admin auth token service.
- `app/services/storage_service.py` - storage abstraction (local JSON).
- `app/routes/api.py` - backend API routes.
- `templates/index.html` - frontend page.
- `static/js/app.js` - frontend logic.
- `static/css/style.css` - frontend styling.
- `run.py` - app entrypoint.

## Run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Security notes
- Do not hardcode admin password. Set env var `UNLOAN_ADMIN_PASSWORD_HASH`.
- Generate password hash with Werkzeug in Python shell:
```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("your-strong-password"))
```
