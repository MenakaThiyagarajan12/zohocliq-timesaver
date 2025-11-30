# backend/config.py
import os

class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 10000))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(os.getcwd(), "uploads"))

    @staticmethod
    def ensure_dirs():
        if not os.path.exists(Config.UPLOAD_DIR):
            os.makedirs(Config.UPLOAD_DIR, exist_ok=True)

Config.ensure_dirs()

