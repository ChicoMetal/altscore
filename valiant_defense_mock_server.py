from fastapi import FastAPI
import random
import uvicorn
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

grid_size = 8
column_labels = "abcdefgh"

current_movement = 0
ACTION_READ_RADAR = "radar"
ACTION_ATTACK = "attack"

def generate_grid():
    grid = [["0" for _ in range(grid_size)] for _ in range(grid_size)]
    
    # Place obstacles
    obstacles = [(2, 4), (3, 4), (5, 4), (5, 6), (6, 4)]
    for x, y in obstacles:
        grid[x][y] = "$"
    
    # Place Hope
    hope_pos = (7, 5)
    grid[hope_pos[0]][hope_pos[1]] = "#"
    
    # Place enemy in a random free spot
    free_positions = [(x, y) for x in range(grid_size) for y in range(grid_size) 
                      if (x, y) != hope_pos and grid[x][y] == "0"]
    enemy_pos = random.choice(free_positions)
    grid[enemy_pos[0]][enemy_pos[1]] = "^"
    
    return grid, enemy_pos

def format_grid(grid):
    radar_report = []
    for row_idx, row in enumerate(grid, start=1):  # Comenzamos desde 1
        formatted_row = "".join(
            f"{column_labels[col_idx]}{cell}{row_idx}" if cell in ("$", "#", "^") 
            else f"{column_labels[col_idx]}{row_idx:02d}"  
            for col_idx, cell in enumerate(row)
        )
        radar_report.append(formatted_row)
    return "|".join(radar_report) + "|"

class AttackPosition(BaseModel):
    x: str
    y: int

class AttackCommand(BaseModel):
    action: str
    attack_position: Optional[AttackPosition] = None

@app.post("/v1/s1/e5/actions/start")
def start1():
    global grid, enemy_pos
    grid, enemy_pos = generate_grid()
    return format_grid(grid)

@app.post("/v1/s1/e5/actions/perform-turn")
def perform_turn1(command: AttackCommand):
    global grid, enemy_pos, current_movement

    response_body = {
        "performed_action": command.action,
        "turns_remaining": current_movement,
        "time_remaining": 8,
        "action_result": None,
        "message": None
    }

    # Basic move logic: move enemy towards Hope avoiding obstacles
    def move_enemy(enemy_pos):
        x, y = enemy_pos
        target_x, target_y = 7, 5  # Hope's position

        best_move = enemy_pos
        best_distance = abs(target_x - x) + abs(target_y - y)

        possible_moves = [(x+dx, y+dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        random.shuffle(possible_moves)

        for nx, ny in possible_moves:
            if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx][ny] not in ("$", "#"):
                new_distance = abs(target_x - nx) + abs(target_y - ny)
                if new_distance < best_distance:
                    best_move = (nx, ny)
                    best_distance = new_distance
        return best_move

    if command.action == ACTION_READ_RADAR:
        new_enemy_pos = move_enemy(enemy_pos)
        grid[enemy_pos[0]][enemy_pos[1]] = "0"
        grid[new_enemy_pos[0]][new_enemy_pos[1]] = "^"
        enemy_pos = new_enemy_pos
        # return {"radar": format_grid(grid)}

        response_body["action_result"] = format_grid(grid)
        response_body["message"] = "Continue"
        return response_body
    elif command.action == ACTION_ATTACK:
        print(f"actions: x: {command.attack_position.x}; y: {command.attack_position.y}")
        print("Grid", grid)
        print("Posicion nave enemiga", enemy_pos)
        new_enemy_pos = move_enemy(enemy_pos)
        grid[enemy_pos[0]][enemy_pos[1]] = "0"
        grid[new_enemy_pos[0]][new_enemy_pos[1]] = "^"
        enemy_pos = new_enemy_pos
        response_body["action_result"] = format_grid(grid)

        if command.attack_position.x is not None and command.attack_position.y is not None:
            response_body["message"] = "Correcto"
            return response_body
        else:
            response_body["message"] = "incorrecto"
            return response_body

    response_body["action_result"] = ""
    response_body["message"] = "error"
    return response_body



@app.post("/v1/s1/e5/actions/start1")
def start():
    # return 'a01b01c01d01e01f01g01h01|a02b02c02d02e$2f02g02h02|a03b03c03d03e03f03g03h$3|a04b04c04d04e04f04g04h04|a05b05c05d05e$5f05g^5h05|a06b06c06d06e$6f06g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e08f#8g08h08|'
    return "start"

@app.post("/v1/s1/e5/actions/perform-turn1")
def perform_turn(command: AttackCommand):
    global current_movement

    response_body = {
        "performed_action": command.action,
        "turns_remaining": current_movement,
        "time_remaining": 8,
        "action_result": None,
        "message": None
    }

    movements = [
        "a01b01c01d01e01f01g01h01|a02b02c02d02e$2f02g02h02|a03b03c03d03e03f03g03h$3|a04b04c04d04e04f04g04h04|a05b05c05d05e$5f05g05h05|a06b06c06d06e$6f06g^6h06|a07b07c07d07e07f07g07h07|a08b08c08d08e08f#8g08h08|",
        "a01b01c01d01e01f01g01h01|a02b02c02d02e$2f02g02h02|a03b03c03d03e03f03g03h$3|a04b04c04d04e04f04g04h04|a05b05c05d05e$5f05g05h05|a06b06c06d06e$6f^6g06h06|a07b07c07d07e07f07g07h07|a08b08c08d08e08f#8g08h08|"
    ]
    if command.action == ACTION_READ_RADAR:
        new_state = movements[current_movement]
        current_movement += 1
        response_body["action_result"] = new_state
        response_body["message"] = "Continue"
        return response_body
    elif command.action == ACTION_ATTACK:
        current_movement = 0
        if int(command.attack_position.x) == 5 and command.attack_position.y == 6:
            response_body["action_result"] = ""
            response_body["message"] = "Correcto"
            return response_body
        else:
            response_body["action_result"] = ""
            response_body["message"] = "incorrecto"
            return response_body

    current_movement = 0
    response_body["action_result"] = ""
    response_body["message"] = "error"
    return response_body



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)