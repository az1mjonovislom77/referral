import os

port = os.environ.get("PORT", "8000")
os.system(f"gunicorn projectm.wsgi:application --bind 0.0.0.0:{port}")
