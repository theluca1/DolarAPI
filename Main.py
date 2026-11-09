# pip install requests openpyxl
import requests
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os

URL = "https://dolarapi.com/v1/dolares"
ARCHIVO = "cotizaciones.xlsx"

datos = requests.get(URL, timeout=10).json()

if os.path.exists(ARCHIVO):
    wb = load_workbook(ARCHIVO); ws = wb.active
else:
    wb = Workbook(); ws = wb.active
    ws.append(["Fecha", "Tipo", "Compra", "Venta"])

ahora = datetime.now().strftime("%Y-%m-%d %H:%M")
for d in datos:
    ws.append([ahora, d["nombre"], d["compra"], d["venta"]])

wb.save(ARCHIVO)
print("Listo:", len(datos), "registros")