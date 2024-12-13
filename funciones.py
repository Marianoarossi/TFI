import sqlite3  
from colorama import Fore, Style, init


# Inicializar colorama
init(autoreset=True)

############################################################################
def crear_tabla():
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT
        )
    ''')
    print("Tabla 'productos' creada exitosamente.")
    conexion.commit()
    conexion.close()     
    
###############################################################################

#funcion para validar si existe o no el producto.
def producto_existe(nombre):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    cursor.execute('''
        SELECT * FROM productos
        WHERE nombre = ?
    ''', (nombre,))
    producto_existente = cursor.fetchone()
    
    conexion.close()
    return producto_existente is not None
##############################################################################

#Llamada a la función agregar_producto()

def agregar_producto(nombre, descripcion, cantidad, precio, categoria):
    nombre = nombre.upper()
    descripcion = descripcion.upper()
    categoria = categoria.upper()
    
    # Validar que la cantidad sea un entero mayor a 0
    try:
        cantidad = int(cantidad)
        if cantidad <= 0:
            print(Fore.RED + "Error: La cantidad debe ser mayor a 0.")
            return
    except ValueError:
        print(Fore.RED + "Error: La cantidad debe ser un número entero.")
        return
    
    # Validar que el precio sea un float mayor a 0
    try:
        precio = float(precio)
        if precio <= 0:
            print(Fore.RED + "Error: El precio debe ser mayor a 0.")
            return
    except ValueError:
        print(Fore.RED + "Error: El precio debe ser un número.")
        return
    
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, cantidad, precio, categoria))
    conexion.commit()
    print(Fore.GREEN + f"\nProducto '{nombre}' agregado al inventario.")
    
    conexion.close()

##############################################################################

#Llamada a la función listar_productos()
def listar_productos():
    # Conectar a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    # Ejecutar la consulta para obtener todos los productos
    cursor.execute('''
        SELECT * FROM productos
    ''')
    productos = cursor.fetchall()
    conexion.close()
    
    # Verificar si hay productos en la base de datos
    if len(productos) == 0:
        print(Fore.RED + "No hay productos registrados en el Inventario.")
        return []
    else:
        # Definir los encabezados de las columnas
        headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        
        # Calcular el ancho de cada columna
        col_widths = [len(header) for header in headers]
        for producto in productos:
            for i, value in enumerate(producto):
                col_widths[i] = max(col_widths[i], len(str(value)))
        
        # Crear una cadena de formato para la tabla
        format_str = " | ".join([f"{{:<{width}}}" for width in col_widths])
        
        # Imprimir los encabezados de la tabla
        print(Fore.CYAN + format_str.format(*headers))
        print(Fore.CYAN + "-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        
        # Imprimir cada fila de la tabla
        for producto in productos:
            print(Fore.CYAN + format_str.format(*producto))
            #return productos
        
##############################################################################
    #Llamada a la función ActualizarProducto()
def actualizar_producto(id_producto=None, nombre_producto=None, nueva_cantidad=None):
    try:
        conexion = sqlite3.connect("inventario.db")
        cursor = conexion.cursor()
        if id_producto:
            cursor.execute('''
                UPDATE productos
                SET cantidad = ?
                WHERE id = ?
            ''', (nueva_cantidad, id_producto))
        elif nombre_producto:
            nombre_producto = nombre_producto.upper()
            cursor.execute('''
                UPDATE productos
                SET cantidad = ?
                WHERE nombre = ?
            ''', (nueva_cantidad, nombre_producto))
        
        if cursor.rowcount == 0:
            raise ValueError("Producto no encontrado.")
        
        conexion.commit()
        print(Fore.GREEN + f"Cantidad del producto actualizada a {nueva_cantidad}.")
    except ValueError as ve:
        print(ve)
    except sqlite3.Error as e:
        print(Fore.RED +f"Error en la base de datos: {e}")
    finally:
        conexion.close()
##############################################################################

    #Llamada a la función EliminarProducto()
def eliminar_producto(id_producto=None, nombre_producto=None):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    # Obtener los detalles del producto antes de eliminarlo
    if id_producto:
        cursor.execute('''
            SELECT * FROM productos
            WHERE id = ?
        ''', (id_producto,))
    elif nombre_producto:
        nombre_producto = nombre_producto.upper()
        cursor.execute('''
            SELECT * FROM productos
            WHERE nombre = ?
        ''', (nombre_producto,))
    
    producto = cursor.fetchone()
    
    if not producto:
        print(Fore.RED + "\nNo se encontró un producto con el ID o nombre especificado.")
        conexion.close()
        return
    
    # Eliminar el producto
    if id_producto:
        cursor.execute('''
            DELETE FROM productos
            WHERE id = ?
        ''', (id_producto,))
    elif nombre_producto:
        cursor.execute('''
            DELETE FROM productos
            WHERE nombre = ?
        ''', (nombre_producto,))
    
    conexion.commit()
    
    # Mostrar el producto eliminado
    print(Fore.RED + f"\nProducto '{producto[1]}' eliminado del inventario.")
    
    conexion.close()
##############################################################################

#Llamada a la función buscar_producto_por_nombre()
def buscar_producto(id_producto=None, nombre_producto=None):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    if id_producto:
        cursor.execute('''
            SELECT * FROM productos
            WHERE id = ?
        ''', (id_producto,))
    elif nombre_producto:
        nombre_producto = nombre_producto.upper()
        cursor.execute('''
            SELECT * FROM productos
            WHERE nombre = ?
        ''', (nombre_producto,))
    else:
        print(Fore.YELLOW +"\nDebe proporcionar un ID o un nombre para buscar el producto.")
        return None
    
    producto = cursor.fetchone()
    conexion.close()
    if producto:
        print(Fore.LIGHTBLUE_EX +f"\nProducto encontrado - ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
        return producto
    else:
        print(Fore.RED +"\nProducto no encontrado.")
        return None
##############################################################################

#Llamada a la función ListarStockBajo()
def listar_stock_bajo(cantidad_limite):
    # Conectar a la base de datos
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    # Ejecutar la consulta para obtener los productos con stock bajo
    cursor.execute('''
        SELECT * FROM productos
        WHERE cantidad <= ?
    ''', (cantidad_limite,))
    productos_bajo_stock = cursor.fetchall()
    conexion.close()
    
    # Verificar si hay productos con stock bajo
    if len(productos_bajo_stock) == 0:
        print(Fore.RED + "\nNo hay productos con stock bajo.")
    else:
        # Definir los encabezados de las columnas
        headers = ["ID", "Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
        
        # Calcular el ancho de cada columna
        col_widths = [len(header) for header in headers]
        for producto in productos_bajo_stock:
            for i, value in enumerate(producto):
                col_widths[i] = max(col_widths[i], len(str(value)))
        
        # Crear una cadena de formato para la tabla
        format_str = " | ".join([f"{{:<{width}}}" for width in col_widths])
        
        # Imprimir los encabezados de la tabla en verde
        print(Fore.GREEN + format_str.format(*headers))
        print(Fore.GREEN + "-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        
        # Imprimir cada fila de la tabla en verde
        for producto in productos_bajo_stock:
            print(Fore.GREEN + format_str.format(*producto))
##############################################################################
