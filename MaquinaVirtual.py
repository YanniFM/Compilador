import sys # Importa el módulo sys, que proporciona acceso a algunas variables y funciones que interactúan con el intérprete de Python.
import matplotlib.pyplot as plt # Importa el módulo de Matplotlib para la generación de Gráfico de Líneass y visualizaciones.
import numpy as np # Importa el módulo NumPy, una biblioteca fundamental para la computación científica en Python.

from random import random # Importa la función random del módulo random, que se usa para generar números aleatorios.
from statistics import mean, mode, variance # Importa las funciones mean, mode y variance del módulo statistics, utilizadas para cálculos estadísticos como promedio, moda y varianza.
from DistribucionMemoria import Limite_Constante, Limite_TemporalLocal, Limite_Global, Limite_TemporalGlobal, Limite_Local

# Lista de funciones especiales integradas. Incluye funciones para conversión de tipos (int, float),
# operaciones matemáticas (pow, rand), estadísticas (med, moda, var) y visualización de datos (reg, plot).
SPECFUNC = ["int", "float", "pow", "rand", "med", "moda", "var", "reg", "plot"]

# Clase MaquinaVirtual: Gestiona la ejecución de cuádruplos generados por el compilador. 
# Responsable de interpretar y ejecutar los cuádruplos, manejar la memoria durante la ejecución
# y proporcionar funcionalidades para operaciones especiales. Incluye métodos para ejecutar  
# instrucciones, manejar saltos condicionales e incondicionales, realizar operaciones aritméticas 
# y lógicas, así como gestionar la entrada/salida. Además, implementa funciones especiales
# como conversiones de tipo y operaciones estadísticas y de visualización.
class MaquinaVirtual:
    # Inicializar la máquina virtual
    def __init__(self, programID, directorioFunciones, MemoriaG, MemoriaL, MemoriaC, MemoriaT) -> None:
        # Inicialización de pilas y memoria para la máquina virtual
        self.pilaSalto = []  # Pila para saltos
        self.funcStack = []  # Pila para llamadas a funciones
        self.params = []     # Lista de parámetros

        # Almacenamiento de información esencial para la ejecución:
        self.programID = programID  # ID del programa actual para seguimiento y referencia.
        self.directorioFunciones = directorioFunciones  # Estructura que almacena información sobre las funciones del programa, como direcciones y variables.
        self.MemoriaG = MemoriaG  # Referencia a la memoria global, para acceso y manipulación de variables globales.
        self.MemoriaL = MemoriaL  # Referencia a la memoria local, usada para variables locales durante la ejecución de funciones.
        self.MemoriaC = MemoriaC  # Referencia a la memoria de constantes, para el manejo de valores constantes del programa.
        self.MemoriaT = MemoriaT  # Referencia a la memoria temporal, para almacenar y manejar valores temporales y resultados intermedios.


    # Ejecutar cuádruplos desde una lista de cuádruplos
    def run(self, CuadruploList, show):
        self.curr = 0
        while self.curr < len(CuadruploList) and CuadruploList[self.curr].operador != "Aceptado":
            Cuadruplo = CuadruploList[self.curr]

            if show:  # Mostrar cuádruplo si es necesario
                print(Cuadruplo, end=" ")
            if Cuadruplo.operando2 == None:
                # Ejecutar operaciones más complejas

                if Cuadruplo.operador == "=":  # Asignación
                    op1 = self.obtenerValor(Cuadruplo.operando1)
                    self.guardarValor(Cuadruplo.resultado, op1)

                elif Cuadruplo.operador == "GOTO":  # Salto incondicional
                    self.curr = Cuadruplo.resultado - 1

                elif Cuadruplo.operador == "GOTOF":  # Salto condicional
                    op1 = self.obtenerValor(Cuadruplo.operando1)
                    if not op1:
                        self.curr = Cuadruplo.resultado - 1

                elif Cuadruplo.operador == "PRINT":  # Imprimir valor
                    print(self.obtenerValor(Cuadruplo.resultado), end="")

                elif Cuadruplo.operador == "READ":  # Leer valor
                    value = input()
                    dir = self.getPointer(Cuadruplo.resultado)

                    if dir < Limite_Global:
                        self.MemoriaG.read(dir, value)

                    elif dir < Limite_Local:
                        self.MemoriaL.read(dir, value)

                elif Cuadruplo.operador == "VER":  # Verificar rango de un arreglo
                    min = 0
                    max = Cuadruplo.resultado
                    op1 = self.obtenerValor(Cuadruplo.operando1)
                    if op1 < min or op1 >= max:
                        print(f"Error: Índice de arreglo {op1} fuera de rango")
                        sys.exit()

                # Preparar espacio para la ejecución de una función
                elif Cuadruplo.operador == "ERA":
                    if Cuadruplo.resultado not in SPECFUNC:
                        reqresultados = self.directorioFunciones[Cuadruplo.resultado].get("reqresultados")
                        reqVars = self.directorioFunciones[Cuadruplo.resultado].get("reqVars")

                        self.MemoriaL.era(reqVars)
                        self.MemoriaT.era(reqresultados)

                        self.funcStack.append(Cuadruplo.resultado)
                        keys = list(self.directorioFunciones[self.funcStack[-1]]["vars"])
                        self.params = keys[: self.directorioFunciones[self.funcStack[-1]]["params"]]

                    else:
                        self.params = []
                        self.funcStack.append(Cuadruplo.resultado)

                # Encontrar datos del parámetro, guardar en la dirección apropiada
                elif Cuadruplo.operador == "PARAM":
                    if self.funcStack[-1] not in SPECFUNC:
                        key = self.params[Cuadruplo.resultado]
                        arrSize = self.directorioFunciones[self.funcStack[-1]]["vars"][key].get(
                            "arrSize"
                        )
                        dir = self.directorioFunciones[self.funcStack[-1]]["vars"][key].get("dir")
                        if arrSize > 1:
                            for i in range(arrSize):
                                value = self.obtenerParametro(Cuadruplo.operando1 + i)
                                self.guardarValor(dir + i, value)
                        else:
                            value = self.obtenerParametro(Cuadruplo.operando1)
                            self.guardarValor(dir, value)
                    else:
                        self.params.insert(0, Cuadruplo.operando1)

                # Salir de la función, ajustar desplazamientos
                elif Cuadruplo.operador == "RETURN":
                    dir = self.directorioFunciones[self.programID]["vars"][self.funcStack[-1]].get(
                        "dir"
                    )
                    value = self.obtenerValor(Cuadruplo.resultado)
                    self.guardarValor(dir, value)

                    func = self.funcStack.pop()

                    reqresultados = self.directorioFunciones[func]["reqresultados"]
                    reqVars = self.directorioFunciones[func]["reqVars"]

                    self.MemoriaL.pop(reqVars)
                    self.MemoriaT.pop(reqresultados)
                    self.curr = self.pilaSalto.pop()
                    if len(self.funcStack) > 0:
                        reqresultados = self.directorioFunciones[self.funcStack[-1]]["reqresultados"]
                        reqVars = self.directorioFunciones[self.funcStack[-1]]["reqVars"]
                        self.MemoriaT.reajustarDesplazamiento(reqresultados)

                    self.params = []

                elif Cuadruplo.operador == "ENDFUNC":
                    self.exitFunc()

                # Guardar cuádruplo para regresar, ir a la función
                elif Cuadruplo.operador == "GOSUB":
                    if Cuadruplo.resultado != "spec":
                        self.pilaSalto.append(self.curr)
                        self.curr = Cuadruplo.resultado - 1
                    else:
                        dir = CuadruploList[self.curr + 1].operando1
                        self.doSpec(dir)

            else:
                # Ejecutar operación simple
                op1 = self.obtenerValor(Cuadruplo.operando1)
                op2 = self.obtenerValor(Cuadruplo.operando2)
                res = self.do(Cuadruplo.operador, op1, op2)
                self.guardarValor(Cuadruplo.resultado, res)
            if show:
                print()
            self.curr += 1

    # Devuelve el valor de la dirección de memoria apropiada
    def obtenerValor(self, dir):
        dir = self.getPointer(dir)  # Obtiene la dirección real en caso de ser un puntero

        # Determina de qué bloque de memoria recuperar el valor
        if dir < Limite_Global:
            value = self.MemoriaG.obtenerValor(dir)  # Memoria global
        elif dir < Limite_Local:
            value = self.MemoriaL.obtenerValor(dir)  # Memoria local
        elif dir < Limite_Constante:
            value = self.MemoriaC.obtenerValor(dir)  # Memoria de constantes
            # Convertir cadenas "true" y "false" a valores booleanos
            if value == "true":
                value = True
            elif value == "false":
                value = False
        elif dir < Limite_TemporalLocal:
            value = self.MemoriaT.obtenerValor(dir)  # Memoria resultado
            # Igual que arriba, convertir cadenas a booleanos
            if value == "true":
                value = True
            elif value == "false":
                value = False
        else:
            print(f"{dir} es una dirección de memoria inválida")
            sys.exit()
        return value

    # Devuelve el valor del parámetro de la dirección apropiada
    def obtenerParametro(self, dir):
        dir = self.getPointer(dir)  # Resuelve si es un puntero

        # Determina de qué bloque de memoria recuperar el valor del parámetro
        if dir < Limite_Global:
            value = self.MemoriaG.obtenerValor(dir)
        elif dir < Limite_Local:
            reqVars = self.directorioFunciones[self.funcStack[-1]]["reqVars"]
            value = self.MemoriaL.obtenerParametro(dir, reqVars)
        elif dir < Limite_Constante:
            value = self.MemoriaC.obtenerValor(dir)
            # Convertir "true" y "false" a booleanos
            if value == "true":
                value = True
            elif value == "false":
                value = False
        elif dir < Limite_TemporalGlobal:
            reqresultados = self.directorioFunciones[self.funcStack[-1]]["reqresultados"]
            value = self.MemoriaT.obtenerParametro(dir, reqresultados)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        elif dir < Limite_TemporalLocal:
            value = self.MemoriaT.obtenerValor(dir)
            if value == "true":
                value = True
            elif value == "false":
                value = False
        else:
            print(f"{dir} es una dirección de memoria inválida")
            sys.exit()

        return value

    # Guarda un valor en la dirección apropiada
    def guardarValor(self, dir, value):
        dir = self.getPointer(dir)  # Resuelve si es un puntero
        # Guarda el valor en la memoria correspondiente
        if dir < Limite_Global:
            self.MemoriaG.guardarValor(dir, value)
        elif dir < Limite_Local:
            self.MemoriaL.guardarValor(dir, value)
        elif dir < Limite_Constante:
            self.MemoriaC.guardarValor(dir, value)
        elif dir < Limite_TemporalLocal:
            self.MemoriaT.guardarValor(dir, value)
        else:
            print(f"{dir} es una dirección de memoria inválida")
            sys.exit()

    # Devuelve la dirección real en caso de que sea un puntero
    def getPointer(self, dir):
        if type(dir) == str:  # Si es un puntero, obtiene la dirección real
            dir = int(dir[1:])
            dir = self.obtenerValor(dir)

        dir = int(dir)
        return dir

    # Limpia la memoria que ya no se necesita y ajusta los desplazamientos
    def exitFunc(self):
        func = self.funcStack.pop()

        reqresultados = self.directorioFunciones[func]["reqresultados"]
        reqVars = self.directorioFunciones[func]["reqVars"]

        self.MemoriaL.pop(reqVars)
        self.MemoriaT.pop(reqresultados)
        self.curr = self.pilaSalto.pop()
        if len(self.funcStack) > 0:
            reqresultados = self.directorioFunciones[self.funcStack[-1]]["reqresultados"]
            reqVars = self.directorioFunciones[self.funcStack[-1]]["reqVars"]
            self.MemoriaL.reajustarDesplazamiento(reqVars)
            self.MemoriaT.reajustarDesplazamiento(reqresultados)

        self.params = []

    # Ejecuta expresiones simples y devuelve el resultado
    def do(self, operador, op1, op2):
        # Realiza operaciones aritméticas y lógicas básicas
        if operador == "+":
            res = op1 + op2
        elif operador == "-":
            res = op1 - op2
        elif operador == "*":
            res = op1 * op2
        elif operador == "/":
            if op2 == 0:
                print("Error: no se puede dividir por 0")
                sys.exit()
            else:
                res = op1 / op2
        elif operador == "%":
            res = op1 % op2
        elif operador == ">":
            res = op1 > op2
        elif operador == "<":
            res = op1 < op2
        elif operador == ">=":
            res = op1 >= op2
        elif operador == "<=":
            res = op1 <= op2
        elif operador == "<>":
            res = op1 != op2
        elif operador == "==":
            res = op1 == op2
        elif operador == "&":
            res = op1 and op2
        elif operador == "|":
            res = op1 or op2
        else:
            print(f"Error: operador no reconocido {operador}")
            sys.exit()

        return res

    # Ejecutar funciones especiales
    def doSpec(self, dir):
        func = self.funcStack.pop()  # Obtener la función especial a ejecutar

        # Convertir a entero y guardar el resultado
        if func == "int":
            x = int(self.obtenerValor(self.params.pop()))  # Convertir el valor a entero
            self.guardarValor(dir, x)

        # Convertir a flotante y guardar el resultado
        elif func == "float":
            x = float(self.obtenerValor(self.params.pop()))  # Convertir el valor a flotante
            self.guardarValor(dir, x)

        # Calcular la potencia y guardar el resultado
        elif func == "pow":
            x = float(self.obtenerValor(self.params.pop()))  # Base
            y = float(self.obtenerValor(self.params.pop()))  # Exponente
            self.guardarValor(dir, pow(x, y))

        # Generar un número aleatorio y guardarlo
        elif func == "rand":
            self.guardarValor(dir, random())  # Guarda un número aleatorio

        # Para otras funciones que requieren cargar un arreglo
        else:
            arr = self.loadArr()  # Carga el arreglo necesario para la función

            # Calcular la media y guardar el resultado
            if func == "med":
                self.guardarValor(dir, mean(arr))

            # Encontrar la moda y guardar el resultado
            elif func == "moda":
                self.guardarValor(dir, mode(arr))

            # Calcular la varianza y guardar el resultado
            elif func == "var":
                self.guardarValor(dir, variance(arr))

            # Realizar una regresión lineal y mostrar el Gráfico de Líneas
            elif func == "reg":
                x = [i for i in range(len(arr))]  # Crear una lista de índices
                coef = np.polyfit(x, arr, 1)  # Ajustar la regresión lineal
                poly1d_fn = np.poly1d(coef)  # Crear función polinómica

                fig, ux = plt.subplots()  # Crear una figura y un eje

                ux.plot(x, arr, ".")  # Puntos de datos
                ux.plot(poly1d_fn(x), "--k")  # Línea de regresión

                ux.set_title("Regresión Lineal")
                ux.set_xlabel("Eje x")
                ux.set_ylabel("Eje y")

                plt.show()  # Mostrar el Gráfico de Líneas

            # Crear y mostrar un Gráfico de Líneas de los datos
            elif func == "plot":
                x = [i for i in range(len(arr))]  # Crear una lista de índices

                fig, ax = plt.subplots()  # Crear una figura y un eje
                ax.plot(x, arr, ".-")  # Crear el Gráfico de Líneas de línea

                ax.set_title("Gráfico de Líneas")
                ax.set_xlabel("Eje x")
                ax.set_ylabel("Eje y")

                plt.show()  # Mostrar la Gráfico de Líneas

    # Cargar un arreglo para la ejecución de una función especial
    def loadArr(self):
        dir = self.params.pop()  # Obtener la dirección del arreglo
        array = []

        # Determinar el contexto actual para cargar el arreglo
        if len(self.funcStack) == 0:
            curr = self.programID
        else:
            curr = self.funcStack[-1]

        keys = list(self.directorioFunciones[curr]["vars"])  # Obtener las claves de las variables

        # Encontrar el tamaño del arreglo y cargar sus valores
        for key in keys:
            if self.directorioFunciones[curr]["vars"][key].get("dir") == dir:
                arrSize = self.directorioFunciones[curr]["vars"][key].get("arrSize")
                break

        for i in range(arrSize):
            array.append(self.obtenerValor(dir + i))  # Cargar cada elemento del arreglo

        return array  # Devolver el arreglo cargado
