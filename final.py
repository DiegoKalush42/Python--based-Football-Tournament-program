import tkinter as tk
from tkinter import messagebox  
from tkinter import ttk 
import random
import os
import json


# Definimos  la ruta al archivo donde se guardarán los datos, lo hacemos en aun archovo json
nombre_archivo = 'tabla_clasificacion.json'
ruta_archivo = os.path.join(os.path.expanduser('~'), nombre_archivo)



equipos_grupo1 = ['Stoli', 'RUP FC', 'Maristas FC', 'La Talacha', 'Prax FC', 'Inter de Rodín', 'Krakens', 'Crudos FC', 'Jojutla', 'Mamitas Puebla FC']
equipos_grupo2 = ['All Star Mixoac', 'Schweeppes', 'Cuervos negros', 'Buque Camaronero', 'CF Sagrev', 'CF Real Mixoac', 'Equipo nuevo 1', 'Equipo nuevo 2', 'Equipo 19', 'Equipo 20']


datos_liga = {
    "tabla_clasificacion": {},
    "jornadas_grupo1": [],
    "jornadas_grupo2": [],
    "calendario_grupo1": [],
    "calendario_grupo2": []
}


tabla_clasificacion = datos_liga['tabla_clasificacion']
jornadas_grupo1 = datos_liga['jornadas_grupo1']
jornadas_grupo2 = datos_liga['jornadas_grupo2']
calendario_grupo1=datos_liga['calendario_grupo1'] 
calendario_grupo2=datos_liga['calendario_grupo2'] 



# Función para guardar la tabla de clasificación en un archivo
def guardar_datos():
    # Prepara los datos para guardar
    datos_liga['tabla_clasificacion'] = tabla_clasificacion
    datos_liga['jornadas_grupo1'] = datos_liga['jornadas_grupo1']
    datos_liga['jornadas_grupo2'] = datos_liga['jornadas_grupo2']
    datos_liga['calendario_grupo1']==datos_liga['calendario_grupo1'] 
    datos_liga['calendario_grupo2'] = datos_liga['calendario_grupo2'] 
    with open(ruta_archivo, 'w') as archivo:
        json.dump(datos_liga, archivo)
    messagebox.showinfo("Éxito", "Cambios Guardados")


def cargar_datos():
    try:
        with open(ruta_archivo, 'r') as archivo:
            datos_cargados = json.load(archivo)
            global tabla_clasificacion, jornadas_grupo1, jornadas_grupo2
            tabla_clasificacion = datos_cargados.get('tabla_clasificacion', {})
            datos_liga['jornadas_grupo1'] = datos_cargados.get('jornadas_grupo1', [])
            datos_liga['jornadas_grupo2'] = datos_cargados.get('jornadas_grupo2', [])
            datos_liga['calendario_grupo1'] = datos_cargados.get('calendario_grupo1', [])
            datos_liga['calendario_grupo2'] = datos_cargados.get('calendario_grupo2', [])
    except FileNotFoundError:
        # No es necesario hacer nada si el archivo no existe; los datos se inicializarán como vacíos
        pass

cargar_datos()


# Inicialización de la ventana principal
root = tk.Tk()
root.configure(background='white')
root.title("Futbol 7 - Varonil")

# Configuración del canvas y las barras de desplazamiento
canvas = tk.Canvas(root, background='white')
frame_principal = tk.Frame(canvas, background='white')  # Este es el frame principal que contendrá todo
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)
canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Empaquetado de las barras de desplazamiento y el canvas
vsb.pack(side="right", fill="y")
hsb.pack(side="bottom", fill="x")
canvas.pack(side="left", fill="both", expand=True)
canvas_window = canvas.create_window((0, 0), window=frame_principal, anchor="nw")

def center_frame(event):
    canvas_width = event.width
    canvas_height = event.height
    frame_width = frame_principal.winfo_reqwidth()
    frame_height = frame_principal.winfo_reqheight()
    new_x = (canvas_width - frame_width) / 2 if canvas_width > frame_width else 0
    new_y = (canvas_height - frame_height) / 2 if canvas_height > frame_height else 0
    canvas.coords(canvas_window, new_x, new_y)

canvas.bind("<Configure>", center_frame)
frame_principal.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))



# Colores para la tabla
colors = {
    'header': '#FF6347',
    'team': '#FFA07A',
    'field': '#8B0000',
    'text': 'white',
}

font_settings = ('Arial', 16)
title_font_settings = ('Arial', 20, 'bold')

title_label = tk.Label(frame_principal, text="Rol de Juegos", bg='white', fg='black', font=title_font_settings)
title_label.pack(fill=tk.X, side=tk.TOP, pady=(10, 20))

entradas_canchas = []  #Inicializar una lista para almacenar referencias a las entradas de los equipos

entradas_resultados = []  # Almacena las entradas de los resultados de cada partido

todos_los_equipos = equipos_grupo1 + equipos_grupo2


