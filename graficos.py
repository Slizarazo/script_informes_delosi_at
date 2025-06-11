import matplotlib.pyplot as plt, io
import os

# Función para generar gráfico
def barras_v_simple(ventas, personas):
    plt.figure(figsize=(6, 4))
    plt.bar(range(len(ventas)), ventas, color='skyblue')
    plt.title("Ventas por persona")
    plt.xlabel("Persona")
    plt.ylabel("Ventas")
    plt.xticks(range(len(ventas)), personas)
    
    # Guardar el gráfico como archivo temporal
    img_path = "grafico_temp.png"
    plt.savefig(img_path, format='png')
    plt.close()
    return img_path

def generate_chart():
    """Genera una gráfica simple y la devuelve como un objeto BytesIO."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 20, 25, 30], marker='o')
    ax.set_title("Ejemplo de Gráfica")
    
    image_stream = io.BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    return image_stream

def generar_grafico(nombre_archivo):
    # Ejemplo de gráfica
    plt.figure()
    plt.plot([1, 2, 3, 4], [10, 20, 15, 25])
    plt.title("Ventas por trimestre")
    plt.xlabel("Trimestre")
    plt.ylabel("Ventas")
    plt.savefig(nombre_archivo)
    plt.close()

def mostrar_tarjetas(p_caso_practico, p_conocimiento, nombre, marca, peso_caso=0.7, guardar=True):
    # Cálculo de la puntuación ponderada
    calificacion_total = peso_caso * p_caso_practico + (1 - peso_caso) * p_conocimiento

    # Datos y etiquetas
    valores = [round(calificacion_total, 2), round(p_caso_practico, 2), round(p_conocimiento, 2)]
    titulos = ['Calificación Total', f'Práctico ({int(peso_caso*100)}%)', 'Promedio Conocimiento']
    colores = ['#764BA2', '#A64AC9', '#B06AB3']

    # Ajustes visuales
    n = len(valores)
    ancho_tarjeta = 2.2        # Más ancho
    espaciado = 0.5             # Más separación
    alto_tarjeta = 1.5
    total_ancho = n * ancho_tarjeta + (n - 1) * espaciado  # Total dinámico

    # Crear figura en tamaño carta
    fig, ax = plt.subplots(figsize=(8, 1.3))
    ax.axis('off')

    for i, (valor, titulo, color) in enumerate(zip(valores, titulos, colores)):
        left = i * (ancho_tarjeta + espaciado) + (8.5 - total_ancho) / 2
        tarjeta = plt.Rectangle((left, 0), ancho_tarjeta, alto_tarjeta, color=color, ec='white', lw=2)
        ax.add_patch(tarjeta)

        # Número grande en negrita
        ax.text(left + ancho_tarjeta / 2, 1.2, f'{valor}',
                ha='center', va='center', fontsize=18, color='white', weight='bold')

        # Subtítulo
        ax.text(left + ancho_tarjeta / 2, 0.6, titulo,
                ha='center', va='center', fontsize=10, color='white')

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 1.5)
    plt.tight_layout()

    if guardar:
        carpeta = os.path.join("graficas", "calificacion_global", marca)
        os.makedirs(carpeta, exist_ok=True)
        ruta_archivo = os.path.join(carpeta, f"{nombre}.png")
        plt.savefig(ruta_archivo, dpi=300, bbox_inches='tight')
        print(f"✅ Imagen guardada en: {ruta_archivo}")

    plt.close(fig)





