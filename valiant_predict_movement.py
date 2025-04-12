def predict_enemy_movement(grid, initial_position):
    """
    Predicts the next position of the enemy ship as it moves toward the friendly ship.
    
    Args:
        grid: 8x8 grid representing the space battle
        initial_position: Current position of the enemy ship (i, j) where:
                          i=row index (0-7)
                          j=column index (0-7)
        
    Returns:
        tuple: The next position (i, j) of the enemy ship
    """
    # Localizar nave amiga (#) y obstáculos ($)
    friendly_pos = None
    obstacles = []
    
    # Recorrer la matriz para encontrar posiciones relevantes
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cell = grid[i][j]
            if '#' in cell:
                friendly_pos = (i, j)
            elif '$' in cell:
                obstacles.append((i, j))
    
    # Si no se encuentra la nave amiga, mantener la posición actual
    if not friendly_pos:
        return initial_position
    
    # Depuración: mostrar posiciones encontradas
    print(f"👾 Posición actual de la nave enemiga (x,y): {tranform_indexes_to_coordinates(initial_position[0], initial_position[1])}")
    print(f"🚀 Posición de la nave amiga (x,y): {tranform_indexes_to_coordinates(friendly_pos[0], friendly_pos[1])}")
    print(f"💎 Obstáculos (x, y): {tranform_list_indexes_to_coordinates(obstacles)}")
    
    # Posibles movimientos (solo 4 direcciones ortogonales)
    directions = [
        (-1, 0),  # arriba (fila anterior)
        (0, 1),   # derecha (columna siguiente)
        (1, 0),   # abajo (fila siguiente)
        (0, -1),  # izquierda (columna anterior)
    ]
    
    # Función para calcular la distancia Manhattan
    def manhattan_distance(pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    # Calcular el mejor movimiento
    current_i, current_j = initial_position
    best_move = None
    min_distance = float('inf')
    
    print("Evaluando movimientos posibles:")
    for di, dj in directions:
        new_i, new_j = current_i + di, current_j + dj
        
        # Verificar si la nueva posición está dentro de los límites y no es un obstáculo
        if 0 <= new_i < 8 and 0 <= new_j < 8 and (new_i, new_j) not in obstacles:
            distance = manhattan_distance((new_i, new_j), friendly_pos)
            print(f"➡️  Movimiento ({di}, {dj}) a {tranform_indexes_to_coordinates(new_i, new_j)}: distancia = {distance}")
            
            if distance < min_distance:
                min_distance = distance
                best_move = (new_i, new_j)
    
    # Si encontramos un movimiento válido, retornarlo
    if best_move:
        print(f"⏩️ Mejor movimiento (x,y): {tranform_indexes_to_coordinates(best_move[0], best_move[1])}")
        return best_move
    
    # Si no hay movimientos válidos, permanecer en el mismo lugar
    return initial_position

def tranform_indexes_to_coordinates(i, j):
    """
    Transforma un índice de matriz [i][j] a coordenadas cartesianas (x, y),
    basadas en la convención del gráfico.
    """
    x = j
    y = 8 - 1 - i
    return x, y

def tranform_list_indexes_to_coordinates(indices):
    coordinates = []

    if len(indices) < 1:
        return coordinates

    for index in indices:
        coordinates.append(tranform_indexes_to_coordinates(index[0], index[1]))

    return coordinates
# Make the function exportable
__all__ = ['predict_enemy_movement']

# Example usage when run directly
if __name__ == "__main__":
    # Grid from the test case
    example_grid = [
        ['a08', 'b08', 'c08', 'd08', 'e08', 'f#8', 'g08', 'h08'],  # i=0
        ['a07', 'b07', 'c07', 'd07', 'e07', 'f07', 'g07', 'h07'],  # i=1
        ['a06', 'b06', 'c06', 'd06', 'e$6', 'f06', 'g06', 'h06'],  # i=2
        ['a05', 'b05', 'c05', 'd05', 'e$5', 'f$5', 'g^5', 'h05'],  # i=3 (nave enemiga en j=6)
        ['a04', 'b04', 'c04', 'd04', 'e04', 'f04', 'g04', 'h04'],  # i=4
        ['a03', 'b03', 'c03', 'd03', 'e03', 'f03', 'g03', 'h$3'],  # i=5
        ['a02', 'b02', 'c02', 'd02', 'e$2', 'f02', 'g02', 'h02'],  # i=6
        ['a01', 'b01', 'c01', 'd01', 'e01', 'f01', 'g01', 'h01']   # i=7
    ]
    
    # Nave enemiga (^) está en g^5, que en índices de matriz es (3, 6) - fila 3, columna 6
    enemy_position = (3, 6)
    print("\nTest 1 - Nave enemiga en posición (3, 6):")
    next_move = predict_enemy_movement(example_grid, enemy_position)
    print(f"Próximo movimiento: {next_move}")
    
    # Prueba con otra posición
    print("\nTest 2 - Nave enemiga en posición (4, 6):")
    enemy_position_2 = (4, 6)
    next_move_2 = predict_enemy_movement(example_grid, enemy_position_2)
    print(f"Próximo movimiento: {next_move_2}")

