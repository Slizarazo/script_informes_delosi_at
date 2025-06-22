import os, io
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties
from matplotlib.table import Table
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
from matplotlib.colors import to_rgb

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

def plot_ponderado(df, nombre, marca):
    """
    df: DataFrame con columnas ['dimensionchildname', 'dimensionparentname', 'answerscore']
    nombre: Nombre del archivo PNG a guardar (sin extensión)
    marca: Nombre de la carpeta de la marca donde se guardará la imagen
    """

    resultados = []
    for child in df['dimensionchildname'].unique():
        sub_df = df[df['dimensionchildname'] == child]
        caso_practico = sub_df['answerscore'][sub_df['dimensionparentname'] == "Caso Práctico"].mean()
        conocimiento = sub_df['answerscore'][sub_df['dimensionparentname'] == "Conocimiento"].mean()
        ponderado = 0.7 * caso_practico + 0.3 * conocimiento
        resultados.append({'dimensionchildname': child, 'Puntuación ponderada': ponderado})

    result_df = pd.DataFrame(resultados).sort_values('Puntuación ponderada', ascending=False)

    alto = max(4, len(result_df) * 0.6)
    fig, ax = plt.subplots(figsize=(10, alto))  # Aumentamos el ancho a 10 para más espacio a la derecha

    bars = ax.barh(result_df['dimensionchildname'], result_df['Puntuación ponderada'],
                   color='#357088', edgecolor='gray')

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.5, bar.get_y() + bar.get_height()/2,
                f'{width:.1f}', va='center', fontsize=10, color='#357088')

    # Eliminar ejes y títulos
    ax.set_ylabel('')
    ax.set_xlabel('')
    ax.tick_params(axis='x', bottom=False, labelbottom=False)
    ax.invert_yaxis()

    # Maximizar uso del espacio visual
    plt.subplots_adjust(left=0.01, right=0.98, top=0.97, bottom=0.03)

    # Nota inferior derecha
    fig.text(0.98, 0.01, 'Valor aspiracional: 100', ha='right', fontsize=9, color='gray')

    # Guardar imagen
    base_dir = os.path.join('graficas', 'distribucion_de_resultados_ponderados_por_capacidad', marca)
    os.makedirs(base_dir, exist_ok=True)
    output_path = os.path.join(base_dir, f'{nombre}.png')

    plt.savefig(output_path, dpi=400, bbox_inches='tight')
    plt.close()

    print(f'✅ Gráfico guardado en: {output_path}')

def plot_por_questionblock(df, usuario, marca):
    """
    df: DataFrame con columnas ['questionblockname', 'dimensionparentname', 'answerscore', 'evaluatedemployeedisplayname']
    usuario: nombre exacto del usuario a graficar
    marca: nombre de la marca (usado como subcarpeta)
    """
    df_usuario = df[df['evaluatedemployeedisplayname'] == usuario]
    questionblocks = df_usuario['questionblockname'].unique()

    resultados = []
    for bloque in questionblocks:
        sub_df = df_usuario[df_usuario['questionblockname'] == bloque]
        caso_practico = sub_df['answerscore'][sub_df['dimensionparentname'] == "Caso Práctico"].mean()
        conocimiento = sub_df['answerscore'][sub_df['dimensionparentname'] == "Conocimiento"].mean()
        ponderado = 0.7 * caso_practico + 0.3 * conocimiento
        resultados.append({'questionblockname': bloque, 'Puntuación ponderada': ponderado})

    result_df = pd.DataFrame(resultados).sort_values('Puntuación ponderada', ascending=False)

    colores = ['#0b5d78' if x >= 70 else '#e9f0f7' for x in result_df['Puntuación ponderada']]
    textos = ['white' if x >= 70 else '#4e5b7c' for x in result_df['Puntuación ponderada']]
    bordes = ['#0b5d78' if x >= 70 else '#d0d8e4' for x in result_df['Puntuación ponderada']]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.grid(False)

    bars = ax.bar(result_df['questionblockname'], result_df['Puntuación ponderada'],
                  color=colores, edgecolor=bordes, linewidth=1.5)

    for bar, texto, val in zip(bars, textos, result_df['Puntuación ponderada']):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height/2, f'{val:.1f}',
                ha='center', va='center', fontsize=10, color=texto, weight='bold')

    ax.tick_params(axis='y', left=False, labelleft=False)
    plt.xticks(rotation=0, ha='center')
    plt.tight_layout()

    # Crear ruta para guardar imagen
    carpeta = os.path.join('graficas', 'distribucion_de_resultados_ponderados_por_fase', marca)
    os.makedirs(carpeta, exist_ok=True)
    ruta_guardado = os.path.join(carpeta, f'{usuario}.png')

    plt.savefig(ruta_guardado, dpi=300)
    plt.close()

