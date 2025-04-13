import time
import requests
from valiant_predict_movement import predict_enemy_movement, tranform_indexes_to_coordinates


BASE_URL = "https://makers-challenge.altscore.ai"
# BASE_URL = "http://localhost:8000"

HEADERS = {
    "API-KEY": "12f1eb55057742b080debc75751e8a47",  # 🔹 Reemplaza con tu API Key real
    "Content-Type": "application/json"
}

ACTION_READ_RADAR = "radar"
ACTION_ATTACK = "attack"
TURN = 1

def get_lecture_response(lecture_response):
    """get_lecture_response"""
    print("🤖 lecture response: ", lecture_response.text)
    lecture = lecture_response.json()
    return lecture["action_result"]


def get_start_response(response):
    """get_start_response"""
    print("🤖 start response: ", response.text)
    return response.text

def start_battle():
    """start"""
    return requests.post(f"{BASE_URL}/v1/s1/e5/actions/start", json=None, headers=HEADERS)


def perform_turn(json):
    """perform_turn"""
    return requests.post(f"{BASE_URL}/v1/s1/e5/actions/perform-turn", json=json, headers=HEADERS)


def perform_turn_lecture():
    """perform_turn_lecture"""
    json={
        "action": ACTION_READ_RADAR,
        "attack_position": None
    }
    return perform_turn(json)

def tranform_x(x):
    equivalent_x = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    return equivalent_x[x]

def tranform_y(y):
    return y + 1

def perform_turn_attack(x, y):
    """perform_turn_attack"""
    json={
        "action": ACTION_ATTACK,
        "attack_position": {
            "x": tranform_x(x),
            "y": tranform_y(y)
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
    rows = [row for row in rows if row.strip() != '']

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


def process_lecture(lecture_string):
    """process_lecture"""
    global TURN
    grid, enemy_pos, valiant_position = parse_radar_data(lecture_string)
    predicted_next_position = predict_enemy_movement(grid, enemy_pos)
    print_board(grid)
    print(f"👾 Nave enemiga detectada en: {tranform_indexes_to_coordinates(enemy_pos[0], enemy_pos[1])}")
    print(f"🔥 {TURN} Coordenadas de ataque ", tranform_indexes_to_coordinates(predicted_next_position[0], predicted_next_position[1]))
    TURN += 1
    return predicted_next_position


def lecture():
    """lecture"""
    lecture_response = perform_turn_lecture()
    lecture_string = get_lecture_response(lecture_response)
    return process_lecture(lecture_string)


def attack(predicted_next_position):
    """attack"""
    i, j = predicted_next_position
    attack_x, attack_y = tranform_indexes_to_coordinates(i, j)
    print(f"🔥 Coordenadas ({attack_x}, {attack_y}); Indices: ({i}, {j})")
    attack_response = perform_turn_attack(attack_x, attack_y)

    if attack_response.status_code == 200:
        print("🤖 ¡Ataque exitoso! La nave enemiga ha sido destruida. ", attack_response.text)
    else:
        print("🤖 El ataque falló. ¡La Hope está en peligro! ", attack_response.text)


def execute_command(predicted_next_position):
    """execute_command"""
    while True:
        comando = input("🔧 Ingresa un comando (leer, atacar, end): ").strip().lower()

        if comando == "leer":
            predicted_next_position = lecture()
        elif comando == "atacar":
            attack(predicted_next_position)
        elif comando == "end":
            print("👋 Finalizando el programa...")
            break
        else:
            print(f"❌ Comando no reconocido: '{comando}'")

        print("🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩")
        print("")
        print("")


def start_mode():
    """start_mode"""
    global TURN
    command = input("🔧 Indicar modo de inicio (new, continue, lecture):  ").strip().lower()

    if command == "new":
        main()
    elif command == "continue":
        continue_turn = None
        while continue_turn is None or int(continue_turn) > 4:
            continue_turn = input("🔧 ultimo turno: ").strip()
            if int(continue_turn) <= 4:
                TURN = int(continue_turn)
        state = input("🔧 lectura ultimo estado: ").strip()
        predicted_next_position = process_lecture(str(state))
        execute_command(predicted_next_position)
    elif command == "lecture":
        execute_command("")
    elif command == "end":
        print("👋 Finalizando el programa...")
    else:
        print(f"❌ Comando no reconocido: '{command}'")


def main():
    """Controla la lógica del juego."""
    start_time = time.time()

    # 1. Leer radar
    response = start_battle()
    radar_string = get_start_response(response)

    # Preguntar si continuar con lectura de datos o pasar a ejecutar los turnos
    start_confirmation = input("🔧 Continuar con start esperado? (S, N):  ").strip().lower()
    if start_confirmation == "n":
        execute_command("")
    else:
        grid, enemy_pos, valiant_position = parse_radar_data(radar_string)

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
    """print_board"""
    for i, fila in enumerate(matriz):
        linea = ""
        for celda in fila:
            contenido = celda[1]
            linea += contenido + " "
        print(linea.strip() + f"    {7 - i} |{8 - i}")

    print("")
    print("")
    print("0 1 2 3 4 5 6 7")
    print("a b c d e f g h")
    print("")
    print("")


if __name__ == "__main__":
    start_mode()
