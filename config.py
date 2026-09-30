from pathlib import Path
from dotenv import load_dotenv
import os


# ---------------------------------------------------------
# BASE DIRECTORY
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv(BASE_DIR / ".env")


# ---------------------------------------------------------
# DIRECTORIES
# ---------------------------------------------------------

STATIC_DIR = BASE_DIR / "static"

PANELS_DIR = STATIC_DIR / "panels"

EXPORTS_DIR = STATIC_DIR / "exports"

TEMPLATES_DIR = BASE_DIR / "templates"


# ---------------------------------------------------------
# API KEYS
# ---------------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
).strip()


HF_API_KEY = os.getenv(
    "HF_API_KEY",
    ""
).strip()


# ---------------------------------------------------------
# MODEL CONFIGURATION
# ---------------------------------------------------------

GEMINI_FLASH_MODEL = os.getenv(
    "GEMINI_FLASH_MODEL",
    "gemini-1.5-flash"
)


GEMINI_PRO_MODEL = os.getenv(
    "GEMINI_PRO_MODEL",
    "gemini-1.5-pro"
)


HF_IMAGE_MODEL = os.getenv(
    "HF_IMAGE_MODEL",
    "runwayml/stable-diffusion-v1-5"
)


# ---------------------------------------------------------
# IMAGE GENERATION MODE
# ---------------------------------------------------------

USE_LOCAL_DIFFUSERS = (
    os.getenv(
        "USE_LOCAL_DIFFUSERS",
        "false"
    ).lower()
    == "true"
)


# ---------------------------------------------------------
# SERVER
# ---------------------------------------------------------

HOST = os.getenv(
    "HOST",
    "127.0.0.1"
)


PORT = int(
    os.getenv(
        "PORT",
        "8000"
    )
)


# ---------------------------------------------------------
# CREATE REQUIRED DIRECTORIES
# ---------------------------------------------------------

PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)