def generar_tabla_como_imagen(df, usuario: str, marca: str):
    # Crear carpeta y ruta de salida
    carpeta = os.path.join('graficas', 'distribucion_por_capacidad_y_fase', marca)
    os.makedirs(carpeta, exist_ok=True)
    ruta_guardado = os.path.join(carpeta, f'{usuario}.png')

    # Crear tabla pivote
    tabla = df.pivot_table(
        index=['questionblockname', 'dimensionparentname'],
        columns='dimensionchildname',
        values='answerscore',
        aggfunc='mean'
    ).reset_index()

    tabla['Total'] = tabla.iloc[:, 2:].mean(axis=1)

    # Agregar totales
    caso_total = df[df['dimensionparentname'] == 'Caso Práctico'].pivot_table(
        index='dimensionchildname', values='answerscore', aggfunc='mean').T
    conoc_total = df[df['dimensionparentname'] == 'Conocimiento'].pivot_table(
        index='dimensionchildname', values='answerscore', aggfunc='mean').T
    pond_total = 0.7 * caso_total + 0.3 * conoc_total

    for t, label in zip([caso_total, conoc_total, pond_total], ['Caso', 'Conoc.', 'Pond.']):
        t['questionblockname'] = 'Total'
        t['dimensionparentname'] = label
        t['Total'] = t.mean(numeric_only=True, axis=1)

    totales = pd.concat([caso_total, conoc_total, pond_total], ignore_index=True)
    tabla = pd.concat([tabla, totales], ignore_index=True)

    columnas_ordenadas = ['questionblockname', 'dimensionparentname'] + sorted(
        [c for c in tabla.columns if c not in ['questionblockname', 'dimensionparentname', 'Total']]
    ) + ['Total']
    tabla = tabla[columnas_ordenadas]

    # Parámetros visuales
    fontsize = 22
    num_columnas = len(tabla.columns)
    ancho_pulg = 8.5
    alto_pulg = 16
    dpi = 300

    fig, ax = plt.subplots(figsize=(ancho_pulg, alto_pulg), dpi=dpi)
    ax.axis('off')

    table_data = [tabla.columns.tolist()] + tabla.round(2).fillna('').values.tolist()
    tabla_visual = ax.table(
        cellText=table_data,
        loc='center',
        cellLoc='center',
        colWidths=[1.0 / num_columnas] * num_columnas
    )

    font_prop = FontProperties()
    font_prop.set_size(fontsize)

    for (i, j), cell in tabla_visual.get_celld().items():
        cell.set_fontsize(fontsize)
        cell.set_text_props(fontproperties=font_prop)
        cell.set_linewidth(0.7)

        if i == 0:
            cell.set_facecolor('#204d74')
            cell.set_text_props(color='white', weight='bold')
        else:
            try:
                valor = float(cell.get_text().get_text())
                if valor == 100:
                    cell.set_facecolor('#00cc44')
                elif valor >= 65:
                    cell.set_facecolor('#99e699')
                elif valor == 0:
                    cell.set_facecolor('#ffcccc')
                else:
                    cell.set_facecolor('#ffffff')
            except:
                cell.set_facecolor('#f0f0f0')

    plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    plt.savefig(ruta_guardado, dpi=dpi)
    plt.close()

    return ruta_guardado

