# Cotización Dólar – Automatización

Script en Python que consume la API pública de dolarapi.com,
guarda las cotizaciones en un Excel y se ejecuta automáticamente
todos los días a las 9:20 con el Programador de tareas de Windows.

## Tecnologías
- Python, requests, openpyxl
- API REST (JSON)
- Programador de tareas de Windows

## Instalación
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python Main.py