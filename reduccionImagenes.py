import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def aplicar_filtro(imagen, filas_filtro, columnas_filtro):
    # Obtener el ancho y alto de la imagen original
    ancho, alto = imagen.size

    # Cargamos los píxeles de la imagen original
    pixeles = imagen.load()

    # Matriz del filtro con todos los elementos iguales a 1
    matriz_filtro = [[1] * columnas_filtro for _ in range(filas_filtro)]

    # Creamos una nueva imagen filtrada con las mismas dimensiones que la original
    nueva_imagen = Image.new("RGB", (ancho, alto))

    # Cargamos los píxeles de la nueva imagen filtrada
    nuevos_pixeles = nueva_imagen.load()

    # Recorremos cada píxel de la imagen original
    for y in range(alto):
        for x in range(ancho):
            # Inicializamos las variables para acumular los valores de color
            r_total, g_total, b_total = 0, 0, 0
            count = 0

            # Recorremos los píxeles vecinos alrededor del píxel actual usando el tamaño del filtro
            for i in range(filas_filtro):
                for j in range(columnas_filtro):
                    # Calculamos las coordenadas de los píxeles vecinos
                    nx = x + j - columnas_filtro // 2
                    ny = y + i - filas_filtro // 2

                    # Verificamos si las coordenadas están dentro de los límites de la imagen
                    if nx >= 0 and ny >= 0 and nx < ancho and ny < alto:
                        # Obtenemos el color del píxel vecino
                        pixel = pixeles[nx, ny]
                        r, g, b = pixel

                        # Multiplicamos el valor de cada canal de color por el elemento correspondiente
                        # en la matriz del filtro
                        r_total += r * matriz_filtro[i][j]
                        g_total += g * matriz_filtro[i][j]
                        b_total += b * matriz_filtro[i][j]

                        # Incrementamos el contador de píxeles vecinos válidos
                        count += 1

            # Calculamos el promedio de los valores de color
            r_avg = r_total // count
            g_avg = g_total // count
            b_avg = b_total // count

            # Establecemos el píxel resultante en la nueva imagen filtrada
            nuevos_pixeles[x, y] = (r_avg, g_avg, b_avg)

    # Devolvemos la nueva imagen filtrada
    return nueva_imagen

def abrir_imagen():
    path = filedialog.askopenfilename(filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])

    if path:
        global imagen
        imagen = Image.open(path)

        # Actualizar la imagen original en el lienzo
        imagen_original = ImageTk.PhotoImage(imagen)
        lienzo_original.configure(image=imagen_original)
        lienzo_original.image = imagen_original

def aplicar_filtro_y_mostrar():
    filas_filtro = int(entrada_filas.get())
    columnas_filtro = int(entrada_columnas.get())

    nueva_imagen = aplicar_filtro(imagen, filas_filtro, columnas_filtro)

    # Actualizar la imagen filtrada en el lienzo
    imagen_filtrada = ImageTk.PhotoImage(nueva_imagen)
    lienzo_filtrado.configure(image=imagen_filtrada)
    lienzo_filtrado.image = imagen_filtrada

root = tk.Tk()
root.title("Aplicar Filtro")

# Frame para los botones y la entrada de texto
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

boton_abrir = tk.Button(frame_botones, text="Abrir Imagen", command=abrir_imagen)
boton_abrir.pack(side="left", padx=5)

etiqueta_filas = tk.Label(frame_botones, text="Filas del filtro:")
etiqueta_filas.pack(side="left", padx=5)

entrada_filas = tk.Entry(frame_botones)
entrada_filas.pack(side="left", padx=5)

etiqueta_columnas = tk.Label(frame_botones, text="Columnas del filtro:")
etiqueta_columnas.pack(side="left", padx=5)

entrada_columnas = tk.Entry(frame_botones)
entrada_columnas.pack(side="left", padx=5)

boton_aplicar = tk.Button(frame_botones, text="Aplicar Filtro", command=aplicar_filtro_y_mostrar)
boton_aplicar.pack(side="left", padx=5)


frame_labels = tk.Frame(root)
frame_labels.pack()

label_original = tk.Label(frame_labels, text="Imagen Original")
label_original.pack(side=tk.LEFT, padx=100)

label_modificada = tk.Label(frame_labels, text="Imagen Modificada")
label_modificada.pack(side=tk.RIGHT, padx=100)

# Frame para la imagen original y la imagen filtrada
frame_imagenes = tk.Frame(root)
frame_imagenes.pack()

lienzo_original = tk.Label(frame_imagenes)
lienzo_original.pack(side=tk.LEFT, padx=10)

lienzo_filtrado = tk.Label(frame_imagenes)
lienzo_filtrado.pack(side=tk.LEFT, padx=10)

root.mainloop()