def actualizar_opciones(equipo_seleccionado, combobox_a_actualizar, todos_los_equipos):
    if equipo_seleccionado == '':  # Si la selección está en blanco  Restablecer las opciones al total de equipos permitidos
        combobox_a_actualizar['values'] = todos_los_equipos
    else:
        # Determina el grupo del equipo seleccionado
        grupo_seleccionado = 'Grupo 1' if equipo_seleccionado in equipos_grupo1 else 'Grupo 2'
        
        # Establece las opciones excluyendo el equipo ya seleccionado y filtrando por el grupo correcto
        if grupo_seleccionado == 'Grupo 1':
            opciones_actualizadas = [''] + [equipo for equipo in equipos_grupo1 if equipo != equipo_seleccionado]
        else:
            opciones_actualizadas = [''] + [equipo for equipo in equipos_grupo2 if equipo != equipo_seleccionado]
        
        combobox_a_actualizar['values'] = opciones_actualizadas



# Función para crear tablas
def create_table(frame, cancha_number, colors, font_settings):
    headers = ['CANCHA', '8:00 - 8:45', '8:45 - 9:30', '9:30 - 10:15', '10:15 - 11:00']
    entradas_equipos = []  # Almacena las entradas de esta cancha específica

    # Crear encabezados
    for i, header in enumerate(headers):
        bg_color = colors['header']
        header_label = tk.Label(frame, text=header, bg=bg_color, fg=colors['text'], font=font_settings, borderwidth=2, relief='solid')
        header_label.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

    for i in range(len(headers)):
        frame.grid_columnconfigure(i, weight=1)

    # Número de cancha
    cancha_label = tk.Label(frame, text=str(cancha_number), bg=colors['field'], fg=colors['text'], font=font_settings, width=5, borderwidth=2, relief='solid')
    cancha_label.grid(row=1, column=0, rowspan=3, sticky="nsew")


    for i in range(1, 5):  # Para los 4 periodos de tiempo
        fila_entradas = []

        valores_con_blanco = [''] + equipos_grupo1 + equipos_grupo2  # Añade la opción en blanco

        # Combobox para el equipo visitante
        combo_visita = ttk.Combobox(frame, font=font_settings, state='normal')  # Cambiado a 'normal' para que puedan haber entradas vacías 
        combo_visita['values'] = valores_con_blanco
        combo_visita.grid(row=1, column=i, sticky="nsew", padx=1, pady=1)

        # Combobox para el equipo local
        combo_local = ttk.Combobox(frame, font=font_settings, state='normal')  # Cambiado a 'normal', para que puedan exisitr entradas vacías 
        combo_local['values'] = valores_con_blanco
        combo_local.grid(row=3, column=i, sticky="nsew", padx=1, pady=1)

        # Ajusta las funciones lambda para conservar la capacidad de limpieza, uno para visitoa y otro para local
        combo_visita.bind('<<ComboboxSelected>>', lambda event, c=combo_local, other=combo_visita: actualizar_opciones(other.get(), c, valores_con_blanco), add='+')
        combo_local.bind('<<ComboboxSelected>>', lambda event, c=combo_visita, other=combo_local: actualizar_opciones(other.get(), c, valores_con_blanco), add='+')

        fila_entradas.extend([combo_visita, combo_local])
        entradas_equipos.append(fila_entradas)



            # 'VS' Label
        vs_label = tk.Label(frame, text='VS', bg=colors['team'], fg='black', font=font_settings, relief='solid', borderwidth=2)
        vs_label.grid(row=2, column=i, sticky="nsew", padx=1, pady=1)

    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_rowconfigure(3, weight=1)


    # Añadir las entradas de esta cancha a la lista global
    entradas_canchas.append(entradas_equipos)

# Crear marcos para cada tabla y espacio blanco entre ellos
for i in range(1, 4):  # Para tres canchas
    table_frame = tk.Frame(frame_principal, background='white')
    table_frame.pack(fill=tk.X, side=tk.TOP, pady=20)
    create_table(table_frame, i, colors, font_settings)

# Función para mostrar los resultados en una nueva ventana y recolectar entradas
def imprimir_datos():
    global entradas_resultados
    entradas_resultados.clear()  # Limpiar la lista de resultados anteriores

    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados de los Partidos")
    ventana_resultados.configure(background='white')
    # Encabezados de la tabla de resultados
    encabezados_resultados = ["Goles Visita", "Equipo Visita", "Equipo Casa", "Goles Casa", "Penales"]
    for i, encabezado in enumerate(encabezados_resultados):
        tk.Label(ventana_resultados, text=encabezado, font=font_settings, bg='light grey', borderwidth=2, relief='solid').grid(row=0, column=i, sticky="nsew", padx=5, pady=5)

    # Llenar la tabla con los datos de los partidos
    fila_resultados = 1
    for cancha in entradas_canchas:
        for partido in cancha:
            datos_partido = {
                'equipo_visita': partido[0].get(),
                'equipo_casa': partido[1].get(),
                'goles_visita': tk.Entry(ventana_resultados, font=font_settings, bg='white', fg='black'),
                'goles_casa': tk.Entry(ventana_resultados, font=font_settings, bg='white', fg='black'),
                'penales': tk.Entry(ventana_resultados, font=font_settings, bg='white', fg='black'),  # Campo adicional para penales
            }
            if datos_partido['equipo_visita'] and datos_partido['equipo_casa']:  # Si ambos equipos están presentes
                tk.Label(ventana_resultados, text=datos_partido['equipo_visita'], font=font_settings, bg='white', fg='black').grid(row=fila_resultados, column=1, sticky="nsew", padx=5, pady=5)
                tk.Label(ventana_resultados, text=datos_partido['equipo_casa'], font=font_settings, bg='white', fg='black').grid(row=fila_resultados, column=2, sticky="nsew", padx=5, pady=5)
                datos_partido['goles_visita'].grid(row=fila_resultados, column=0, sticky="nsew", padx=5, pady=5)
                datos_partido['goles_casa'].grid(row=fila_resultados, column=3, sticky="nsew", padx=5, pady=5)
                datos_partido['penales'].grid(row=fila_resultados, column=4, sticky="nsew", padx=5, pady=5)  # Posicionando el campo de penales
                entradas_resultados.append(datos_partido)
                fila_resultados += 1
    # Botón para guardar los resultados de las entradas
    boton_guardar = tk.Button(ventana_resultados, text="Guardar Resultados", command=lambda: guardar_resultados(ventana_resultados))
    boton_guardar.grid(row=fila_resultados, columnspan=5, sticky='ew', padx=10, pady=10)
    


