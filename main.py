import os

nombre_db = 'datos.db'
archivo_a_ejecutar = 'load_data.py'

if not os.path.exists(os.path.join(os.getcwd(), 'datos.db')):
    print("cargando la base de datos...")
    try:
        exec(open(archivo_a_ejecutar).read())
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo_a_ejecutar}.")

from controller import webServer

webServer.app.run(debug=True)
