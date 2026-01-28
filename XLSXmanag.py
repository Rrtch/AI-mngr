import pandas as pd

ruta="C:/Users/casti/Desktop/DeskDrive/FissioT_DataBase.xlsx"

def leer_base():
    return pd.read_excel(ruta)

def verificar_id(ID):
    df = leer_base()
    # Forma 1: con `isin`
    existe = ID in df["id"].values
    #print(existe)  # True o False
    return existe

def leer_registro(ID):
    """Devuelve un único registro por su ID como string legible."""
    df = leer_base()
    resultado = df[df["id"] == ID]

    if not resultado.empty:
        # Tomamos la primera fila como Series
        fila = resultado.iloc[0]

        # Convertimos a string: clave=valor separados por comas
        #s = ", ".join(f"{col}={fila[col]}" for col in fila.index)
        #fila = resultado.iloc[0]

        # Convertimos a lista
        s = [str(v) for v in fila if pd.notna(v)]
        s.insert(0,"User data = ")
        return s
    

    else:
        return None

def insertar_registro(nuevo):
    """
    Inserta un nuevo registro en la base.
    `nuevo` debe ser un diccionario con las mismas columnas que la base.
    """
    df = leer_base()
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_excel(ruta, index=False)
    print(f"Registro insertado: {nuevo}")

def actualizar_registro(id_buscar, cambios):
    """
    Actualiza un registro por ID.
    `cambios` es un diccionario con las columnas a modificar.
    """
    df = leer_base()  # 1. leer el Excel en un DataFrame

    # 2. Recorrer el diccionario de cambios
    for columna, valor in cambios.items():
        # 3. Localizar la fila donde id == id_buscar y cambiar la columna
        df.loc[df["id"] == id_buscar, columna] = valor

    # 4. Guardar de nuevo el DataFrame en el Excel
    df.to_excel(ruta, index=False)
    print(f"Registro {id_buscar} actualizado con {cambios}")

def actualizar_registro_si_vacio(id_buscar, cambios):
    """
    Actualiza un registro por ID, pero solo reemplaza los campos vacíos.
    `cambios` es un diccionario con posibles nuevos valores.
    """
    df = leer_base()

    # Reemplazar solo donde el campo esté vacío
    for columna, valor in cambios.items():
        # Localizar el valor actual de esa celda
        valor_actual = df.loc[df["id"] == id_buscar, columna].values[0]

        # Si está vacío (NaN o cadena vacía), se reemplaza
        if pd.isna(valor_actual) or valor_actual == "":
            df.loc[df["id"] == id_buscar, columna] = valor

    # Guardar cambios
    df.to_excel(ruta, index=False)
    print(f"Registro {id_buscar} actualizado solo en campos vacíos con {cambios}")

def crear_registro(id):
    if verificar_id(id):
        print("El ID ya existe.")
        return
    else:
        insertar_registro({"id":id})
        return
