import json
import csv
import os
from logger import info, error

EXPORT_DIR = "exports"

if not os.path.exists(EXPORT_DIR):
    os.makedirs(EXPORT_DIR)


def export_txt(filename, data):
    try:
        path = os.path.join(EXPORT_DIR, filename + ".txt")
        with open(path, "w") as f:
            f.write("=== Resultados de OreaNet Scanner ===\n\n")
            for key, value in data.items():
                f.write(f"{key}: {value}\n")

        info(f"Resultados exportados a TXT: {path}")
        print(f"[+] Exportado correctamente a {path}")

    except Exception as e:
        error(f"Error exportando TXT: {e}")


def export_json(filename, data):
    try:
        path = os.path.join(EXPORT_DIR, filename + ".json")
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        info(f"Resultados exportados a JSON: {path}")
        print(f"[+] Exportado correctamente a {path}")

    except Exception as e:
        error(f"Error exportando JSON: {e}")


def export_csv(filename, data):
    try:
        path = os.path.join(EXPORT_DIR, filename + ".csv")
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Clave", "Valor"])
            for key, value in data.items():
                writer.writerow([key, value])

        info(f"Resultados exportados a CSV: {path}")
        print(f"[+] Exportado correctamente a {path}")

    except Exception as e:
        error(f"Error exportando CSV: {e}")
