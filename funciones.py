import sqlite3  

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
    conexion.commit()
    conexion.close()     
    print("Tabla 'productos' creada exitosamente.")


#Llamada a la función agregar_producto()
def agregar_producto(nombre, descripcion, cantidad, precio, categoria):
    nombre = nombre.upper()
    descripcion = descripcion.upper()
    categoria = categoria.upper()
    
    # Validar que la cantidad sea un entero
    try:
        cantidad = int(cantidad)
    except ValueError:
        print("Error: La cantidad debe ser un número entero.")
        return
    
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    
    # Verificar si el producto ya existe
    cursor.execute('''
        SELECT * FROM productos
        WHERE nombre = ?
    ''', (nombre,))
    producto_existente = cursor.fetchone()
    
    if producto_existente:
        print(f"El producto '{nombre}' ya existe en el inventario. Modifique el producto existente.")
    else:
        cursor.execute('''
            INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
            VALUES (?, ?, ?, ?, ?)
        ''', (nombre, descripcion, cantidad, precio, categoria))
        conexion.commit()
        print(f"Producto '{nombre}' agregado al inventario.")
    
    conexion.close()


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
        print("No hay productos registrados en el Inventario.")
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
        print(format_str.format(*headers))
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        
        # Imprimir cada fila de la tabla
        for producto in productos:
            print(format_str.format(*producto))
        
        #return productos
        
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
        print(f"Cantidad del producto actualizada a {nueva_cantidad}.")
    except ValueError as ve:
        print(ve)
    except sqlite3.Error as e:
        print(f"Error en la base de datos: {e}")
    finally:
        conexion.close()

    #Llamada a la función EliminarProducto()
def eliminar_producto(id_producto=None, nombre_producto=None):
    conexion = sqlite3.connect("inventario.db")
    cursor = conexion.cursor()
    if id_producto:
        cursor.execute('''
            DELETE FROM productos
            WHERE id = ?
        ''', (id_producto,))
    elif nombre_producto:
        nombre_producto = nombre_producto.upper()
        cursor.execute('''
            DELETE FROM productos
            WHERE nombre = ?
        ''', (nombre_producto,))
    
    if cursor.rowcount == 0:
        print("No se encontró un producto con el ID o nombre especificado.")
    else:
        print("Producto eliminado del inventario.")
    
    conexion.commit()
    conexion.close()


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
        print("Debe proporcionar un ID o un nombre para buscar el producto.")
        return None
    
    producto = cursor.fetchone()
    conexion.close()
    if producto:
        print(f"Producto encontrado - ID: {producto[0]}, Nombre: {producto[1]}, Descripción: {producto[2]}, Cantidad: {producto[3]}, Precio: {producto[4]}, Categoría: {producto[5]}")
        return producto
    else:
        print("Producto no encontrado.")
        return None

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
        print("No hay productos con stock bajo.")
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
        
        # Imprimir los encabezados de la tabla
        print(format_str.format(*headers))
        print("-" * (sum(col_widths) + 3 * (len(headers) - 1)))
        
        # Imprimir cada fila de la tabla
        for producto in productos_bajo_stock:
            print(format_str.format(*producto))