def crear_tabla_distribucion_v4(df, usuario, marca):
    df_usuario = df[df["evaluatedemployeedisplayname"] == usuario]

    capacidades = ["Planeación", "Mejora Continua", "Ejecución", "Control"]
    bloques = [
        "Capacidad de Adaptación",
        "Conexión Humana",
        "Diálogo Constructivo",
        "Gestión Eficaz",
        "Pensamiento Crítico"
    ]

    resultados = []
    for capacidad in capacidades:
        df_cap = df_usuario[df_usuario["dimensionchildname"] == capacidad]
        fila_caso, fila_conoc, fila_pond = [f"{capacidad} Caso"], [f"{capacidad} Conoc."], [f"{capacidad} Ponde."]

        for bloque in bloques:
            caso = df_cap.query("dimensionparentname == 'Caso Práctico' and questionblockname == @bloque")["answerscore"].mean()
            conoc = df_cap.query("dimensionparentname == 'Conocimiento' and questionblockname == @bloque")["answerscore"].mean()
            pond = 0.7 * caso + 0.3 * conoc if not np.isnan(caso) and not np.isnan(conoc) else np.nan
            fila_caso.append(round(caso, 2) if not np.isnan(caso) else 0)
            fila_conoc.append(round(conoc, 2) if not np.isnan(conoc) else 0)
            fila_pond.append(round(pond, 2) if not np.isnan(pond) else 0)

        for fila in [fila_caso, fila_conoc, fila_pond]:
            fila.append(round(np.mean(fila[1:]), 2))
            resultados.append(fila)

    total_caso = ["Total Caso"]
    total_conoc = ["Total Conoc."]
    total_pond = ["Total Ponde."]

    for i in range(1, len(bloques) + 1):
        valores_caso = [fila[i] for fila in resultados if "Caso" in fila[0]]
        valores_conoc = [fila[i] for fila in resultados if "Conoc." in fila[0]]
        valores_pond = [fila[i] for fila in resultados if "Ponde." in fila[0]]
        total_caso.append(round(np.mean(valores_caso), 2))
        total_conoc.append(round(np.mean(valores_conoc), 2))
        total_pond.append(round(np.mean(valores_pond), 2))

    total_caso.append(round(np.mean(total_caso[1:]), 2))
    total_conoc.append(round(np.mean(total_conoc[1:]), 2))
    total_pond.append(round(np.mean(total_pond[1:]), 2))
    resultados.extend([total_caso, total_conoc, total_pond])

    # Encabezados con salto de línea manual para visualización en dos líneas
    columnas = [
        "Capacidad",
        "Capacidad\nAdaptación",
        "Conexión\nHumana",
        "Diálogo\nConstructivo",
        "Gestión\nEficaz",
        "Pensamiento\nCrítico",
        "Total"
    ]
    df_tabla = pd.DataFrame(resultados, columns=columnas)

    # Solo aplicar división a la primera columna
    def dividir_lineas(texto, max_palabras=2):
        palabras = texto.split()
        if len(palabras) > max_palabras:
            return " ".join(palabras[:max_palabras]) + "\n" + " ".join(palabras[max_palabras:])
        return texto

    df_tabla["Capacidad"] = df_tabla["Capacidad"].apply(dividir_lineas)

    carpeta = os.path.join('graficas', 'distribucion_por_capacidad_y_fase', marca)
    os.makedirs(carpeta, exist_ok=True)
    ruta_guardado = os.path.join(carpeta, f'{usuario}.png')

    fig = Figure(figsize=(10, 7))  # altura aumentada
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.set_axis_off()
    table = Table(ax, bbox=[0, 0, 1, 1])

    def color_fondo(valor):
        if valor == 0:
            return "#ffffff"
        elif valor < 50:
            return "#f4cccc"
        elif valor < 70:
            return "#fff2cc"
        else:
            return "#d9ead3"

    nrows, ncols = df_tabla.shape
    width, height = 1.3 / ncols, 1.7 / nrows

    for i in range(nrows):
        for j in range(ncols):
            val = df_tabla.iat[i, j]
            txt = str(val)
            bgcolor = "#c9daf8" if j == 0 else color_fondo(val)
            cell = table.add_cell(i, j, width, height, text=txt, loc='center', facecolor=bgcolor)
            cell.get_text().set_fontsize(12)
            cell.get_text().set_weight("bold")
            cell.PAD = 0.08

    for j in range(ncols):
        cell = table.add_cell(-1, j, width, height, text=df_tabla.columns[j], loc='center', facecolor="#6fa8dc")
        cell.get_text().set_fontsize(12)
        cell.get_text().set_weight("bold")
        cell.PAD = 0.12

    ax.add_table(table)
    fig.savefig(ruta_guardado, dpi=150)
    return ruta_guardado

def calcular_y_graficar_tarjetas(df, usuario, marca):
    # Filtrar los datos de esa marca
    data = df[df["marca"] == marca]

    # Calcular promedios
    promedio_caso = data[data["dimensionparentname"] == "Caso Práctico"]["answerscore"].mean()
    promedio_conoc = data[data["dimensionparentname"] == "Conocimiento"]["answerscore"].mean()
    ponderado_total = 0.7 * promedio_caso + 0.3 * promedio_conoc

    # Calcular valores comparativos (simulación de contexto más amplio)
    df_ponderado = []
    for m in df["Marca"].unique():
        d = df[df["Marca"] == m]
        c = d[d["dimensionparentname"] == "Caso Práctico"]["answerscore"].mean()
        k = d[d["dimensionparentname"] == "Conocimiento"]["answerscore"].mean()
        df_ponderado.append(0.7 * c + 0.3 * k)
    promedio_marca = np.mean(df_ponderado)

    # Ponderado promedio UN (si tienes otra columna como "Unidad de Negocio", puedes hacer lo mismo allí)
    promedio_un = df[df["dimensionparentname"].isin(["Caso Práctico", "Conocimiento"])]["answerscore"].mean()

    # Crear carpeta y ruta
    carpeta = os.path.join('graficas', 'comparativa_de_resultados', marca)
    os.makedirs(carpeta, exist_ok=True)
    ruta_guardado = os.path.join(carpeta, f'{usuario}.png')

    # Crear la imagen tipo tarjeta
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.5))
    colores = ["#6A1B9A", "#AB47BC", "#AB47BC"]
    titulos = ["Calificación Total", "Calificación promedio de la marca", "Calificación promedio de la UN"]
    valores = [ponderado_total, promedio_marca, promedio_un]

    for i, ax in enumerate(axs):
        ax.set_facecolor(colores[i])
        ax.text(0.5, 0.6, f"{valores[i]:.2f}", ha='center', va='center', fontsize=28, fontweight='bold', color='white')
        ax.text(0.5, 0.25, titulos[i], ha='center', va='center', fontsize=14, color='white')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        for spine in ax.spines.values():
            spine.set_visible(False)

    plt.tight_layout()
    fig.savefig(ruta_guardado, dpi=150, bbox_inches='tight')
    plt.close(fig)

    return ruta_guardado






