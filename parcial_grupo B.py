import json

DATA_FILE = "panaderia.json"
USER_FILE = "usuarios.json"

def cargar_datos():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"productos_base": [], "productos_derivados": [], "ganancias": 0}

def guardar_datos(datos):
    with open(DATA_FILE, "w") as file:
        json.dump(datos, file, indent=4)

def cargar_usuarios():
    try:
        with open(USER_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open(USER_FILE, "w") as file:
        json.dump(usuarios, file, indent=4)

def registrar_usuario():
    usuarios = cargar_usuarios()
    print("Registro de nuevo usuario")
    usuario_id = input("Ingrese un identificador único para su cuenta (por ejemplo: Numero de telefono): ")
    if usuario_id in usuarios:
        print("Este identificador ya está registrado. Intenta con otro.")
        return
    nombre = input("Ingrese su nombre: ")
    edad = input("Ingrese su edad: ")
    usuarios[usuario_id] = {"nombre": nombre, "edad": edad}
    guardar_usuarios(usuarios)
    print("Usuario registrado con éxito.")

def autenticar_usuario():
    usuarios = cargar_usuarios()
    print("Autenticación de usuario")
    usuario_id = input("Ingrese su identificador único (usuario o alias): ")
    if usuario_id in usuarios:
        print(f"Bienvenido, {usuarios[usuario_id]['nombre']}!")
        return True
    else:
        print("Usuario no encontrado. ¿Desea registrarse?")
        respuesta = input("¿Registrar usuario? (s/n): ").lower()
        if respuesta == 's':
            registrar_usuario()
            return True
        else:
            return False

def agregar_producto_base(datos):
    nombre = input("Nombre del producto base (Ejemplo: Harina, Huevos): ")
    cantidad_comprada = float(input("Cantidad comprada (en unidades o kg): "))
    precio_compra = float(input("Precio de compra por unidad: "))
    producto = {"nombre": nombre, "cantidad_comprada": cantidad_comprada, "precio_compra": precio_compra}
    datos["productos_base"].append(producto)
    print(f"Producto base '{nombre}' agregado con éxito.")

def agregar_producto_derivado(datos):
    nombre = input("Nombre del producto derivado: ")
    precio_unitario = float(input("Precio unitario del producto derivado: "))
    cantidad_necesaria = float(input(f"Cantidad de producto base necesario para hacer un {nombre}: "))
    cantidad_disponible = float(input("Cantidad disponible del producto derivado: "))
    total_precio = precio_unitario * cantidad_disponible
    producto = {"nombre": nombre, "precio_unitario": precio_unitario, "cantidad_necesaria": cantidad_necesaria, "cantidad_disponible": cantidad_disponible, "total_precio": total_precio}
    datos["productos_derivados"].append(producto)
    print(f"Producto derivado '{nombre}' agregado con éxito.")

def eliminar_producto(datos, tipo):
    lista = datos["productos_base"] if tipo == "base" else datos["productos_derivados"]
    if not lista:
        print("No hay productos para eliminar.")
        return
    for i, producto in enumerate(lista):
        if tipo == "base":
            print(f"{i + 1}. {producto['nombre']} | Precio Unitario: {producto['precio_compra']}")
        elif tipo == "derivados":
            print(f"{i + 1}. {producto['nombre']} | Precio Unitario: {producto['precio_unitario']} | Total: {producto['total_precio']}")
    try:
        index = int(input("Selecciona el número del producto a eliminar: ")) - 1
        eliminado = lista.pop(index)
        print(f"Producto '{eliminado['nombre']}' eliminado.")
    except (IndexError, ValueError):
        print("Selección inválida.")

def ver_productos(datos, tipo):
    lista = datos["productos_base"] if tipo == "base" else datos["productos_derivados"]
    if not lista:
        print("No hay productos registrados.")
    else:
        for i, producto in enumerate(lista):
            if tipo == "base":
                print(f"{i + 1}. {producto['nombre']} | Cantidad disponible: {producto['cantidad_comprada']} | Precio Unitario: {producto['precio_compra']}")
            elif tipo == "derivados":
                ganancia_posible = producto["cantidad_disponible"] * producto["precio_unitario"]
                print(f"{i + 1}. {producto['nombre']} | Cantidad disponible: {producto['cantidad_disponible']} | Precio Unitario: {producto['precio_unitario']} | Ganancia potencial: {ganancia_posible:.2f} | Total: {producto['total_precio']}")

def ordenar_productos(datos, tipo, criterio, descendente=False):
    lista = datos["productos_base"] if tipo == "base" else datos["productos_derivados"]
    
    # Se usa el criterio para ordenar
    lista.sort(key=lambda p: p.get(criterio, 0), reverse=descendente)
    print(f"Productos {tipo} ordenados por {criterio}.")

def buscar_producto(datos, tipo, nombre):
    lista = datos["productos_base"] if tipo == "base" else datos["productos_derivados"]
    resultados = [p for p in lista if nombre.lower() in p["nombre"].lower()]
    if resultados:
        print("Resultados de la búsqueda:")
        for producto in resultados:
            print(producto)
    else:
        print("No se encontraron coincidencias.")

def registrar_venta(datos):
    ver_productos(datos, "derivados")
    try:
        index = int(input("Selecciona el producto derivado que se vendió: ")) - 1
        cantidad_vendida = float(input("¿Cuántos productos fueron vendidos? "))
        producto_vendido = datos["productos_derivados"][index]
        if cantidad_vendida <= producto_vendido["cantidad_disponible"]:
            producto_vendido["cantidad_disponible"] -= cantidad_vendida
            ganancia = cantidad_vendida * producto_vendido["precio_unitario"]
            datos["ganancias"] += ganancia
            monto_a_recibir = ganancia
            print(f"Venta registrada: {ganancia} ganados.")
            print(f"Total a recibir por la venta: {monto_a_recibir}")
        else:
            print("No hay suficiente cantidad disponible para la venta.")
    except (IndexError, ValueError):
        print("Selección inválida.")

def menu_principal():
    print("\nMenú principal:")
    print("1. Agregar producto base")
    print("2. Agregar producto derivado")
    print("3. Eliminar producto base")
    print("4. Eliminar producto derivado")
    print("5. Ver productos base")
    print("6. Ver productos derivados")
    print("7. Ordenar productos")
    print("8. Buscar producto")
    print("9. Registrar venta")
    print("10. Ver ganancias acumuladas")
    print("11. Salir")

def main():
    datos = cargar_datos()
    if autenticar_usuario():  # Solo permitimos acceder al menú si el usuario está autenticado
        while True:
            menu_principal()
            opcion = input("Selecciona una opción: ")
            if opcion == "1":
                agregar_producto_base(datos)
            elif opcion == "2":
                agregar_producto_derivado(datos)
            elif opcion == "3":
                eliminar_producto(datos, "base")
            elif opcion == "4":
                eliminar_producto(datos, "derivados")
            elif opcion == "5":
                ver_productos(datos, "base")
            elif opcion == "6":
                ver_productos(datos, "derivados")
            elif opcion == "7":
                tipo = input("¿Qué productos deseas ordenar? (base/derivados): ")
                criterio = input("Criterio (nombre, cantidad_comprada, precio_compra): ")
                descendente = input("¿Orden descendente? (s/n): ").lower() == "s"
                ordenar_productos(datos, tipo, criterio, descendente)
            elif opcion == "8":
                tipo = input("¿Dónde buscar? (base/derivados): ")
                nombre = input("Nombre del producto a buscar: ")
                buscar_producto(datos, tipo, nombre)
            elif opcion == "9":
                registrar_venta(datos)
            elif opcion == "10":
                print(f"Ganancias acumuladas hasta ahora: {datos['ganancias']}")
            elif opcion == "11":
                guardar_datos(datos)
                print("Datos guardados. Saliendo del programa.")
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
    else:
        print("No se pudo autenticar al usuario. Saliendo del programa.")

if __name__ == "__main__":
    main()

