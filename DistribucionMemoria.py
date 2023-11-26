# La distribución de memoria aquí se realiza en bloques de 2000 unidades para cada tipo
# de variable y constante. Este esquema facilita la identificación y el aislamiento
# de diferentes tipos de datos (globales, locales, constantes, temporales) para evitar
# colisiones y mejorar la eficiencia en la asignación y el acceso a la memoria. Al
# comenzar en 50000 y finalizar cerca de 90000, se proporciona suficiente espacio para
# cada tipo, permitiendo una expansión o modificación futura sin reestructurar
# completamente el esquema de memoria, lo cual es crucial para la escalabilidad y
# mantenimiento del proyecto.

# Variables Globales:
Global_Entero = 50000  # Dirección de inicio para variables enteras globales
Global_Flotante = 52000  # Dirección de inicio para variables flotantes globales
Global_Caracter = 54000  # Dirección de inicio para variables de carácter globales
Limite_Global = 56000  # Límite superior para el espacio de memoria de variables globales

# Variables Locales:
Local_Entero = 58000  # Dirección de inicio para variables enteras locales
Local_Flotante = 60000  # Dirección de inicio para variables flotantes locales
Local_Caracter = 62000  # Dirección de inicio para variables de carácter locales
Limite_Local = 64000  # Límite superior para el espacio de memoria de variables locales

# Constantes:
Constante_Bool = 66000  # Dirección de inicio para constantes booleanas
Constante_Entero = 68000  # Dirección de inicio para constantes enteras
Constante_Flotante = 70000  # Dirección de inicio para constantes flotantes
Constante_Caracter = 72000  # Dirección de inicio para constantes de carácter
Constante_Cadena = 74000  # Dirección de inicio para constantes de cadena de texto
Limite_Constante = 76000  # Límite superior para el espacio de memoria de constantes

# Temporales Globales:
TemporalGlobal_Bool = 78000  # Dirección de inicio para temporales booleanos globales
TemporalGlobal_Entero = 80000  # Dirección de inicio para temporales enteros globales
TemporalGlobal_Flotante = 82000  # Dirección de inicio para temporales flotantes globales
TemporalGlobal_Caracter = 84000  # Dirección de inicio para temporales de carácter globales
TemporalGlobal_Cadena = 86000  # Dirección de inicio para temporales de cadena de texto globales
Limite_TemporalGlobal = 88000  # Límite superior para el espacio de memoria de temporales globales

# Temporales Locales:
TemporalLocal_Bool = 90000  # Dirección de inicio para temporales booleanos locales
TemporalLocal_Entero = 92000  # Dirección de inicio para temporales enteros locales
TemporalLocal_Flotante = 94000  # Dirección de inicio para temporales flotantes locales
TemporalLocal_Caracter = 96000  # Dirección de inicio para temporales de carácter locales
TemporalLocal_Cadena = 98000  # Dirección de inicio para temporales de cadena de texto locales
Limite_TemporalLocal = 100000  # Límite superior para el espacio de memoria de temporales locales