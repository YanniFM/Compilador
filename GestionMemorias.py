import sys # Importa el módulo sys, que proporciona acceso a algunas variables y funciones interactuando con el intérprete de Python.

from DistribucionMemoria import (
    # Constantes: Direcciones de memoria para diferentes tipos de datos constantes.
    Constante_Bool, Constante_Entero, Constante_Flotante, Constante_Caracter, Constante_Cadena, Limite_Constante,
    # Globales: Direcciones de memoria para variables globales y su límite.
    Global_Entero, Global_Flotante, Global_Caracter, Limite_Global,
    # Locales: Direcciones de memoria para variables locales y su límite.
    Local_Entero, Local_Flotante, Local_Caracter, Limite_Local,
    # Temporales Locales: Direcciones para variables temporales locales y su límite.
    TemporalLocal_Bool, TemporalLocal_Entero, TemporalLocal_Flotante, TemporalLocal_Caracter, TemporalLocal_Cadena, Limite_TemporalLocal,
    # Temporales Globales: Direcciones para variables temporales globales y su límite.
    TemporalGlobal_Bool, TemporalGlobal_Entero, TemporalGlobal_Flotante, TemporalGlobal_Caracter, TemporalGlobal_Cadena, Limite_TemporalGlobal
)

# Clase para la gestión de memoria global.
class MemoriaGlobal:
    def __init__(self) -> None:
        # Inicializa contadores y listas para cada tipo de variable global.
        self.contadorEnteros = 0
        self.listaEnteros = []
        self.contadorFlotantes = 0
        self.listaFlotantes = []
        self.contadorCaracteres = 0
        self.listaCaracteres = []

    # Asignación de memoria para nuevas variables globales.
    def asignarMemoria(self, var):
        # Identifica el tipo de variable y asigna memoria adecuadamente.
        varType = var.get("type")
        # Asignación de memoria para enteros.
        if varType == "int":
            dir = Global_Entero
            arrSize = int(var.get("arrSize"))
            dir += self.contadorEnteros + arrSize
            # Verifica si hay espacio disponible en la memoria global para enteros.
            if dir < Global_Entero or dir >= Global_Flotante:
                print("no global memory for int variables available")
                sys.exit()
            else:
                # Asigna memoria y actualiza el contador de enteros.
                if arrSize > 1:
                    self.contadorEnteros += arrSize
                    dir -= arrSize
                    for i in range(arrSize):
                        self.listaEnteros.append(0)
                else:
                    self.contadorEnteros += 1
                    self.listaEnteros.append(0)

        # Asignación de memoria para flotantes.
        elif varType == "float":
            dir = Global_Flotante
            arrSize = int(var.get("arrSize"))
            dir += self.contadorFlotantes + arrSize
            # Verifica si hay espacio disponible en la memoria global para flotantes.
            if dir < Global_Flotante or dir >= Global_Caracter:
                print("no global memory for float variables available")
                sys.exit()

            else:
                # Asigna memoria y actualiza el contador de flotantes.
                if arrSize > 1:
                    self.contadorFlotantes += arrSize
                    dir -= arrSize
                    for i in range(arrSize):
                        self.listaFlotantes.append(0.0)
                else:
                    self.contadorFlotantes += 1
                    self.listaFlotantes.append(0.0)

        else:
            # Asignación de memoria para caracteres.
            dir = Global_Caracter
            arrSize = int(var.get("arrSize"))
            dir += self.contadorCaracteres + arrSize
            # Verifica si hay espacio disponible en la memoria global para caracteres.
            if dir < Global_Caracter or dir >= Limite_Global:
                print("no global memory for char variables available")
                sys.exit()

            else:
                # Asigna memoria y actualiza el contador de caracteres.
                if arrSize > 1:
                    self.contadorCaracteres += arrSize
                    dir -= arrSize
                    for i in range(arrSize):
                        self.listaCaracteres.append(" ")
                else:
                    self.contadorCaracteres += 1
                    self.listaCaracteres.append(" ")

        return dir

    # Obtiene el valor almacenado en una dirección de memoria específica.
    def obtenerValor(self, dir):
        if dir < Global_Entero or dir >= Limite_Global:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < Global_Flotante:
            return self.listaEnteros[dir - Global_Entero]
        elif dir < Global_Caracter:
            return self.listaFlotantes[dir - Global_Flotante]
        elif dir < Limite_Global:
            return self.listaCaracteres[dir - Global_Caracter]

    # Guarda un valor en una dirección de memoria específica.
    def guardarValor(self, dir, value):
        if dir < Global_Entero or dir >= Limite_Global:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < Global_Flotante:
            self.listaEnteros[dir - Global_Entero] = value
        elif dir < Global_Caracter:
            self.listaFlotantes[dir - Global_Flotante] = value
        elif dir < Limite_Global:
            self.listaCaracteres[dir - Global_Caracter] = value

    # Lee un valor del usuario y lo guarda en una dirección de memoria específica.
    def read(self, dir, value):
        if dir < Global_Entero or dir >= Limite_Global:
            print("Invalid direction for variable")
            sys.exit()

        # Procesa el valor de entrada según el tipo de la dirección de memoria.
        elif dir < Global_Flotante:
            try:
                # Intenta convertir el valor a entero.
                value = int(value)
            except:
                # Muestra un error si el valor no es entero.
                print(f"Input value {value} is not of type int")
                sys.exit()
            # Guarda el valor entero en la dirección especificada.
            self.listaEnteros[dir - Global_Entero] = value

        elif dir < Global_Caracter:
            try:
                # Intenta convertir el valor a flotante.
                value = float(value)
            except:
                # Muestra un error si el valor no es flotante.
                print(f"Input value {value} is not of type float")
                sys.exit()
            # Guarda el valor flotante en la dirección especificada.
            self.listaFlotantes[dir - Global_Flotante] = value

        elif dir < Limite_Global:
            # Verifica si el valor es un solo carácter.
            if len(value) > 1:
                print(f"Input value {value} is not of type char")
                sys.exit()
            # Guarda el valor de carácter en la dirección especificada.
            else:
                self.listaCaracteres[dir - Global_Caracter] = value


