# pip install requests openpyxl
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from openpyxl import Workbook, load_workbook

BASE = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE, ".env"))

URL = "https://dolarapi.com/v1/dolares"
ARCHIVO = os.path.join(BASE, "cotizaciones.xlsx")
LOG = os.path.join(BASE, "log.txt")
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def log(msg):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} - {msg}\n")


def enviar_telegram(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    r = requests.post(url, data={"chat_id": CHAT_ID, "text": texto}, timeout=10)
    r.raise_for_status()


def obtener_cotizaciones():
    r = requests.get(URL, timeout=10)
    r.raise_for_status()
    return r.json()


def guardar_excel(datos, ahora):
    if os.path.exists(ARCHIVO):
        wb = load_workbook(ARCHIVO)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.append(["Fecha", "Tipo", "Compra", "Venta"])
    for d in datos:
        ws.append([ahora, d["nombre"], d["compra"], d["venta"]])
    wb.save(ARCHIVO)


def armar_mensaje(datos, ahora):
    lineas = [f"💵 Cotizaciones {ahora}"]
    for d in datos:
        lineas.append(f"{d['nombre']}: compra ${d['compra']} / venta ${d['venta']}")
    return "\n".join(lineas)


def main():
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        datos = obtener_cotizaciones()
        guardar_excel(datos, ahora)
        enviar_telegram(armar_mensaje(datos, ahora))
        log(f"OK - {len(datos)} registros")
    except Exception as e:
        log(f"ERROR - {e}")
        try:
            enviar_telegram(f"⚠️ Falló la cotización: {e}")
        except Exception:
            pass


if __name__ == "__main__":
    main()