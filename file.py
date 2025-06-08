import re
from docx import Document
from docx2pdf import convert
import os
import matplotlib.pyplot as plt
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generar_grafico(nombre_archivo):
    # Ejemplo de gráfica
    plt.figure()
    plt.plot([1, 2, 3, 4], [10, 20, 15, 25])
    plt.title("Ventas por trimestre")
    plt.xlabel("Trimestre")
    plt.ylabel("Ventas")
    plt.savefig(nombre_archivo)
    plt.close()

def reemplazar_llaves_y_exportar_pdf(path_docx, reemplazos, graficos={}, output_pdf_path=None):
    doc = Document(path_docx)
    
    def reemplazar_o_insertar(parrafo, reemplazos, graficos):
        for key, val in reemplazos.items():
            llave = f"[[{key}]]"
            if llave in parrafo.text:
                for run in parrafo.runs:
                    if llave in run.text:
                        run.text = run.text.replace(llave, val)

        for key, ruta_img in graficos.items():
            llave = f"[[{key}]]"
            if llave in parrafo.text:
                # Eliminar texto marcador y reemplazarlo con imagen
                for run in parrafo.runs:
                    if llave in run.text:
                        run.text = run.text.replace(llave, '')
                run = parrafo.add_run()
                run.add_picture(ruta_img, width=Inches(4))
                parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for parrafo in doc.paragraphs:
        reemplazar_o_insertar(parrafo, reemplazos, graficos)

    for tabla in doc.tables:
        for fila in tabla.rows:
            for celda in fila.cells:
                for parrafo in celda.paragraphs:
                    reemplazar_o_insertar(parrafo, reemplazos, graficos)

    temp_docx = "documento_modificado.docx"
    doc.save(temp_docx)

    if output_pdf_path is None:
        output_pdf_path = os.path.splitext(path_docx)[0] + "_modificado.pdf"
    convert(temp_docx, output_pdf_path)
    os.remove(temp_docx)

    return output_pdf_path


# Generar imagen de gráfico
ruta_grafico = "graficas/grf_juan_perez.png"
generar_grafico(ruta_grafico)

# Diccionarios
reemplazos = {
    "Nombre": "Juan Perez",
    "Fecha_assesment": "27 de abril del 2025",
    "Marca": "MARCA ejemplo",
    "Calif_total": "87"
}

graficos = {
    "Grafica": ruta_grafico
}

ruta_pdf = reemplazar_llaves_y_exportar_pdf("inf_delosi.docx", reemplazos, graficos)
print(f"PDF generado: {ruta_pdf}")