# Clase diseñada para la gestión de variables locales
class MemoriaLocal:
    def __init__(self) -> None:
        # Inicialización de contadores y listas para la gestión de la memoria local.
        self.contadorEnteros = 0
        self.listaEnteros = []
        self.contadorFlotantes = 0
        self.listaFlotantes = []
        self.contadorCaracteres = 0
        self.listaCaracteres = []
        # Mapa de desplazamiento para manejar el offset de las variables locales.
        self.varOffsetMap = {"int": 0, "float": 0, "char": 0}

    def asignarMemoria(self, var):
        # Asigna memoria para una nueva variable local según su tipo y tamaño.
        varType = var.get("type")

        if varType == "int":
            # Asignación de memoria para variables enteras locales.
            dir = Local_Entero
            arrSize = int(var.get("arrSize"))
            dir += self.contadorEnteros + arrSize
            # Verifica si hay suficiente espacio disponible en el rango de memoria local para enteros.
            if dir < Local_Entero or dir >= Local_Flotante:
                print("no local memory for int variables available")
                sys.exit()
            else:
                # Aumenta el contador de enteros y asigna espacio para la variable o arreglo.
                if arrSize > 1:
                    self.contadorEnteros += arrSize
                    dir -= arrSize
                else:
                    self.contadorEnteros += 1

        elif varType == "float":
            # Asignación de memoria para variables flotantes locales.
            dir = Local_Flotante
            arrSize = int(var.get("arrSize"))
            dir += self.contadorFlotantes + arrSize
            # Verifica si hay suficiente espacio disponible en el rango de memoria local para flotantes.
            if dir < Local_Flotante or dir >= Local_Caracter:
                print("no local memory for float variables available")
                sys.exit()
            else:
                # Aumenta el contador de flotantes y asigna espacio para la variable o arreglo.
                if arrSize > 1:
                    self.contadorFlotantes += arrSize
                    dir -= arrSize
                else:
                    self.contadorFlotantes += 1

        else:
            # Asignación de memoria para variables de carácter locales.
            dir = Local_Caracter
            arrSize = int(var.get("arrSize"))
            dir += self.contadorCaracteres + arrSize
            # Verifica si hay suficiente espacio disponible en el rango de memoria local para caracteres.
            if dir < Local_Caracter or dir >= Limite_Local:
                print("no local memory for char variables available")
                sys.exit()
            else:
                # Aumenta el contador de caracteres y asigna espacio para la variable o arreglo.
                if arrSize > 1:
                    self.contadorCaracteres += arrSize
                    dir -= arrSize
                else:
                    self.contadorCaracteres += 1

        return dir

    def clear(self):
        # Crear y devolver un diccionario con la cantidad de memoria requerida para cada tipo de variable.
        reqMem = {
            "int": self.contadorEnteros,
            "float": self.contadorFlotantes,
            "char": self.contadorCaracteres,
        }

        # Resetear los contadores de cada tipo de variable a 0.
        self.contadorEnteros = 0
        self.contadorFlotantes = 0
        self.contadorCaracteres = 0

        return reqMem

    def era(self, reqMem):
        # Asignar espacio e inicializar variables locales, además de guardar el desplazamiento actual.
        self.varOffsetMap = {
            "int": self.contadorEnteros,
            "float": self.contadorFlotantes,
            "char": self.contadorCaracteres,
        }

        ints = reqMem.get("int")
        self.contadorEnteros += ints
        floats = reqMem.get("float")
        self.contadorFlotantes += floats
        chars = reqMem.get("char")
        self.contadorCaracteres += chars

        if self.contadorEnteros >= Local_Flotante:
            print("no local memory for int variables available")
            sys.exit()
        else:
            for i in range(ints):
                self.listaEnteros.append(0)

        if self.contadorFlotantes >= Local_Caracter:
            print("no local memory for float variables available")
            sys.exit()
        else:
            for i in range(floats):
                self.listaFlotantes.append(0.0)

        if self.contadorCaracteres >= Limite_Local:
            print("no local memory for char variables available")
            sys.exit()
        else:
            for i in range(chars):
                self.listaCaracteres.append(" ")

    def pop(self, reqMem):
        # Liberar la memoria no requerida y revertir el desplazamiento al estado anterior.
        ints = reqMem.get("int")
        self.contadorEnteros -= ints
        floats = reqMem.get("float")
        self.contadorFlotantes -= floats
        chars = reqMem.get("char")
        self.contadorCaracteres -= chars

        self.reajustarDesplazamiento(reqMem)

        if ints > 0:
            self.listaEnteros = self.listaEnteros[:-ints]
        if floats > 0:
            self.listaFlotantes = self.listaFlotantes[:-floats]
        if chars > 0:
            self.listaCaracteres = self.listaCaracteres[:-chars]

    def reajustarDesplazamiento(self, reqMem):
        # Ajustar el mapa de desplazamiento al liberar memoria.
        ints = reqMem.get("int")
        floats = reqMem.get("float")
        chars = reqMem.get("char")

        self.varOffsetMap["int"] -= ints
        if self.varOffsetMap["int"] < 0:
            self.varOffsetMap["int"] = 0
        self.varOffsetMap["float"] -= floats
        if self.varOffsetMap["float"] < 0:
            self.varOffsetMap["float"] = 0
        self.varOffsetMap["char"] -= chars
        if self.varOffsetMap["char"] < 0:
            self.varOffsetMap["char"] = 0

    def obtenerValor(self, dir):
        # Obtener el valor de la variable en la dirección especificada.
        if dir < Local_Entero or dir >= Limite_Local:
            print("Invalid direction for variable")
            sys.exit()
        elif dir < Local_Flotante:
            return self.listaEnteros[dir - Local_Entero + self.varOffsetMap["int"]]

        elif dir < Local_Caracter:
            return self.listaFlotantes[dir - Local_Flotante + self.varOffsetMap["float"]]

        elif dir < Limite_Local:
            return self.listaCaracteres[dir - Local_Caracter + self.varOffsetMap["char"]]

    def obtenerParametro(self, dir, reqMem):
        # Obtener el valor del parámetro en la dirección especificada, considerando el desplazamiento y la memoria requerida.
        if dir < Local_Entero or dir >= Limite_Local:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < Local_Flotante:
            return self.listaEnteros[
                dir - Local_Entero + self.varOffsetMap["int"] - reqMem["int"]
            ]

        elif dir < Local_Caracter:
            return self.listaFlotantes[
                dir - Local_Flotante + self.varOffsetMap["float"] - reqMem["float"]
            ]

        elif dir < Limite_Local:
            return self.listaCaracteres[
                dir - Local_Caracter + self.varOffsetMap["char"] - reqMem["char"]
            ]

    def guardarValor(self, dir, value):
        # Guarda un valor en una dirección de memoria específica dentro de la memoria local.
        if dir < Local_Entero or dir >= Limite_Local:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < Local_Flotante:
            self.listaEnteros[dir - Local_Entero + self.varOffsetMap["int"]] = value

        elif dir < Local_Caracter:
            self.listaFlotantes[dir - Local_Flotante + self.varOffsetMap["float"]] = value

        elif dir < Limite_Local:
            self.listaCaracteres[dir - Local_Caracter + self.varOffsetMap["char"]] = value

    def read(self, dir, value):
        # Lee un valor de entrada y lo guarda en la dirección de memoria especificada.
        if dir < Local_Entero or dir >= Limite_Local:
            print("Invalid direction for variable")
            sys.exit()

        elif dir < Local_Flotante:
            try:
                value = int(value)
            except:
                print(f"Input value {value} is not of type int")
                sys.exit()
            self.listaEnteros[dir - Local_Entero + self.varOffsetMap["int"]] = value

        elif dir < Local_Caracter:
            try:
                value = float(value)
            except:
                print(f"Input value {value} is not of type float")
                sys.exit()
            self.listaFlotantes[dir - Local_Flotante + self.varOffsetMap["float"]] = value

        elif dir < Limite_Local:
            if len(value) > 1:
                print(f"Input value {value} is not of type char")
                sys.exit()
            else:
                self.listaCaracteres[dir - Local_Caracter + self.varOffsetMap["char"]] = value