def reinicializar_tabla():
    for equipo in equipos_grupo1:
        tabla_clasificacion[equipo] = {'Grupo': 'Grupo 1', 'Lugar': 0, 'JJ': 0, 'JG': 0,'JEG': 0,'JEP': 0, 'JP':0, 'GF': 0, 'GC': 0, 'Dif': 0, 'Puntos': 0}
    for equipo in equipos_grupo2:
        tabla_clasificacion[equipo] = {'Grupo': 'Grupo 2', 'Lugar': 0, 'JJ': 0, 'JG': 0,'JEG': 0,'JEP': 0, 'JP':0, 'GF': 0, 'GC': 0, 'Dif': 0, 'Puntos': 0}

def inicializar_tabla():
    for equipo in equipos_grupo1:
        # Comprueba si el equipo ya existe en la tabla, y si no, inicialízalo
        if equipo not in tabla_clasificacion:
            tabla_clasificacion[equipo] = {'Grupo': 'Grupo 1', 'Lugar': 0, 'JJ': 0, 'JG': 0, 'JEG': 0, 'JEP': 0, 'JP': 0, 'GF': 0, 'GC': 0, 'Dif': 0, 'Puntos': 0}

    for equipo in equipos_grupo2:
        # Comprueba si el equipo ya existe en la tabla, y si no, inicialízalo
        if equipo not in tabla_clasificacion:
            tabla_clasificacion[equipo] = {'Grupo': 'Grupo 2', 'Lugar': 0, 'JJ': 0, 'JG': 0, 'JEG': 0, 'JEP': 0, 'JP': 0, 'GF': 0, 'GC': 0, 'Dif': 0, 'Puntos': 0}

inicializar_tabla()

def actualizar_tabla(equipo_visita, goles_visita, equipo_casa, goles_casa, penales):
    # Actualizar juegos jugados
    tabla_clasificacion[equipo_visita]['JJ'] += 1
    tabla_clasificacion[equipo_casa]['JJ'] += 1

    # Actualizar goles a favor y en contra
    tabla_clasificacion[equipo_visita]['GF'] += goles_visita
    tabla_clasificacion[equipo_casa]['GF'] += goles_casa
    tabla_clasificacion[equipo_visita]['GC'] += goles_casa
    tabla_clasificacion[equipo_casa]['GC'] += goles_visita

    # Actualizar diferencia de goles
    tabla_clasificacion[equipo_visita]['Dif'] = tabla_clasificacion[equipo_visita]['GF'] - tabla_clasificacion[equipo_visita]['GC']
    tabla_clasificacion[equipo_casa]['Dif'] = tabla_clasificacion[equipo_casa]['GF'] - tabla_clasificacion[equipo_casa]['GC']

    # Determinar resultado del partido
    if goles_visita > goles_casa:
        tabla_clasificacion[equipo_visita]['JG'] += 1
        tabla_clasificacion[equipo_visita]['Puntos'] += 3
        tabla_clasificacion[equipo_casa]['JP'] += 1


    elif goles_visita < goles_casa:
        tabla_clasificacion[equipo_casa]['JG'] += 1
        tabla_clasificacion[equipo_casa]['Puntos'] += 3
        tabla_clasificacion[equipo_visita]['JP'] += 1

    else:  # Empate
        if penales == '1':  # Ganó el equipo visitante por penales
            tabla_clasificacion[equipo_visita]['Puntos'] += 2
            tabla_clasificacion[equipo_casa]['Puntos'] += 1
            tabla_clasificacion[equipo_visita]['JEG'] += 1
            tabla_clasificacion[equipo_casa]['JEP'] += 1

        elif penales == '2':  # Ganó el equipo local por penales
            tabla_clasificacion[equipo_casa]['Puntos'] += 2
            tabla_clasificacion[equipo_visita]['Puntos'] += 1
            tabla_clasificacion[equipo_casa]['JEG'] += 1
            tabla_clasificacion[equipo_visita]['JEP'] += 1
        else:  # Empate sin penales
            tabla_clasificacion[equipo_visita]['Puntos'] += 1
            tabla_clasificacion[equipo_casa]['Puntos'] += 1

    ordenar_tabla()  # Reordenar la tabla basado en nuevos resultados

