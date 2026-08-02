from colorama import Fore, init

init(autoreset=True)


def print_result(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)

        print(f'{function.__name__} вернула: {result}')

        return result

    return wrapper


def symbols():
    EMPTY_SPACE_SYMBOL = (".", Fore.WHITE)

    WALL_SYMBOL = ("#", Fore.WHITE)

    TRAP_SYMBOL = ("T", Fore.RED)

    GOLD_SYMBOL = ("G", Fore.YELLOW)

    EXIT_SYMBOL = ("E", Fore.MAGENTA)

    PLAYER_SYMBOL = ("P", Fore.BLUE)

    symbols = [

        EMPTY_SPACE_SYMBOL,

        WALL_SYMBOL,

        TRAP_SYMBOL,

        GOLD_SYMBOL,

        EXIT_SYMBOL,

        PLAYER_SYMBOL,

    ]

    return symbols


def take_gold() -> int:
    GOLD = 10

    return GOLD


def show_gold(treasures: int) -> None:
    print(f'You found treasure! Current amount of treasures: {treasures}')


def take_damage() -> int:
    DAMAGE = 25

    return DAMAGE


def show_damage(player_health: int, DAMAGE) -> None:
    print(

        f'You have walked into a trap.! -{DAMAGE} health.'

        f'There is some health left: {player_health}'

    )


def is_health_full(player_health: int) -> bool:
    is_health_full = True

    if player_health == 0:
        is_health_full = False

    return is_health_full


def handle_wall_symbol(symbol: str):
    WALL_SYMBOL = "#"

    if symbol == WALL_SYMBOL:
        return True

    return False


def handle_trap_symbol(symbol: str):
    TRAP_SYMBOL = "T"

    health = 0

    if symbol == TRAP_SYMBOL:

        health = take_damage()

        if health == 0:
            return health

    return health


def handle_gold_symbol(symbol: str):
    GOLD_SYMBOL = "G"

    gold = 0

    if symbol == GOLD_SYMBOL:
        gold = take_gold()

        return gold

    return gold


def handle_exit_symbol(symbol: str):
    EXIT_SYMBOL = "E"

    if symbol == EXIT_SYMBOL:
        return True

    return False


symbol_functions = {

    "G": handle_gold_symbol,

    "T": handle_trap_symbol,

    "E": handle_exit_symbol

}


def handle_symbol(symbol: str):
    handlers = {

        ".": handle_wall_symbol(),

        "T": handle_trap_symbol(),

        "G": handle_gold_symbol()

    }

    return handlers.get(symbol)


def show_hud(health: int, gold: int, control_commands: list[str]) -> None:
    text_color = Fore.BLUE

    decore_color = Fore.GREEN

    print(decore_color + "------------------------------")

    print(f"HEALTH: {health} | TREASURES: {gold}")

    print(text_color + "Control commands: W - Up, S - Down, A - Left, D - Right, Q - quit to menu")

    print(decore_color + "------------------------------")


def find_current_player_index(map: list, player_symbol: str) -> tuple[int, int] | tuple[None, None]:
    if map is None:
        return None, None

    SYMBOL_INDEX = 0

    for index_hall, row in enumerate(map):
        for index_cell, cell in enumerate(row):
            cell_symbol = cell[SYMBOL_INDEX]

            if cell_symbol == player_symbol:
                return index_hall, index_cell

    return -1, -1


def create_map():
    map = [

        ['.', '.', '.', 'T', '.'],

        ['.', '#', '.', '.', '.'],

        ['.', 'T', 'G', '#', '.'],

        ['T', 'G', 'G', 'P', 'E'],

    ]

    return map


def paint_map(map: list):
    for row in map:
        for cell in row:
            for items in symbols():
                new_symbol = items[0]
                if cell == new_symbol:
                    cell_index = row.index(cell)
                    row[cell_index] = items

        hall_index = map.index(row)
        map[hall_index] = row

    return map


def print_map(map: list):
    for hall in map:
        for cell in hall:
            symbol = cell[0]
            symbol_color = cell[1]
            line_ending = ' '

            print(symbol_color + symbol, end=line_ending)

        print()


def get_next_symbol(map: list, hall_index: int, cell_index: int) -> str:
    return map[hall_index][cell_index]

def is_out_of_range(area: list[list], row_index: int, cell_index: int) -> bool:
    row_count = len(area)
    column_count = len(area[0])

    return (row_index < 0 or row_index >= row_count or
            cell_index < 0 or cell_index >= column_count)


def move_player(map):
    EMPTY_SPACE_SYMBOL = "."

    moves = 0

    is_exit_reach = False
    is_health_zero = False
    command = ''

    show_rules()

    return moves, gold, player_health


def show_rules():
    print(
        """
        You need to reach the end of the dungeon "E" symbol without spending
        all your health, as you may encounter traps "T" wich can damage you
        - 25 health. When the health becomes 0, the game ends.
        You can also collect treasures "G" along the way.

        Symbols:
        P - Player
        # - Wall
        G - Gold
        T - Trap

        Control commands:
        W - Up
        S - Down
        A - Left
        D - Right
        Q - Quit to menu
        """
    )


def show_results(results: tuple):
    moves, treasure, health = results

    print(
        f'Health: {health} \n'
        f'Treasure: {treasure} \n'
        f'Moves: {moves} \n'
    )