# Gestor de memoria temporal
class MemoriaTemporal:
    def __init__(self) -> None:
        # Inicialización de contadores para temporales globales.
        self.contadorGlobalBool = 0
        self.contadorGlobalEntero = 0
        self.contadorGlobalFlotante = 0
        self.contadorGlobalCaracter = 0
        self.contadorGlobalCadena = 0

        # Inicialización de listas para almacenar temporales globales.
        self.listaGlobalBool = []
        self.listaGlobalEntero = []
        self.listaGlobalFlotante = []
        self.listaGlobalCaracter = []
        self.listaGlobalCadena = []

        # Inicialización de contadores para temporales locales.
        self.contadorLocalBool = 0
        self.contadorLocalEntero = 0
        self.contadorLocalFlotante = 0
        self.contadorLocalCaracter = 0
        self.contadorLocalCadena = 0

        # Inicialización de listas para almacenar temporales locales.
        self.listaLocalBool = []
        self.listaLocalEntero = []
        self.listaLocalFlotante = []
        self.listaLocalCaracter = []
        self.listaLocalCadena = []

        # Inicialización del mapa de desplazamiento temporal.
        self.DesplazamientoTemporal = {"bool": 0, "int": 0, "float": 0, "char": 0, "string": 0}

    def asignarMemoria(self, tempType, isLocal):
        # Asignación de memoria para variables temporales.
        if isLocal:
            # Proceso para temporales locales según el tipo de variable.
            # Asignación para booleanos locales.
            if tempType == "bool":
                dir = TemporalGlobal_Bool
                dir += self.contadorLocalBool
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalGlobal_Bool or dir >= TemporalGlobal_Entero:
                    print("no local memory for bool temps available")
                    sys.exit()
                else:
                    self.contadorLocalBool += 1
    
            # Asignación para enteros locales.
            elif tempType == "int":
                dir = TemporalGlobal_Entero
                dir += self.contadorLocalEntero
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalGlobal_Entero or dir >= TemporalGlobal_Flotante:
                    print("no local memory for int temps available")
                    sys.exit()
                else:
                    self.contadorLocalEntero += 1
    
            # Asignación para flotantes locales.
            elif tempType == "float":
                dir = TemporalGlobal_Flotante
                dir += self.contadorLocalFlotante
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalGlobal_Flotante or dir >= TemporalGlobal_Caracter:
                    print("no local memory for float temps available")
                    sys.exit()
                else:
                    self.contadorLocalFlotante += 1
    
            # Asignación para caracteres locales.
            elif tempType == "char":
                dir = TemporalGlobal_Caracter
                dir += self.contadorLocalCaracter
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalGlobal_Caracter or dir >= TemporalGlobal_Cadena:
                    print("no local memory for char temps available")
                    sys.exit()
                else:
                    self.contadorLocalCaracter += 1
                    
            # Asignación para cadenas de texto locales.
            else:
                dir = TemporalGlobal_Cadena
                dir += self.contadorLocalCadena
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalGlobal_Cadena or dir >= Limite_TemporalGlobal:
                    print("no local memory for string temps available")
                    sys.exit()
                else:
                    self.contadorLocalCadena += 1

        # Asignación de memoria para temporales globales.
        else:
            # Asignación para booleanos globales.
            if tempType == "bool":
                dir = TemporalLocal_Bool
                dir += self.contadorGlobalBool
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalLocal_Bool or dir >= TemporalLocal_Entero:
                    print("no global memory for bool temps available")
                    sys.exit()
                else:
                    self.contadorGlobalBool += 1
                    self.listaGlobalBool.append("true")
        
            # Asignación para enteros globales.
            elif tempType == "int":
                dir = TemporalLocal_Entero
                dir += self.contadorGlobalEntero
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalLocal_Entero or dir >= TemporalLocal_Flotante:
                    print("no global memory for int temps available")
                    sys.exit()
                else:
                    self.contadorGlobalEntero += 1
                    self.listaGlobalEntero.append(0)
        
            # Asignación para flotantes globales.
            elif tempType == "float":
                dir = TemporalLocal_Flotante
                dir += self.contadorGlobalFlotante
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalLocal_Flotante or dir >= TemporalLocal_Caracter:
                    print("no global memory for float temps available")
                    sys.exit()
                else:
                    self.contadorGlobalFlotante += 1
                    self.listaGlobalFlotante.append(0.0)
        
            # Asignación para caracteres globales.
            elif tempType == "char":
                dir = TemporalLocal_Caracter
                dir += self.contadorGlobalCaracter
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalLocal_Caracter or dir >= TemporalLocal_Cadena:
                    print("no global memory for char temps available")
                    sys.exit()
                else:
                    self.contadorGlobalCaracter += 1
                    self.listaGlobalCaracter.append(" ")
        
            # Asignación para cadenas de texto globales.
            else:
                dir = TemporalLocal_Cadena
                dir += self.contadorGlobalCadena
                # Verifica espacio disponible y asigna memoria.
                if dir < TemporalLocal_Cadena or dir >= Limite_TemporalLocal:
                    print("no global memory for string temps available")
                    sys.exit()
                else:
                    self.contadorGlobalCadena += 1
                    self.listaGlobalCadena.append(" ")
        return dir
        
    # Función para limpiar y reiniciar la memoria temporal local entre funciones.
    def clear(self):
        # Recopila la memoria requerida actualmente y la devuelve.
        reqMem = {
            "bool": self.contadorLocalBool,
            "int": self.contadorLocalEntero,
            "float": self.contadorLocalFlotante,
            "char": self.contadorLocalCaracter,
            "string": self.contadorLocalCadena,
        }
    
        # Reinicia los contadores de memoria temporal local.
        self.contadorLocalBool = 0
        self.contadorLocalEntero = 0
        self.contadorLocalFlotante = 0
        self.contadorLocalCaracter = 0
        self.contadorLocalCadena = 0
        return reqMem
    
    # Asigna espacio e inicializa temporales locales, guardando el desplazamiento.
    def era(self, reqMem):
        # Configura el mapa de desplazamiento de memoria temporal.
        self.DesplazamientoTemporal = {
            "bool": self.contadorLocalBool,
            "int": self.contadorLocalEntero,
            "float": self.contadorLocalFlotante,
            "char": self.contadorLocalCaracter,
            "string": self.contadorLocalCadena,
        }
    
        # Incrementa los contadores de memoria para cada tipo de temporal.
        bools = reqMem.get("bool")
        self.contadorLocalBool += bools
        ints = reqMem.get("int")
        self.contadorLocalEntero += ints
        floats = reqMem.get("float")
        self.contadorLocalFlotante += floats
        chars = reqMem.get("char")
        self.contadorLocalCaracter += chars
        strings = reqMem.get("string")
        self.contadorLocalCadena += strings
    
        # Verifica la disponibilidad de espacio para cada tipo de variable temporal local y asigna memoria.
        
        # Para variables temporales booleanas locales:
        if self.contadorLocalBool >= TemporalGlobal_Entero:
            print("no local memory for bool temps available")
            sys.exit()
        else:
            # Inicializa la lista de booleanos con valores predeterminados.
            for i in range(bools):
                self.listaLocalBool.append("true")
        
        # Para variables temporales enteras locales:
        if self.contadorLocalEntero >= TemporalGlobal_Flotante:
            print("no local memory for int temps available")
            sys.exit()
        else:
            # Inicializa la lista de enteros con ceros.
            for i in range(ints):
                self.listaLocalEntero.append(0)
        
        # Para variables temporales flotantes locales:
        if self.contadorLocalFlotante >= TemporalGlobal_Caracter:
            print("no local memory for float temps available")
            sys.exit()
        else:
            # Inicializa la lista de flotantes con ceros decimales.
            for i in range(floats):
                self.listaLocalFlotante.append(0.0)
        
        # Para variables temporales de carácter locales:
        if self.contadorLocalCaracter >= TemporalGlobal_Cadena:
            print("no local memory for char temps available")
            sys.exit()
        else:
            # Inicializa la lista de caracteres con espacios en blanco.
            for i in range(chars):
                self.listaLocalCaracter.append(" ")
        
        # Para variables temporales de cadenas de texto locales:
        if self.contadorLocalCadena >= Limite_TemporalGlobal:
            print("no local memory for string temps available")
            sys.exit()
        else:
            # Inicializa la lista de cadenas de texto con cadenas vacías.
            for i in range(strings):
                self.listaLocalCadena.append(" ")
        

    # Libera memoria no requerida y restablece los desplazamientos a su estado anterior.
    def pop(self, reqMem):
        # Reduce el conteo de las variables temporales según los requisitos.
        bools = reqMem.get("bool")
        self.contadorLocalBool -= bools
        ints = reqMem.get("int")
        self.contadorLocalEntero -= ints
        floats = reqMem.get("float")
        self.contadorLocalFlotante -= floats
        chars = reqMem.get("char")
        self.contadorLocalCaracter -= chars
        strings = reqMem.get("string")
        self.contadorLocalCadena -= strings
    
        # Elimina los elementos finales de las listas de temporales para liberar memoria.
        self.listaLocalBool = self.listaLocalBool[:-bools]
        self.listaLocalEntero = self.listaLocalEntero[:-ints]
        self.listaLocalFlotante = self.listaLocalFlotante[:-floats]
        self.listaLocalCaracter = self.listaLocalCaracter[:-chars]
        self.listaLocalCadena = self.listaLocalCadena[:-strings]
    
    # Revierte el desplazamiento de las direcciones de memoria temporales.
    def reajustarDesplazamiento(self, reqMem):
        bools = reqMem.get("bool")
        ints = reqMem.get("int")
        floats = reqMem.get("float")
        chars = reqMem.get("char")
        strings = reqMem.get("string")

        self.DesplazamientoTemporal["bool"] -= bools
        if self.DesplazamientoTemporal["bool"] < 0:
            self.DesplazamientoTemporal["bool"] = 0
        self.DesplazamientoTemporal["int"] -= ints
        if self.DesplazamientoTemporal["int"] < 0:
            self.DesplazamientoTemporal["int"] = 0
        self.DesplazamientoTemporal["float"] -= floats
        if self.DesplazamientoTemporal["float"] < 0:
            self.DesplazamientoTemporal["float"] = 0
        self.DesplazamientoTemporal["char"] -= chars
        if self.DesplazamientoTemporal["char"] < 0:
            self.DesplazamientoTemporal["char"] = 0
        self.DesplazamientoTemporal["string"] -= strings
        if self.DesplazamientoTemporal["string"] < 0:
            self.DesplazamientoTemporal["string"] = 0

    # Devuelve el valor almacenado en la dirección de memoria indicada.
    def obtenerValor(self, dir):
        # Comprueba si la dirección es para temporales locales.
        if dir < Limite_TemporalGlobal:
            # Devuelve el valor correspondiente de la lista de temporales locales, ajustando por el desplazamiento.
            if dir < TemporalGlobal_Bool:
                print("Invalid direction for temp")
                sys.exit()
    
            elif dir < TemporalGlobal_Entero:
                return self.listaLocalBool[dir - TemporalGlobal_Bool + self.DesplazamientoTemporal["bool"]]
    
            elif dir < TemporalGlobal_Flotante:
                return self.listaLocalEntero[dir - TemporalGlobal_Entero + self.DesplazamientoTemporal["int"]]
    
            elif dir < TemporalGlobal_Caracter:
                return self.listaLocalFlotante[dir - TemporalGlobal_Flotante + self.DesplazamientoTemporal["float"]]
    
            elif dir < TemporalGlobal_Cadena:
                return self.listaLocalCaracter[dir - TemporalGlobal_Caracter + self.DesplazamientoTemporal["char"]]
    
            elif dir < Limite_TemporalGlobal:
                return self.listaLocalCadena[dir - TemporalGlobal_Cadena + self.DesplazamientoTemporal["string"]]
    
        # De lo contrario, comprueba si la dirección es para temporales globales.
        else:
            if dir < TemporalLocal_Bool or dir >= Limite_TemporalLocal:
                print("Invalid direction for temp")
                sys.exit()
    
            elif dir < TemporalLocal_Entero:
                return self.listaGlobalBool[dir - TemporalLocal_Bool]
    
            elif dir < TemporalLocal_Flotante:
                return self.listaGlobalEntero[dir - TemporalLocal_Entero]
    
            elif dir < TemporalLocal_Caracter:
                return self.listaGlobalFlotante[dir - TemporalLocal_Flotante]
    
            elif dir < TemporalLocal_Cadena:
                return self.listaGlobalCaracter[dir - TemporalLocal_Caracter]
    
            elif dir < Limite_TemporalLocal:
                return self.listaGlobalCadena[dir - TemporalLocal_Cadena]
    
    # Devuelve el valor del parámetro almacenado en la dirección de memoria para temporales locales.
    def obtenerParametro(self, dir, reqMem):
        # Verifica que la dirección esté en el rango de temporales locales.
        if dir < Limite_TemporalGlobal:
            # Calcula la posición correcta en la lista de temporales locales, ajustando por el desplazamiento y la memoria requerida.
            if dir < TemporalGlobal_Bool:
                print("Invalid direction for temp")
                sys.exit()
    
            elif dir < TemporalGlobal_Entero:
                return self.listaLocalBool[dir - TemporalGlobal_Bool + self.DesplazamientoTemporal["bool"] - reqMem["bool"]]
    
            elif dir < TemporalGlobal_Flotante:
                return self.listaLocalEntero[dir - TemporalGlobal_Entero + self.DesplazamientoTemporal["int"] - reqMem["int"]]
    
            elif dir < TemporalGlobal_Caracter:
                return self.listaLocalFlotante[dir - TemporalGlobal_Flotante + self.DesplazamientoTemporal["float"] - reqMem["float"]]
    
            elif dir < TemporalGlobal_Cadena:
                return self.listaLocalCaracter[dir - TemporalGlobal_Caracter + self.DesplazamientoTemporal["char"] - reqMem["char"]]
    
            elif dir < Limite_TemporalGlobal:
                return self.listaLocalCadena[dir - TemporalGlobal_Cadena + self.DesplazamientoTemporal["string"] - reqMem["string"]]
    

    # Guarda un valor en la dirección de memoria especificada.
    def guardarValor(self, dir, value):
        # Verifica si la dirección está en el rango de temporales locales o globales y asigna el valor correspondiente.
        if dir < Limite_TemporalGlobal:
            # Temporales locales: ajusta la dirección utilizando el mapa de desplazamiento.
            if dir < TemporalGlobal_Bool:
                print("Invalid direction for temp")
                sys.exit()
    
            elif dir < TemporalGlobal_Entero:
                self.listaLocalBool[dir - TemporalGlobal_Bool + self.DesplazamientoTemporal["bool"]] = value
    
            elif dir < TemporalGlobal_Flotante:
                self.listaLocalEntero[dir - TemporalGlobal_Entero + self.DesplazamientoTemporal["int"]] = int(value)
    
            elif dir < TemporalGlobal_Caracter:
                self.listaLocalFlotante[dir - TemporalGlobal_Flotante + self.DesplazamientoTemporal["float"]] = float(value)
    
            elif dir < TemporalGlobal_Cadena:
                self.listaLocalCaracter[dir - TemporalGlobal_Caracter + self.DesplazamientoTemporal["char"]] = value
    
            elif dir < Limite_TemporalGlobal:
                self.listaLocalCadena[dir - TemporalGlobal_Cadena + self.DesplazamientoTemporal["string"]] = value
    
        else:
            # Temporales globales: asigna directamente el valor.
            if dir < TemporalLocal_Bool or dir >= Limite_TemporalLocal:
                print("Invalid direction for temp")
                sys.exit()
    
            elif dir < TemporalLocal_Entero:
                self.listaGlobalBool[dir - TemporalLocal_Bool] = value
    
            elif dir < TemporalLocal_Flotante:
                self.listaGlobalEntero[dir - TemporalLocal_Entero] = value
    
            elif dir < TemporalLocal_Caracter:
                self.listaGlobalFlotante[dir - TemporalLocal_Flotante] = value
    
            elif dir < TemporalLocal_Cadena:
                self.listaGlobalCaracter[dir - TemporalLocal_Caracter] = value
    
            elif dir < Limite_TemporalLocal:
                self.listaGlobalCadena[dir - TemporalLocal_Cadena] = value
    