def ordenar_tabla():
    global tabla_clasificacion
    # Se Convierte  el diccionario en una lista de tuplas y se ordena por puntos, diferencia de goles y goles a favor
    tabla_ordenada = sorted(tabla_clasificacion.items(), key=lambda item: (-item[1]['Puntos'], -item[1]['Dif'],-item[1]['GF']))
    # Actualizan los lugares y lo volvemos a aconvertir en un diccionario
    tabla_clasificacion = {}
    for lugar, (equipo, datos) in enumerate(tabla_ordenada, start=1):
        datos['Lugar'] = lugar
        tabla_clasificacion[equipo] = datos


def mostrar_grupo(tabla_grupo, inicio_fila, grupo_titulo, ventana_tabla):
    title_bg_color = '#4E96AD' 
    header_bg_color = '#7FB3D5' 
    row_colors = ['#EAF2F8', '#D4E6F1']  # Colores alternos para las filas

    encabezados = ["Lugar", "Equipo", "JJ", "JG", "JEG", "JEP", "JP", "GF", "GC", "Dif", "Puntos"]
    tk.Label(ventana_tabla, text=grupo_titulo, font=title_font_settings, bg=title_bg_color, fg='white').grid(row=inicio_fila, columnspan=len(encabezados), sticky="nsew", padx=5, pady=5)
    for i, encabezado in enumerate(encabezados):
        tk.Label(ventana_tabla, text=encabezado, font=font_settings, bg=header_bg_color, fg='white').grid(row=inicio_fila + 1, column=i, sticky="nsew", padx=5, pady=5)

    equipos_ordenados = sorted(tabla_grupo.items(), key=lambda item: (-item[1]['Puntos'], -item[1]['Dif']))
    for index, (equipo, datos) in enumerate(equipos_ordenados, start=1):
        bg_color = row_colors[index % 2]  # Alternar colores de fila
        tk.Label(ventana_tabla, text=index, font=font_settings, bg=bg_color).grid(row=inicio_fila + index + 1, column=0, sticky="nsew", padx=5, pady=5)
        tk.Label(ventana_tabla, text=equipo, font=font_settings, bg=bg_color).grid(row=inicio_fila + index + 1, column=1, sticky="nsew", padx=5, pady=5)
        for j, key in enumerate(['JJ', 'JG', 'JEG', 'JEP', 'JP', 'GF', 'GC', 'Dif', 'Puntos']):
            tk.Label(ventana_tabla, text=datos[key], font=font_settings, bg=bg_color).grid(row=inicio_fila + index + 1, column=j + 2, sticky="nsew", padx=5, pady=5)


def mostrar_tabla_clasificacion():
    ventana_tabla = tk.Toplevel(root)
    ventana_tabla.title("Tabla de Clasificación")
    ventana_tabla.configure(background='white')

    # Configurar el contenedor principal de la ventana para que tenga desplazamiento
    contenedor_principal = tk.Canvas(ventana_tabla)
    scrollbar_vertical = tk.Scrollbar(ventana_tabla, orient="vertical", command=contenedor_principal.yview)
    scrollbar_horizontal = tk.Scrollbar(ventana_tabla, orient="horizontal", command=contenedor_principal.xview)
    contenedor_principal.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

    scrollbar_vertical.pack(side="right", fill="y")
    scrollbar_horizontal.pack(side="bottom", fill="x")
    contenedor_principal.pack(side="left", fill="both", expand=True)

    # Crear un frame dentro del canvas para los grupos y botones
    frame_tablas = tk.Frame(contenedor_principal)
    contenedor_principal.create_window((0, 0), window=frame_tablas, anchor="nw")

    # Obtenemos los grupos separados de la tabla de clasificación
    tabla_grupo1 = {equipo: datos for equipo, datos in tabla_clasificacion.items() if datos['Grupo'] == 'Grupo 1'}
    tabla_grupo2 = {equipo: datos for equipo, datos in tabla_clasificacion.items() if datos['Grupo'] == 'Grupo 2'}
    

    # Configurar paneles para cada grupo
    panel_grupo1 = tk.Frame(frame_tablas, background='white')
    panel_grupo2 = tk.Frame(frame_tablas, background='white')

    # Mostrar las tablas para cada grupo en sus respectivos paneles
    mostrar_grupo(tabla_grupo1, 0, "Premier", panel_grupo1)
    mostrar_grupo(tabla_grupo2, 0, "Ascenso", panel_grupo2)

    boton_historial_grupo1 = tk.Button(panel_grupo1, text='Historial Partidos Grupo 1', command=lambda: mostrar_historial(1))
    boton_historial_grupo1.grid(row=len(tabla_grupo1) + 2, columnspan=3, sticky='ew', padx=10, pady=10)  # Ajusta la fila de inicio según 

    boton_borrar_historial_grupo1 = tk.Button(panel_grupo1, text='Borrar todo el historial del grupo 1', command=lambda: limpiar_historial_1())
    boton_borrar_historial_grupo1.grid(row=len(tabla_grupo1) + 3, columnspan=3, sticky='ew', padx=10, pady=10)

    boton_historial_grupo2 = tk.Button(panel_grupo2, text='Historial Partidos Grupo 2', command=lambda: mostrar_historial(2))
    boton_historial_grupo2.grid(row=len(tabla_grupo2) + 2, columnspan=3, sticky='ew', padx=10, pady=10)  

    boton_borrar_historial_grupo2 = tk.Button(panel_grupo2, text='Borrar todo el historial del grupo 2', command=lambda: limpiar_historial_2())
    boton_borrar_historial_grupo2.grid(row=len(tabla_grupo2) + 3, columnspan=3, sticky='ew', padx=10, pady=10)

    boton_partidos_faltantes_1 = tk.Button(panel_grupo1, text=' Partidos Por jugar  Grupo 1', command=lambda: partidos_faltantes_por_jugar(1))
    boton_partidos_faltantes_1.grid(row=len(tabla_grupo1) + 2, column=6, columnspan=3, sticky='ew', padx=10, pady=10)  

    boton_partidos_faltantes_2 = tk.Button(panel_grupo2, text=' Partidos Por jugar  Grupo 2', command=lambda: partidos_faltantes_por_jugar(2))
    boton_partidos_faltantes_2.grid(row=len(tabla_grupo2) + 2, column=6, columnspan=3, sticky='ew', padx=10, pady=10)  

    panel_grupo1.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    panel_grupo2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    # Actualizar y configurar el contenedor principal para que se ajuste al contenido
    frame_tablas.update_idletasks()
    contenedor_principal.config(scrollregion=contenedor_principal.bbox("all"))

   


