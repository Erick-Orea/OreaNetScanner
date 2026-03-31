import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "oreanetscanner.log")


if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def log(level, message):
    """
    Registra un evento en el archivo de log con formato profesional.
    Niveles: INFO, FOUND, WARNING, ERROR
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {level:<7} {message}\n"

    with open(LOG_FILE, "a") as f:
        f.write(entry)

def info(message):
    log("INFO", message)

def found(message):
    log("FOUND", message)

def warning(message):
    log("WARNING", message)

def error(message):
    log("ERROR", message)