# Gestiona la memoria asignada a constantes de diferentes tipos.
class MemoriaConst:
    def __init__(self) -> None:
        # Contadores e inicialización de listas para cada tipo de constante.
        self.boolCount = 0
        self.boolList = []
        self.contadorEnteros = 0
        self.listaEnteros = []
        self.contadorFlotantes = 0
        self.listaFlotantes = []
        self.contadorCaracteres = 0
        self.listaCaracteres = []
        self.stringCount = 0
        self.stringList = []

    def asignarMemoria(self, var):
        # Asigna memoria para constantes, basándose en su tipo y valor.
        varType = var.get("type")
        value = var.get("id")

        # Asignación de memoria para constantes booleanas.
        if varType == "bool":
            dir = Constante_Bool
            dir += self.boolCount
            if dir < Constante_Bool or dir >= Constante_Entero:
                print("no memory available")
                sys.exit()
            else:
                self.boolCount += 1
                self.boolList.append(value)

        # Asignación de memoria para constantes enteras.
        elif varType == "int":
            dir = Constante_Entero
            dir += self.contadorEnteros
            if dir < Constante_Entero or dir >= Constante_Flotante:
                print("no memory available")
                sys.exit()
            else:
                self.contadorEnteros += 1
                self.listaEnteros.append(int(value))

        # Asignación de memoria para constantes flotantes.
        elif varType == "float":
            dir = Constante_Flotante
            dir += self.contadorFlotantes
            if dir < Constante_Flotante or dir >= Constante_Caracter:
                print("no memory available")
                sys.exit()
            else:
                self.contadorFlotantes += 1
                self.listaFlotantes.append(float(value))

        # Asignación de memoria para constantes de carácter.
        elif varType == "char":
            dir = Constante_Caracter
            dir += self.contadorCaracteres
            if dir < Constante_Caracter or dir >= Constante_Cadena:
                print("no memory available")
                sys.exit()
            else:
                self.contadorCaracteres += 1
                self.listaCaracteres.append(value)

        # Asignación de memoria para constantes de cadena de texto.
        else:
            dir = Constante_Cadena
            dir += self.stringCount
            if dir < Constante_Cadena or dir >= Limite_Constante:
                print("no memory available")
                sys.exit()
            else:
                self.stringCount += 1
                self.stringList.append(value)

        return dir

    def obtenerValor(self, dir):
        # Recupera el valor almacenado en una dirección de memoria específica.
        if dir < Constante_Bool or dir >= Limite_Constante:
            print("Invalid direction for temp")
            sys.exit()

        # Recupera un valor booleano.
        elif dir < Constante_Entero:
            return self.boolList[dir - Constante_Bool]

        # Recupera un valor entero.
        elif dir < Constante_Flotante:
            return self.listaEnteros[dir - Constante_Entero]

        # Recupera un valor flotante.
        elif dir < Constante_Caracter:
            return self.listaFlotantes[dir - Constante_Flotante]

        # Recupera un carácter.
        elif dir < Constante_Cadena:
            return self.listaCaracteres[dir - Constante_Caracter]

        # Recupera una cadena de texto.
        elif dir < Limite_Constante:
            return self.stringList[dir - Constante_Cadena]