# Función para guardar los resultados y luego imprimirlos
def guardar_resultados(ventana):

    jornada_actual_grupo1 = []
    jornada_actual_grupo2 = []
    for partido in entradas_resultados:
        print(partido)
        print(entradas_resultados)
        equipo_visita = partido['equipo_visita']
        equipo_casa = partido['equipo_casa']
        goles_visita = partido['goles_visita'].get().strip()
        goles_casa = partido['goles_casa'].get().strip()
        penales = partido['penales'].get().strip()  # Extraemos el resultado de los penales 

        # Comprobar que ambos equipos están registrados en los grupos
        if equipo_visita not in equipos_grupo1 and equipo_visita not in equipos_grupo2:
            messagebox.showerror("Error", f"El equipo '{equipo_visita}' no está registrado en ningún grupo.")
            return  # Detiene el guardado de datos
        if equipo_casa not in equipos_grupo1 and equipo_casa not in equipos_grupo2:
            messagebox.showerror("Error", f"El equipo '{equipo_casa}' no está registrado en ningún grupo.")
            return  # Detiene el guardado de datos

        # Comprueba que no se introduzcan equipos iguales
        if equipo_visita == equipo_casa:
            messagebox.showerror("Error", "Un equipo no puede jugar contra sí mismo.")
            return  # Detiene el guardado de datos

        # Comprueba que los equipos pertenezcan al mismo grupo
        grupo_equipo_visita = 'Grupo 1' if equipo_visita in equipos_grupo1 else 'Grupo 2'
        grupo_equipo_casa = 'Grupo 1' if equipo_casa in equipos_grupo1 else 'Grupo 2'
        if grupo_equipo_visita != grupo_equipo_casa:
            messagebox.showerror("Error", "Equipos de diferentes grupos no pueden enfrentarse.")
            return     
        
        try:
            goles_visita = int(goles_visita)
            goles_casa = int(goles_casa)
        except ValueError:
            messagebox.showerror("Error", "Los goles deben ser números enteros.")
            return 

        # Validar que los penales sean '1', '2' o vacíos
        if penales not in ['1', '2', '']:
            messagebox.showerror("Error", "Los penales deben ser '1', '2' o dejar el campo vacío.")
            return  

        # Después de validar y antes de actualizar la tabla
        partido_info = f"{equipo_visita} vs {equipo_casa} - Marcador {goles_visita}:{goles_casa}" + (f" Penales: {penales}" if penales else "")
        if grupo_equipo_visita == 'Grupo 1':
            jornada_actual_grupo1.append(partido_info)
        else:
            jornada_actual_grupo2.append(partido_info)
   
    for partido in entradas_resultados: #ya una vez que se validaron todos los partidos, ya se pueden guardar los datos
        equipo_visita = partido['equipo_visita']
        equipo_casa = partido['equipo_casa']
        goles_visita =(partido['goles_visita'].get().strip())
        goles_casa =(partido['goles_casa'].get().strip())
        goles_casa=int(goles_casa)
        goles_visita=int(goles_visita)
        penales = partido['penales'].get().strip()

        actualizar_tabla(equipo_visita, goles_visita, equipo_casa, goles_casa, penales)  # Pasamos los resultados  a actualizar_tabla

    if jornada_actual_grupo1:  # Solo añadir si hay partidos esa jornada
        datos_liga['jornadas_grupo1'].append(jornada_actual_grupo1)
    if jornada_actual_grupo2:  # Igual para el Grupo 2
        datos_liga['jornadas_grupo2'].append(jornada_actual_grupo2)

    messagebox.showinfo("Éxito", "Resultados guardados y tabla de clasificación actualizada.")
    # Imprimir la tabla de clasificación actualizada
    print("Tabla de Clasificación Actualizada:")
    for equipo, datos in tabla_clasificacion.items():
        print(f"{datos['Lugar']}. {equipo}: JJ={datos['JJ']}, JG={datos['JG']},JEG={datos['JEG']},JEP={datos['JEP']},JP={datos['JP']}, GF={datos['GF']}, GC={datos['GC']}, Dif={datos['Dif']}, Puntos={datos['Puntos']}")
        
    guardar_datos()
    ventana.destroy()
    mostrar_tabla_clasificacion()