def play():
    is_win = False
    is_live = True
    QUIT_COMMAND = "Q"

    map = create_map()

    player_health = 100
    gold = 0

    UP_DIRECTION_COMMAND = "W"
    DOWN_DIRECTION_COMMAND = "S"
    LEFT_DIRECTION_COMMAND = "A"
    RIGHT_DIRECTION_COMMAND = "D"

    commands = [
        UP_DIRECTION_COMMAND,
        DOWN_DIRECTION_COMMAND,
        LEFT_DIRECTION_COMMAND,
        RIGHT_DIRECTION_COMMAND
    ]

    PLAYER_SYMBOL = "P"
    STEP = 1

    command = ''


    while not is_win and is_live and command != QUIT_COMMAND:
        colored_map = paint_map(map)
        print_map(colored_map)
        show_hud(player_health, gold, commands)

        print()

        command = input('Enter your command: ').capitalize().strip()

        if command in commands:
            current_row_index, current_cell_index = find_current_player_index(map, PLAYER_SYMBOL)

            next_row_index = current_row_index
            next_cell_index = current_cell_index

            if command == UP_DIRECTION_COMMAND:
                next_row_index = current_row_index - STEP
            elif command == DOWN_DIRECTION_COMMAND:
                next_row_index = current_row_index + STEP
            elif command == LEFT_DIRECTION_COMMAND:
                next_cell_index = current_cell_index - STEP
            elif command == RIGHT_DIRECTION_COMMAND:
                next_cell_index = current_cell_index + STEP

            is_out_of_map_range = is_out_of_range(map, next_row_index, next_cell_index)

            if not is_out_of_map_range:

            else:
                print("You have gone beyond the map.")




            if command == UP_DIRECTION_COMMAND or command == DOWN_DIRECTION_COMMAND:
                if command == UP_DIRECTION_COMMAND:
                    up_direction_index = current_row_index - NEXT_INDEX
                    next_hall_index = up_direction_index
                elif command == DOWN_DIRECTION_COMMAND:
                    down_direction_index = current_row_index + NEXT_INDEX
                    next_hall_index = down_direction_index

                is_not_out_of_range = is_out_of_range(area, next_hall_index)

                if is_not_out_of_range:
                    next_symbol = get_next_symbol(map, next_hall_index, current_cell_index)
                    real_symbol = next_symbol[0]
                    is_wall_ahead = handle_wall_symbol(real_symbol)
                    is_exit_reach = handle_exit_symbol(real_symbol)
                    health = handle_trap_symbol(real_symbol)

                    player_health -= health

                    if player_health <= 0:
                        is_health_zero = True

                    taken_gold = handle_gold_symbol(real_symbol)

                    gold += taken_gold

                    if not is_wall_ahead:
                        map[next_hall_index][current_cell_index] = PLAYER_SYMBOL
                        map[current_row_index][current_cell_index] = EMPTY_SPACE_SYMBOL
                        moves += 1
                    else:
                        print("You can't move - wall ahead")
                else:
                    print("You have gone beyond the map.")
            elif command == LEFT_DIRECTION_COMMAND or command == RIGHT_DIRECTION_COMMAND:
                area = map[current_row_index]

                if command == LEFT_DIRECTION_COMMAND:
                    left_direction_index = current_cell_index - NEXT_INDEX
                    next_cell_index = left_direction_index
                elif command == RIGHT_DIRECTION_COMMAND:
                    right_direction_index = current_cell_index + NEXT_INDEX

                    next_cell_index = right_direction_index
                is_not_out_of_range = is_out_of_range(area, next_cell_index)

                if is_not_out_of_range:
                    next_symbol = get_next_symbol(map, current_row_index, next_cell_index)
                    real_symbol = next_symbol[0]
                    is_wall_ahead = handle_wall_symbol(real_symbol)
                    is_exit_reach = handle_exit_symbol(real_symbol)
                    health = handle_trap_symbol(real_symbol)
                    player_health -= health

                    if player_health <= 0:
                        is_health_zero =

                    taken_gold = handle_gold_symbol(real_symbol)
                    gold += taken_gold
                    if not is_wall_ahead:
                        map[current_row_index][next_cell_index] = PLAYER_SYMBOL
                        map[current_row_index][current_cell_index] = EMPTY_SPACE_SYMBOL
                        moves += 1
                    else:
                        print(
                            "\n"
                            "You can't move - wall ahead"
                            "\n"
                        )
                else:
                    print("You can't move beyond the map.")
        else:
            print("Wrong control command")

    show_results(result)


def show_end_window():
    print("End of the game")

def show_error_message():
    print("Wrong menu input command")

def main():
    QUIT_COMMAND_NUMBER = 3

    COMMANDS = {
        1: "Start game",
        2: "Show rules",
        QUIT_COMMAND_NUMBER: "Quit"
    }
    COMMAND_FUNCTIONS = {
        1: play,
        2: show_rules,
        QUIT_COMMAND_NUMBER: show_end_window,
    }

    input_command_number = -1

    while input_command_number != QUIT_COMMAND_NUMBER:
        print("=== Treasure Dungeon ===")

        for command_number, command_name in COMMANDS.items():
            print(f'{command_number}. {command_name}')

        user_input = input('Choose number command: ').strip()

        if user_input.isdigit():
            input_command_number = int(user_input)
            command_function = COMMAND_FUNCTIONS.get(input_command_number, None)

            if command_function:
                command_function()
            else:
                show_error_message()
        else:
            print('Принимается только номер')

main()