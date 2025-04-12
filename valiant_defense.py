import time
import requests
import sys
from valiant_predict_movement import predict_enemy_movement, tranform_indexes_to_coordinates


BASE_URL = "http://localhost:8000"

ACTION_READ_RADAR = "leer"
ACTION_ATTACK = "atacar"
TURN = 1


def start_battle():
    """start"""
    return requests.post(f"{BASE_URL}/v1/s1/e5/actions/start")


def perform_turn(json):
    """perform_turn"""
    return requests.post(f"{BASE_URL}/v1/s1/e5/actions/perform-turn", json=json)


def perform_turn_lecture():
    """perform_turn_lecture"""
    json={
        "action": ACTION_READ_RADAR,
        "attack_position": None
    }
    return perform_turn(json)


def perform_turn_attack(x, y):
    """perform_turn_attack"""
    json={
        "action": ACTION_ATTACK,
        "attack_position": {
            "x": str(x),
            "y": int(y)
        }
    }
    return perform_turn(json)


def format_response_string(response):
    """format_response_string"""
    if((response[0] == "\"" and response[-1] == "\"") or (response[0] == "'" and response[-1] == "'")):
        response = response[1:-2]

    return response


def parse_radar_data(radar_string):
    """parse_radar_data"""
    grid = []
    enemy_position = None
    valiant_position = None

    radar_string = format_response_string(radar_string)

    rows = radar_string.split("|")[::-1]

    for i, row in enumerate(rows):
        grid.append([])
        for j in range(8):
            cell = row[j * 3 : j * 3 + 3]  # Extraemos celdas en formato 'a01', 'b02', etc.
            grid[i].append(cell)
            if '^' in cell:  # Detectamos la nave enemiga
                enemy_position = (i, j)
            if '#' in cell:  # Detectamos la nave enemiga
                valiant_position = (i, j)

    return grid, enemy_position, valiant_position


def lecture():
    global TURN
    lecture_response = perform_turn_lecture()
    lecture_string = lecture_response.text
    grid, enemy_pos, valiant_position = parse_radar_data(lecture_string)
    predicted_next_position = predict_enemy_movement(grid, enemy_pos)
    print_board(grid)
    print("Lecture response: ", lecture_string)
    print(f"👾 Nave enemiga detectada en: {tranform_indexes_to_coordinates(enemy_pos[0], enemy_pos[1])}")
    print(f"🔥 {TURN} Coordenadas de ataque ", tranform_indexes_to_coordinates(predicted_next_position[0], predicted_next_position[1]))
    TURN += 1
    return predicted_next_position


def attack(predicted_next_position):
    i, j = predicted_next_position
    attack_x, attack_y = tranform_indexes_to_coordinates(i, j)
    print(f"🔥 Coordenadas ({attack_x}, {attack_y}); Indices: ({i}, {j})")
    attack_response = perform_turn_attack(attack_x, attack_y)

    if attack_response.status_code == 200:
        print("¡Ataque exitoso! La nave enemiga ha sido destruida. ", attack_response.text)
    else:
        print("El ataque falló. ¡La Hope está en peligro! ", attack_response.text)


def execute_command(predicted_next_position):
    while True:
        comando = input("🔧 Ingresa un comando (leer, atacar, end): ").strip().lower()

        if comando == ACTION_READ_RADAR:
            predicted_next_position = lecture()
        elif comando == ACTION_ATTACK:
            attack(predicted_next_position)
        elif comando == "end":
            print("👋 Finalizando el programa...")
            break
        else:
            print(f"❌ Comando no reconocido: '{comando}'")

        print("🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩")
        print("")
        print("")


def main():
    """Controla la lógica del juego."""
    start_time = time.time()

    # 1. Leer radar
    response = start_battle()
    radar_string = response.text
    grid, enemy_pos, valiant_position = parse_radar_data(radar_string)

    print("radar: ", radar_string)
    print_board(grid)

    if enemy_pos is None:
        print("No se encontró la nave enemiga.", radar_string)
        return

    print(f"🚀 Posicion de Valiant: {tranform_indexes_to_coordinates(valiant_position[0], valiant_position[1])}")
    print(f"👾 Nave enemiga detectada en: {tranform_indexes_to_coordinates(enemy_pos[0], enemy_pos[1])}")

    # Predecir movimiento
    predicted_next_position = predict_enemy_movement(grid, enemy_pos)
    print("🔥 Coordenadas de ataque ", tranform_indexes_to_coordinates(predicted_next_position[0], predicted_next_position[1]))

    print("🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩")
    print("")
    print("")

    execute_command(predicted_next_position)

    print("Tiempo total transcurrido:", time.time() - start_time, "segundos")


def print_board(matriz):
    for i, fila in enumerate(matriz):
        linea = ""
        for celda in fila:
            contenido = celda[1]
            linea += contenido + " "
        print(linea.strip() + f"    {7 - i}")

    print("")
    print("")
    print("0 1 2 3 4 5 6 7")
    print("")
    print("")


if __name__ == "__main__":
    main()