def mostrar_historial(grupo):
    if grupo == 1:
        historial = datos_liga['jornadas_grupo1']
        titulo_grupo = "Historial de Partidos - Grupo 1"
    else:
        historial = datos_liga['jornadas_grupo2']
        titulo_grupo = "Historial de Partidos - Grupo 2"

    ventana_historial = tk.Toplevel(root)
    ventana_historial.title(titulo_grupo)

    # Configuración del scrollbar
    canvas = tk.Canvas(ventana_historial, highlightthickness=0)  # Eliminar el borde del canvas
    scrollbar = ttk.Scrollbar(ventana_historial, orient="vertical", command=canvas.yview)
    frame_scrollable = tk.Frame(canvas)  # Este frame dentro del canvas tendrá los widgets desplazables

    # Crear una ventana dentro del canvas para el frame scrollable
    canvas_frame = canvas.create_window((0, 0), window=frame_scrollable, anchor="center")

    # Función para actualizar la posición del frame scrollable al cambiar el tamaño de la ventana
    def configure_canvas(event):
        canvas_width = event.width
        canvas.itemconfig(canvas_frame, width=canvas_width)  # Ajustar el ancho del frame al del canvas
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_frame, anchor="center")  # Centrar el frame dentro del canvas

    canvas.bind("<Configure>", configure_canvas)
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(ventana_historial, text=titulo_grupo, font=title_font_settings).pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mostrar cada jornada y sus partidos en el frame_scrollable
    for num_jornada, partidos in enumerate(historial, start=1):
        jornada_label = tk.Label(frame_scrollable, text=f"Jornada {num_jornada}", font=font_settings)
        jornada_label.pack()
        for partido in partidos:
            partido_label = tk.Label(frame_scrollable, text=partido, font=font_settings)
            partido_label.pack()


def partidos_faltantes_por_jugar(grupo_numero):
    if grupo_numero == 1:
        jornadas_planificadas = datos_liga['calendario_grupo1']
        historial_partidos = datos_liga['jornadas_grupo1']
        titulo_grupo = "Partidos Restantes - Grupo 1"
    else:
        jornadas_planificadas = datos_liga['calendario_grupo2']
        historial_partidos = datos_liga['jornadas_grupo2']
        titulo_grupo = "Partidos Restantes - Grupo 2"

    # Se Convierte  el historial de partidos en un formato comparable
    partidos_jugados = set()
    for jornada in historial_partidos:
        for registro in jornada:
            # Extraemos solo la parte que contiene "EquipoA vs EquipoB", podemos ver como se guardan los aprtidos en partido_info
            partido = registro.split(' - ')[0]  # Separamos la información del partido de los marcadores
            equipos = partido.split(' vs ')  # Separamos los nombres de los equipos
            equipos_ordenados = ' vs '.join(sorted(equipos))  # Ordenamos los nombres alfabéticamente y los juntamos de nuevo, para que no importe quien fue visita o local, así no se repiten los partidos.
            partidos_jugados.add(equipos_ordenados)

            
    # Revisar qué partidos de las jornadas planificadas aún no se han jugado
    partidos_faltantes = {}  # Cambiar a diccionario para agrupar por jornada


    ventana_faltantes = tk.Toplevel(root)
    ventana_faltantes.title(titulo_grupo)

    # Configuración del scrollbar
    canvas = tk.Canvas(ventana_faltantes, highlightthickness=0)  
    scrollbar = ttk.Scrollbar(ventana_faltantes, orient="vertical", command=canvas.yview)
    frame_scrollable = tk.Frame(canvas) 

    canvas_frame = canvas.create_window((0, 0), window=frame_scrollable, anchor="nw") 

    def configure_canvas(event):
        canvas_width = event.width
        canvas.itemconfig(canvas_frame, width=canvas_width)  
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_frame, anchor="center")  

    canvas.bind("<Configure>", configure_canvas)
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(ventana_faltantes, text=titulo_grupo, font=title_font_settings).pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for numero_jornada, jornada in enumerate(jornadas_planificadas, start=1):
        partidos_de_jornada = []  # Lista para almacenar partidos de esta jornada aún no jugados
        for partido in jornada:
            # Ordenamos alfabéticamente los nombres de los equipos antes de formar la cadena del encuentro, se ordena alfabéticamente por la imsa razón de que no importe el orden
            equipos_ordenados = ' vs '.join(sorted([partido[0], partido[1]]))
            if equipos_ordenados not in partidos_jugados:
                partidos_de_jornada.append(equipos_ordenados)
        if partidos_de_jornada:
            partidos_faltantes[f"Jornada {numero_jornada} por jugar"] = partidos_de_jornada


    # Mostrar los partidos faltantes organizados por jornada en la interfaz gráfica
    for jornada, partidos in partidos_faltantes.items():
        tk.Label(frame_scrollable, text=jornada, font=title_font_settings).pack(fill='x')
        for partido in partidos:
            tk.Label(frame_scrollable, text=partido).pack(fill='x')

    print(jornadas_planificadas)
    print(partidos_faltantes)
    print(partidos_jugados)

    return partidos_faltantes



