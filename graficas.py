import matplotlib.pyplot as plt, io

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




