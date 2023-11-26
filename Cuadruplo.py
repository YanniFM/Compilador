class Cuadruplo:
    
    def __init__(self, operador, operando1, operando2, resultado) -> None:
        # Guarda el operador de la instrucción (p.ej., +, -, *, /).
        self.operador = operador
        # Almacena las direcciones de memoria de los operandos y el resultado en lugar de los valores directos.
        # Esto permite una mayor flexibilidad y abstracción, especialmente en entornos de compilación.
        self.operando1 = operando1.get("dir")
        self.operando2 = operando2.get("dir")
        self.resultado = resultado
        # Versión anterior almacenaba directamente los operandos y el resultado.

    def fill(self, resultado) -> None:
        # Método para actualizar el lugar donde se almacena el resultado.
        self.resultado = resultado

    def __str__(self):
        # Representación en cadena del cuádruplo ajustada para reflejar la nueva estructura que almacena direcciones.
        return f"[{self.operador}, {self.operando1}, {self.operando2}, {self.resultado}]"
        # En la versión anterior, la representación en cadena incluía los valores directos de los operandos.
        # return str(self.operador) + " " + str(self.operando1) + " " + str(self.operando2) + " " + str(self.resultado)