def limpiar_partidos():
    for cancha in entradas_canchas:  # Iterar sobre cada lista de entradas de canchas
        for partido in cancha:  # Iterar sobre cada lista de entradas de partidos en la cancha
            for entrada in partido:  # Iterar sobre cada entrada en el partido
                if isinstance(entrada, ttk.Combobox):  # Si la entrada es un Combobox
                    entrada.set('')  # Limpiar la selección actual
                    entrada['values'] = equipos_grupo1 + equipos_grupo2  # Restablecer los valores originales
                else:  # Para widgets de tipo Entry y otros
                    entrada.delete(0, tk.END)  # Limpiar la entrada



def limpiar_tabla():
    global tabla_clasificacion
    tabla_clasificacion = {}  # Resetea la tabla de clasificación a un diccionario vacío
    inicializar_tabla()  # Vuelve a inicializar la tabla para reestablecer la estructura básica con los equipos
    messagebox.showinfo("Tabla Limpiada", "La tabla de clasificación ha sido reseteada.")


def limpiar_historial_1():
    global datos_liga
    datos_liga['jornadas_grupo1'] =  []
  # Resetea la tabla de clasificación a un diccionario vacío
    messagebox.showinfo("Historial del grupo uno resetado.")
    
def limpiar_calendario_1():
    global datos_liga
    datos_liga['calendario_grupo1']=[]
    messagebox.showinfo("Calendario del grupo 1 Reseteado.")

def limpiar_calendario_2():
    global datos_liga
    datos_liga['calendario_grupo2']=[]
    messagebox.showinfo("Calendario del grupo 2 Reseteado.")


def limpiar_historial_2():
    global datos_liga
    datos_liga['jornadas_grupo2'] =  []
  # Resetea la tabla de clasificación a un diccionario vacío
    messagebox.showinfo("Historial del grupo uno resetado.")


    # Función para generar partidos de un grupo específico

def generar_calendario_completo(equipos):
    # Asegurarse de que la lista de equipos no se modifique
    equipos = list(equipos)
    
    '''Si el número de equipos es impar, podríamos agregar otro equipo llamado 'descansa' para indicar que le toca a 
    ese equipo descanrar pero, se podria dejar vació y no simplemente de dejaría a un equipo descasnadn cada jornada. '''
    if len(equipos) % 2 != 0:
        equipos.append(None)
    
    total_equipos = len(equipos)
    partidos_por_jornada = total_equipos // 2
    jornadas = []

    # Rotar los equipos (excepto el primero) para generar las jornadas
    for i in range(total_equipos - 1):  # Se necesita una jornada menos que el número de equipos
        jornada_actual = []
        for j in range(partidos_por_jornada):
            if equipos[j] is not None and equipos[total_equipos - j - 1] is not None:  # Ignorar el 'equipo descansa'
                jornada_actual.append((equipos[j], equipos[total_equipos - j - 1]))
        jornadas.append(jornada_actual)
        
        # Rotar los equipos, manteniendo el primero en su lugar
        equipos = [equipos[0]] + equipos[-1:] + equipos[1:-1]

    return jornadas



def inicializar_calendario_completo():
    # Verifica si ya existen datos en los calendarios de ambos grupos
    if datos_liga.get('calendario_grupo1') and datos_liga.get('calendario_grupo2'):
        # Si ambos calendarios ya tienen datos, no hace falta inicializarlos nuevamente
        print("Los calendarios de ambos grupos ya están inicializados.")
        return
    
    # Si uno o ambos calendarios están vacíos, se generan nuevos calendarios
    if not datos_liga.get('calendario_grupo1'):
        print("Inicializando calendario para el Grupo 1...")
        datos_liga['calendario_grupo1'] = generar_calendario_completo(equipos_grupo1)
    
    if not datos_liga.get('calendario_grupo2'):
        print("Inicializando calendario para el Grupo 2...")
        datos_liga['calendario_grupo2'] = generar_calendario_completo(equipos_grupo2)
    
    guardar_datos()

inicializar_calendario_completo()


def obtener_proxima_jornada(grupo_numero):
    if grupo_numero == 1:
        jornadas = datos_liga['calendario_grupo1']
        historial = datos_liga['jornadas_grupo1']
    else:
        jornadas = datos_liga['calendario_grupo2']
        historial = datos_liga['jornadas_grupo2']

    numero_jornada_actual = len(historial)
    if numero_jornada_actual < len(jornadas):
        return jornadas[numero_jornada_actual]  # Devuelve la siguiente jornada
    else:
        return None  # No hay más jornadas disponibles
import random

