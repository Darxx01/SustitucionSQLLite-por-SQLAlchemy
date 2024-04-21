import mysql.connector

# Conexión a la base de datos MariaDB
CONFIG_DB = {
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': '127.0.0.1',
    'database': 'diccionario',
    'raise_on_warnings': True
}

def obtener_conexion():
    return mysql.connector.connect(**CONFIG_DB)

def crear_tablas():
    tablas = [
        """
        CREATE TABLE IF NOT EXISTS diccionario(
            id INT AUTO_INCREMENT PRIMARY KEY,
            palabra TEXT NOT NULL,
            significado TEXT NOT NULL
        );
        """
    ]
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    for tabla in tablas:
        cursor.execute(tabla)
    cursor.close()
    conexion.close()

def principal():
    crear_tablas()
    menu = """
a) Agregar nueva palabra
b) Editar palabra existente
c) Eliminar palabra existente
d) Ver listado de palabras
e) Buscar significado de palabra
f) Salir
Elige: """
    eleccion = ""
    while eleccion != "f":
        eleccion = input(menu)
        if eleccion == "a":
            palabra = input("Ingresa la palabra: ")
            # Comprobar si no existe
            posible_significado = buscar_significado_palabra(palabra)
            if posible_significado:
                print(f"La palabra '{palabra}' ya existe")
            else:
                significado = input("Ingresa el significado: ")
                agregar_palabra(palabra, significado)
                print("Palabra agregada")
        elif eleccion == "b":
            palabra = input("Ingresa la palabra que quieres editar: ")
            nuevo_significado = input("Ingresa el nuevo significado: ")
            editar_palabra(palabra, nuevo_significado)
            print("Palabra actualizada")
        elif eleccion == "c":
            palabra = input("Ingresa la palabra a eliminar: ")
            eliminar_palabra(palabra)
        elif eleccion == "d":
            palabras = obtener_palabras()
            print("=== Lista de palabras ===")
            for palabra in palabras:
                print(palabra[0])
        elif eleccion == "e":
            palabra = input(
                "Ingresa la palabra de la cual quieres saber el significado: ")
            significado = buscar_significado_palabra(palabra)
            if significado:
                print(f"El significado de '{palabra}' es:\n{significado[0]}")
            else:
                print(f"Palabra '{palabra}' no encontrada")

def agregar_palabra(palabra, significado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "INSERT INTO diccionario(palabra, significado) VALUES (%s, %s)"
    cursor.execute(sentencia, (palabra, significado))
    conexion.commit()
    cursor.close()
    conexion.close()

def editar_palabra(palabra, nuevo_significado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "UPDATE diccionario SET significado = %s WHERE palabra = %s"
    cursor.execute(sentencia, (nuevo_significado, palabra))
    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_palabra(palabra):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    sentencia = "DELETE FROM diccionario WHERE palabra = %s"
    cursor.execute(sentencia, (palabra,))
    conexion.commit()
    cursor.close()
    conexion.close()

def obtener_palabras():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT palabra FROM diccionario"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    return resultados

def buscar_significado_palabra(palabra):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "SELECT significado FROM diccionario WHERE palabra = %s"
    cursor.execute(consulta, (palabra,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado

if __name__ == '__main__':
    principal()
