-------------------------------------------------------------------------------------------------------------------------------------
Prerrequisitos
Lo que necesitas para instalar el software y cómo instalarlo, por ejemplo:

Python 3.8 o superior
PLY (Python Lex-Yacc)

-------------------------------------------------------------------------------------------------------------------------------------
Instalación
Una serie de ejemplos paso a paso que te dicen cómo hacer un entorno de desarrollo en funcionamiento.

pip install ply

-------------------------------------------------------------------------------------------------------------------------------------
Estructura de Archivos

-Lexer.py: Contiene el analizador léxico que tokeniza el código fuente.
-Parser.py: Define el analizador sintáctico y las reglas gramaticales / Punto de entrada del programa. Gestiona la lectura de archivos y la ejecución del análisis y la máquina virtual..
-CuboSemantico.py: Define las reglas de tipo para operaciones.
-Cuadruplo.py: Estructura y manejo de los cuádruplos.
-MaquinaVirtual.py: Simula la ejecución del código a partir de cuádruplos.
-GestionMemoria.py: Contiene  la gestion de Memoria Global, Local, Temporal y Contante importando las variables con memoria
-DistribucionMemoria.py: Se Realiza La distribución de memoria aquí se realiza en bloques de 2000 unidades para cada tipo.
-------------------------------------------------------------------------------------------------------------------------------------
Uso
Cómo ejecutar el conjunto de pruebas automatizadas para este sistema.

python Parser.py <ArchivoPrueba.txt>

-------------------------------------------------------------------------------------------------------------------------------------

Construido con:

Python - El lenguaje de programación usado
PLY - Herramienta de análisis léxico y sintáctico
NumPy - Biblioteca esencial para operaciones matriciales y numéricas en Python.
Matplotlib - Herramienta de visualización de datos para Python, permite crear gráficos y representaciones visuales.
(Estas librerías son fundamentales y se pueden instalar fácilmente utilizando = pip install ply,Numpy, Matplotlib)
-------------------------------------------------------------------------------------------------------------------------------------

Declaración de Variables Globales

Las variables globales se definen con la palabra clave "vars" y pueden ser de tipo int, float o char.

program variablesGlobales;
vars
int i, j;
float x, y;
char a, b;

main(){
    # Código del programa
}

-------------------------------------------------------------------------------------------------------------------------------------

Declaración de Variables Locales

Las variables locales, específicas de una función, se declaran dentro de la función y solo están activas en ella.

program variablesLocales;
vars
int a, b;

function void imprimir()
vars 
int i, j;
{
    write(i, " ", a);
    write(j, " ", b);
}
    
main(){
    imprimir();
}

-------------------------------------------------------------------------------------------------------------------------------------

Declaración y Acceso a Arreglos

MyRLanguage permite el uso de arreglos, tanto globales como locales.

program arreglos;
vars
int i, j[5];
float x[3], y;
char a, b[100];

main(){
    x[2] = 5.8;
    write(x[2]);
}

-------------------------------------------------------------------------------------------------------------------------------------

Entrada y Salida de Datos

Para recibir datos del usuario, utiliza "read"; para imprimir en consola, utiliza "write".

program frutas;
vars
int cantidad;
main(){
    write("¿Cuántas manzanas deseas?");
    read(cantidad);
    write("Entregar ", cantidad, " manzana(s)");
}

-------------------------------------------------------------------------------------------------------------------------------------

Operadores Lógicos, Aritméticos y Booleanos

MyRLanguage soporta una variedad de operadores para realizar operaciones lógicas, aritméticas y booleanas.

program operadores;
main(){
    write(4 * 5 + 6);
    write(3 < 1 & 4 > 2);
}

-------------------------------------------------------------------------------------------------------------------------------------

Asignación de Valores

La asignación se realiza mediante el operador "=".

program asignacion;
vars
int cantidad;

function int alCuadrado(int i){
    i = i * i;
    return(i);
}
main(){
    cantidad = 4 * 5 + 6;
    write(cantidad);
    cantidad = alCuadrado(cantidad);
    write(cantidad);
}

-------------------------------------------------------------------------------------------------------------------------------------

Ciclos

MyRLanguage soporta ciclos "while" y "for" para facilitar la repetición de bloques de código.

program ciclos;
vars
int i;

main(){
    while (i < 5) do {
        write(i);
        i = i + 1;
    }
    for i = 0 to 5 do {
        write(i);
    }
}

-------------------------------------------------------------------------------------------------------------------------------------

Funciones, Retornos y Llamadas

Las funciones en MyRLanguage permiten modularizar el código y mejorar su legibilidad.

program funciones;
vars
int array[5], i;
float promedio;

function void imprimirArreglo(int a[5]){
    for i = 0 to 4 do {
        write("índice ", i , " = ", a[i]);
    }
}

function float calcularPromedio(int a[5])
vars float total, aux;
{
    for i = 0 to 4 do {
        aux = float(a[i]);
        total = total + aux;
    }
    total = total / 5;
    return(total);
}
    
main(){
    for i = 0 to 4 do {
        read(array[i]);
    }

    imprimirArreglo(array);

    promedio = calcularPromedio(array);
    write("El promedio es ", promedio);
}


-------------------------------------------------------------------------------------------------------------------------------------

Funciones Especiales

MyRLanguage incluye funciones especiales predefinidas para realizar tareas específicas.

int(x): Convierte un valor float a int truncando los decimales.
float(x): Convierte un valor int a float.
pow(x, y): Calcula x elevado a la potencia y.
rand(): Genera un valor float aleatorio entre 0 y 1.
med(array): Calcula la media de los valores en un arreglo.
moda(array): Calcula la moda de los valores en un arreglo.
var(array): Calcula la varianza de los valores en un arreglo.
reg(array): Muestra un gráfico de regresión lineal de los valores en un arreglo.
plot(array): Muestra un gráfico de línea de los valores en un arreglo.
Ejecución del Código


-------------------------------------------------------------------------------------------------------------------------------------