def asignar_partidos_a_canchas():
    # Obtener la próxima jornada para ambos grupos
    proxima_jornada_grupo1 = obtener_proxima_jornada(1)
    proxima_jornada_grupo2 = obtener_proxima_jornada(2)

    if proxima_jornada_grupo1 is None and proxima_jornada_grupo2 is None:
        messagebox.showinfo("Información", "No hay más jornadas disponibles para ambos grupos.")
        return

    # Combina las jornadas de ambos grupos y mezcla los partidos
    partidos_combinados = (proxima_jornada_grupo1 if proxima_jornada_grupo1 is not None else []) + \
                          (proxima_jornada_grupo2 if proxima_jornada_grupo2 is not None else [])
    random.shuffle(partidos_combinados)

    # Asegurarse de que hay suficientes entradas (comboboxes) para todos los partidos de la jornada combinada.
    if len(partidos_combinados) > sum(len(cancha) for cancha in entradas_canchas):
        messagebox.showerror("Error", "No hay suficientes campos para todos los partidos de esta jornada combinada.")
        return

    index_partido = 0  # Índice para llevar cuenta del partido actual en la jornada

    for cancha in entradas_canchas:
        for comboboxes in cancha:
            if index_partido < len(partidos_combinados):  # Verifica si aún hay partidos por asignar
                partido = partidos_combinados[index_partido]
                comboboxes[0].set(partido[0])  # Establece el equipo de visita en el primer combobox
                comboboxes[1].set(partido[1])  # Establece el equipo de casa en el segundo combobox
                index_partido += 1  # Mueve al siguiente partido
            else:
                # Si no hay más partidos, limpia los comboboxes restantes
                comboboxes[0].set('')
                comboboxes[1].set('')



# Iterar sobre cada jornada y los partidos dentro de cada jornada para el Grupo 1
for indice_jornada, jornada in enumerate(datos_liga['calendario_grupo1'], start=1):
    print(f"Jornada {indice_jornada}: {len(jornada)} partidos")
    for partido in jornada:
        print(f"  {partido[0]} vs {partido[1]}")
# Iterar sobre cada jornada y los partidos dentro de cada jornada para el Grupo 1
for indice_jornada, jornada in enumerate(datos_liga['calendario_grupo2'], start=1):
    print(f"Jornada {indice_jornada}: {len(jornada)} partidos")
    for partido in jornada:
        print(f"  {partido[0]} vs {partido[1]}")

'''Esto nos ayuda a ver que en efecto, se estpan genradno correctamente las jornadas y checar si 
se están registradn correctamente de la función partidos_faltantes_por_jugar'''

    # Si necesitas manejar múltiples grupos en un día, puedes expandir este método
    # para alternar entre grupo_numero 1 y 2, o establecerlo basado en alguna lógica específica de tu aplicación.




frame_botones = tk.Frame(frame_principal)
frame_botones.pack(pady=10)

boton_imprimir_datos = tk.Button(frame_botones, text="Imprimir Datos", command=imprimir_datos)
boton_imprimir_datos.grid(row=0, column=0, padx=5, pady=2)

boton_mostrar_tabla = tk.Button(frame_botones, text="Mostrar Tabla de Clasificación", command=mostrar_tabla_clasificacion)
boton_mostrar_tabla.grid(row=0, column=1, padx=5, pady=2)

boton_limpiar = tk.Button(frame_botones, text='Limpiar Partidos', command=limpiar_partidos)
boton_limpiar.grid(row=0, column=2, padx=5, pady=2)

boton_limpiar_tabla = tk.Button(frame_botones, text='Limpiar Tabla', command=limpiar_tabla)
boton_limpiar_tabla.grid(row=0, column=3, padx=5, pady=2)

boton_generar_partidos = tk.Button(frame_botones, text='Generar Partidos Aleatorios', command=asignar_partidos_a_canchas)
boton_generar_partidos.grid(row=0, column=4, columnspan=2, padx=5, pady=2)  # Span across both columns for emphasis

boton_limpiar_calendario_1 = tk.Button(frame_botones, text='Limpiar Calendario del grupo 1', command=limpiar_calendario_1)
boton_limpiar_calendario_1.grid(row=1, column=0, padx=5, pady=2)

boton_limpiar_calendario_2 = tk.Button(frame_botones, text='Limpiar Calendario del grupo 2', command=limpiar_calendario_2)
boton_limpiar_calendario_2.grid(row=1, column=1, padx=5, pady=2)

boton_guardar = tk.Button(frame_botones, text='Guardar Cambios', command=guardar_datos)
boton_guardar.grid(row=1, column=2, padx=5, pady=2)



# Establecer estilos comunes
boton_estilos = {
    'activebackground': '#AED6F1',  
    'bg': '#D6EAF8',                
    'fg': '#1B4F72',                
    'relief': 'groove',             
    'font': ('Arial', 12, 'bold'),  
    'padx': 10,                     
    'pady': 5                       
}


# Aplicar estilos a los botones
boton_imprimir_datos.config(**boton_estilos)
boton_mostrar_tabla.config(**boton_estilos)
boton_limpiar.config(**boton_estilos)
boton_limpiar_tabla.config(**boton_estilos)
boton_generar_partidos.config(**boton_estilos)
boton_limpiar_calendario_1.config(**boton_estilos)
boton_limpiar_calendario_2.config(**boton_estilos)
boton_guardar.config(**boton_estilos)

# Configurar el frame de botones
frame_botones.config(
    bg='#EBF5FB'  # Color de fondo del frame
)

# Ajustar la disposición de los botones en el frame
frame_botones.pack(pady=20, padx=20) 

boton_generar_partidos.config(bg='#5499C7', fg='white')  #diseño diferetne porque se tiene pensasdo que sea el priemro que se usará.


# Ejecutar la aplicación
root.mainloop()



