# Import
import sqlite3
import os


# Variables
contacts = []
parar = False


# Metodo -> crea BBDD
def crear_bbdd():
    conexion = sqlite3.connect('agendapython.db')
    cursor = conexion.cursor()
    cursor.execute('''CREATE TABLE contactos (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, apellido TEXT, telefono TEXT CHECK (length(telefono) = 9) NOT NULL)''')
    cursor.execute("INSERT INTO contactos (nombre, apellido, telefono) VALUES ('Javier', 'Garcia', '601367968')")
    conexion.commit()
    conexion.close()


# Metodo -> carga contenido BBDD
def cargar_bbdd():
    conexion = sqlite3.connect('agendapython.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM contactos')
    resultados = cursor.fetchall()
    
    for resultado in resultados:
        c_nombre = resultado[1]
        c_apellido = resultado[2]
        c_telefono = resultado[3]
        c = Contacto(c_nombre, c_apellido, c_telefono)
        contacts.append(c)

    conexion.commit()
    conexion.close()


# Metodo -> muestra el menu principal
def mostrar_menu():
    print("*** AGENDA PYTHON ***")
    print("1. Mostrar contactos")
    print("2. Añadir contacto")
    print("3. Eliminar contacto")
    print("4. Eliminar agenda")
    print("5. Salir")


# Metodo -> muestra contactos de la lista
def mostrar_contactos():
    if len(contacts) == 0:
        print("No hay ningún contacto.")
    else:
        for c in contacts:
            print(c.__str__())
    print()


# Metodo -> añade contacto a la lista
def añadir_contacto():
    try:
        c_nombre = input("Nombre: ")
        c_apellido = input("Apellido: ")
        c_telefono = input("Telefono: ")
        c_telefono = int(c_telefono)

        if isinstance(c_telefono, int) and len(str(c_telefono)) == 9:
            c = Contacto(c_nombre, c_apellido, c_telefono)
            contacts.append(c)
            conexion = sqlite3.connect('agendapython.db')
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO contactos (nombre, apellido, telefono) VALUES ('" + c_nombre + "', '" + c_apellido + "', '" + str(c_telefono) + "')")
            conexion.commit()
            conexion.close()
            print("Contacto añadido.\n")
        else:
            print("ERROR: Debes introducir 9 dígitos\n")  
    except:
        print("ERROR: Debes introducir un número de telefono\n")


# Metodo -> elimina contacto a la lista, si hay varios
# con el mismo nombre, elimina el primero
def eliminar_contacto():
    try:
        nombre_del = input("Nombre del contacto a borrar: ")
        encontrado = False
        for c in contacts:
            if c.nombre == nombre_del:
                contacts.remove(c)

                conexion = sqlite3.connect('agendapython.db')
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM contactos WHERE nombre='" + nombre_del + "'")
                conexion.commit()
                conexion.close()

                print("Contacto eliminado.\n")
                encontrado = True
        if encontrado == False:
            print("No existe ese contacto.\n")

    except:
        print("ERROR al eliminar el contacto.\n")


# Metodo -> elimina toda la bbdd de la agenda
def eliminar_agenda():
    os.remove('agendapython.db')
    contacts.clear()
    print("Agenda eliminada.\n")


# Clase Contacto
class Contacto:
    def __init__(self, nombre, apellido, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def __str__(self):
        cadena = self.nombre + ", " + self.apellido + ", " + str(self.telefono)
        return cadena


# Main
if os.path.exists("agendapython.db"):
    cargar_bbdd()
else:
    crear_bbdd()

while parar == False:
    mostrar_menu()
    opcion = input("\n")
    print()
    if opcion == "1":
        mostrar_contactos()
    elif opcion == "2":
        añadir_contacto()
    elif opcion == "3":
        eliminar_contacto()
    elif opcion == "4":
        eliminar_agenda()
    else:
        print("Ha salido de la Agenda Python\n")
        parar = True