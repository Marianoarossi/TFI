Librerias necesarias:

Ejecutar:
pip install colorama
-----

En la misma carpeta se encontraran el modulo funciones.py que es utilizado en el main.py para hacer funcionar el codigo junto a su base de datos inventario.db.

La funcion main()  inicializa limpiando la pantalla de la terminal. Luego llama a la funcion crear_tabla() en la cual si no existe crea una tabla llamada productos con los siguientes campos:
id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            categoria TEXT


Luego el sistema arroja un mensaje color verde de bienvenida usando la libreria colorama . Seguido a eso muestra el menú de opciones :
        1. Agregar producto al inventario
        2. Consultar de un producto
        3. Modificar la cantidad de un producto
        4. Eliminar un producto del inventario
        5. Listar productos registrados
        6. Listar productos con stock bajo
        7. Salir

Se realiza un bucle para permanecer en el menú hasta que se seleccione  opción = 7 para salir.

En cada opción se realizan unas validaciones y luego llama a la funcion del modulo funciones.py
Se trabajo con el ingreso de datos convertidos a mayusculas. 

