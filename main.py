import sqlite3
import funciones
import os
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

def main():
    os.system('cls')
    funciones.crear_tabla()  # Asegúrate de que esta línea se ejecute
    
    # Mensaje de bienvenida en verde
    print(Fore.GREEN + "\n ############################################################\n")
    print(Fore.GREEN + "\tBienvenido al programa de gestión de productos.")
    print(Fore.GREEN + "\n ############################################################\n")

    while True:
        print("\nIngrese una opción del menú:\n\t1. Agregar producto al inventario\n\t2. Consultar de un producto\n\t3. Modificar la cantidad de un producto\n\t4. Eliminar un producto del inventario\n\t5. Listar productos registrados\n\t6. Listar productos con stock bajo\n\t7. Salir\n")

        opcion = input("Seleccione una opción: \n") #toma la opción ingresada por el usuario.

        if opcion == "1":
            os.system('cls')
            nombre = input("Ingrese el nombre del producto: ").upper()
            
            # Verificar si el producto ya existe
            if funciones.producto_existe(nombre):
                print(Fore.RED + f"El producto '{nombre}' ya existe en el inventario. Modifique el producto YA EXISTENTE.")
                continue  # Volver al menú principal
            
            descripcion = input("Ingrese la descripción del producto: ").upper()
            
            while True:
                try:
                    cantidad = int(input("Ingrese la cantidad del producto: "))
                    break
                except ValueError:
                    print("Error: La cantidad debe ser un número entero. Inténtelo de nuevo.")

            while True:
                try:
                    precio = float(input("Ingrese el precio del producto: "))
                    break
                except ValueError:
                    print("Error: La cantidad debe ser un número entero. Inténtelo de nuevo.")
            
            categoria = input("Ingrese la categoría del producto: ").upper()
            funciones.agregar_producto(nombre, descripcion, cantidad, precio, categoria)

        elif opcion == "2": # Consultar un producto
            os.system('cls')
            while True:
                metodo_busqueda = input("¿Desea buscar por ID o por nombre? (Ingrese 'ID' o 'nombre'): ").strip().lower()
                if metodo_busqueda == 'id':
                    id_producto = int(input("Ingrese el ID del producto que desea consultar: "))
                    funciones.buscar_producto(id_producto=id_producto)
                    break
                elif metodo_busqueda == 'nombre':
                    nombre_producto = input("Ingrese el nombre del producto que desea consultar: ")
                    funciones.buscar_producto(nombre_producto=nombre_producto)
                    break
                else:
                    print("Método de búsqueda no válido. Por favor, ingrese 'ID' o 'nombre'.")

        elif opcion == "3": # Modificar la cantidad de un producto 
            os.system('cls')
            metodo_valido = False
            while not metodo_valido:
                metodo_busqueda = input("¿Desea buscar por ID o por nombre? (Ingrese 'ID' o 'nombre'): ").strip().lower()
                if metodo_busqueda == 'id':
                    id_producto = int(input("Ingrese el ID del producto que desea modificar: "))
                    producto = funciones.buscar_producto(id_producto=id_producto)
                    if producto:
                        nueva_cantidad = int(input("Ingrese la nueva cantidad del producto: "))
                        funciones.actualizar_producto(id_producto=id_producto, nueva_cantidad=nueva_cantidad)
                    metodo_valido = True
                elif metodo_busqueda == 'nombre':
                    nombre_producto = input("Ingrese el nombre del producto que desea modificar: ")
                    producto = funciones.buscar_producto(nombre_producto=nombre_producto)
                    if producto:
                        nueva_cantidad = int(input("Ingrese la nueva cantidad del producto: "))
                        funciones.actualizar_producto(nombre_producto=nombre_producto, nueva_cantidad=nueva_cantidad)
                    metodo_valido = True
                else:
                    print("Método de búsqueda no válido. Por favor, ingrese 'ID' o 'nombre'.")

        elif opcion == "4":  # Eliminar un producto del inventario
            os.system('cls')
            metodo_valido = False
            while not metodo_valido:
                metodo_busqueda = input("¿Desea eliminar por ID o por nombre? (Ingrese 'ID' o 'nombre'): ").strip().lower()
                if metodo_busqueda == 'id':
                    id_producto = int(input("Ingrese el ID del producto que desea eliminar: "))
                    funciones.eliminar_producto(id_producto=id_producto)
                    metodo_valido = True
                elif metodo_busqueda == 'nombre':
                    nombre_producto = input("Ingrese el nombre del producto que desea eliminar: ")
                    funciones.eliminar_producto(nombre_producto=nombre_producto)
                    metodo_valido = True
                else:
                    print("Método de búsqueda no válido. Por favor, ingrese 'ID' o 'nombre'.")

        elif opcion == "5": # Listar productos registrados
            os.system('cls')
            productos = funciones.listar_productos()
            if productos:
                print(Fore.GREEN + f"Productos registrados: {productos}")

        elif opcion == "6":  # Opción para listar los productos de bajo stock dependiendo la cantidad definida por el usuario.
            os.system('cls')
            cantidad_limite = int(input("Ingrese la cantidad mínima de stock para listar los productos: "))
            funciones.listar_stock_bajo(cantidad_limite)

        elif opcion == "7":
            print("Finalizó la sesión del programa.")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

if __name__ == "__main__":
    main()