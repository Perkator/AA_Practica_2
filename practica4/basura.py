# Este es el famoso archivo "basura" en el cual se encuentran los métodos que 
# forman parte del juego solamente, no tiene mucho secreto tampoco
import random as ran

# Genera una tupla aleatoria de la dimensión del tablero de juego
def generar_casilla():
    return (ran.randint(0,2), ran.randint(0,2))

# Método que modifica la casilla pasada al tablero pasado con el caracter "turno"
def modificar_tablero(tablero, casilla, turno):
    tablero[casilla[0]][casilla[1]] = turno

# Método que imprime el tablero por pantalla de una manera mas o menos más estética
def pintar_tablero(tablero):
    for fila in tablero:
        fila_str = " | ".join(str(casilla) if casilla is not None else " " for casilla in fila)
        print(f" {fila_str}")

# Método que devuelve un booleano dependiendo de si la casilla pasada como parámetro es válida
# en el teclado pasado como parámetro. Es válida en el caso de que esa casilla no este escrita
def casilla_valida(tablero, casilla):
    if tablero[casilla[0]][casilla[1]] is not None:
        return False
    else: return True

# Método que devuelve un booleano que depende si el teclado pasado como parámetro es ganador
def victoria(tablero):
    # Verificar filas y columnas
    for i in range(3):
        # Verificar filas
        if tablero[i][0] == tablero[i][1] == tablero[i][2] and tablero[i][0] is not None:
            return True
        
        # Verificar columnas
        if tablero[0][i] == tablero[1][i] == tablero[2][i] and tablero[0][i] is not None:
            return True

    # Verificar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] and tablero[0][0] is not None:
        return True

    if tablero[0][2] == tablero[1][1] == tablero[2][0] and tablero[0][2] is not None:
        return True

    # No hay ganador
    return False

# Método que devuelve un booleano dependiendo de que el tablero este completo
def tablas(tablero):
    for linea in tablero:
        for i in linea:
            if i is None:
                return False
    return True