import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
import os
from graficas import *

# Paso 1: Cargar los datos (supongamos que tenemos un DataFrame con información de cada persona)
data = {
    "Nombre": ["Juan", "Ana", "Pedro", "Laura"],
    "Edad": [28, 34, 45, 22],
    "Ventas": [200, 150, 300, 180]
}
df = pd.DataFrame(data)

# Función para crear un informe PDF
def crear_informe(pdf_filename, persona_data, grafico_img):
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    # Título
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, height - 40, f"Informe Personalizado de {persona_data['Nombre']}")
    
    # Información personal
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 80, f"Nombre: {persona_data['Nombre']}")
    c.drawString(100, height - 100, f"Edad: {persona_data['Edad']}")
    c.drawString(100, height - 120, f"Ventas: {persona_data['Ventas']}")
    
    # Insertar gráfico
    c.drawImage(grafico_img, 100, height - 300, width=400, height=200)
    
    c.save()

# Paso 2: Generar gráfico
grafico_path = barras_v_simple(df['Ventas'], df['Nombre'])

# Paso 3: Crear informe para una persona (por ejemplo, Juan)
persona_juan = df.iloc[0]  # Datos de Juan
crear_informe("informe_juan.pdf", persona_juan, grafico_path)

print("Informe PDF generado: informe_juan.pdf")

# Limpiar el archivo temporal de imagen después de crear el PDF
os.remove(grafico_path)
