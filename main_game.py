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


# def generate_symbols():
#     EMPTY_SPACE_SYMBOL = (".", Fore.WHITE)
#     WALL_SYMBOL = ("#", Fore.WHITE)
#     TRAP_SYMBOL = ("T", Fore.RED)
#     GOLD_SYMBOL = ("G", Fore.YELLOW)
#     EXIT_SYMBOL = ("E", Fore.MAGENTA)
#     PLAYER_SYMBOL = ("P", Fore.BLUE)
#
#     return {
#         ".": handle_wall_symbol(),
#         "T": handle_trap_symbol(),
#         "G": handle_gold_symbol(),
#         "E": handle_exit_symbol()
#     }


def take_gold() -> int:
    GOLD = 10
    return GOLD


def show_gold(treasures: int) -> None:
    print(
        f'You found treasure! Current amount of treasures: {treasures}'
    )


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


def show_hud(
    health: int,
    gold: int,
    control_commands: dict[str, str]
) -> None:
    control_commands_list = [
        f'{control_symbol} - {description}'
        for control_symbol, description in control_commands.items()
    ]

    formatted_control_commands_list = ', '.join(control_commands_list)

    text_color = Fore.BLUE
    decore_color = Fore.GREEN

    print(decore_color + "------------------------------")
    print(f"HEALTH: {health} | TREASURES: {gold}")
    print(text_color + f"Control commands: {formatted_control_commands_list}")
    print(decore_color + "------------------------------")


def find_current_player_index(
        map: list,
        player_symbol: str
) -> tuple[int, int] | tuple[None, None]:
    if map is None:
        return None, None

    SYMBOL_INDEX = 0

    for row_index, row in enumerate(map):
        for cell_index, cell in enumerate(row):
            if cell[SYMBOL_INDEX] == player_symbol:
                return row_index, cell_index

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

        row_index = map.index(row)
        map[row_index] = row

    return map


def print_map(map: list):
    symbol_index = 0
    symbol_color_index = 1

    for hall in map:
        for cell in hall:
            symbol = cell[symbol_index]
            symbol_color = cell[symbol_color_index]
            line_ending = ' '

            print(symbol_color + symbol, end=line_ending)

        print()


def get_next_symbol(map: list, row_index: int, cell_index: int) -> str:
    next_symbol = map[row_index][cell_index]
    return next_symbol


def is_out_of_range(map: list[list], row_index: int, cell_index: int) -> bool:
    row_count = len(map)

    cells_row_index = 0
    cells_count = len(map[cells_row_index])

    is_out_row = row_index < 0 or row_index >= row_count
    is_out_cells_row = cell_index < 0 or cell_index >= cells_count

    return is_out_row or is_out_cells_row


def play():
    map = create_map()

    is_win = False
    is_live = True

    moves = 0
    gold = 0
    player_health = 100

    UP_DIRECTION_COMMAND = "W"
    DOWN_DIRECTION_COMMAND = "S"
    LEFT_DIRECTION_COMMAND = "A"
    RIGHT_DIRECTION_COMMAND = "D"
    QUIT_TO_MENU_COMMAND = "Q"

    PLAYER_SYMBOL = "P"
    EMPTY_SPACE_SYMBOL = "."

    commands = {
        "W": "Up",
        "S": "Down",
        "A": "Left",
        "D": "Right",
        "Q": "Quit_to_menu",
    }

    print(commands)

    STEP = 1
    SYMBOL_INDEX = 0
    command = ''
    show_rules()

    while not is_win and is_live and command != QUIT_TO_MENU_COMMAND:
        colored_map = paint_map(map)
        print_map(colored_map)
        show_hud(player_health, gold, commands)

        print()

        command = input('Enter your command: ').upper().strip()

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
                next_symbol = get_next_symbol(map, next_row_index, next_cell_index)
                symbol = next_symbol[SYMBOL_INDEX]
                is_wall_ahead = handle_wall_symbol(symbol)
                is_win = handle_exit_symbol(symbol)
                health = handle_trap_symbol(symbol)
                player_health -= health

                if player_health <= 0:
                    is_live = False

                taken_gold = handle_gold_symbol(symbol)
                gold += taken_gold

                if not is_wall_ahead:
                    map[next_row_index][next_cell_index] = PLAYER_SYMBOL
                    map[current_row_index][current_cell_index] = EMPTY_SPACE_SYMBOL
                    moves += 1
                else:
                    print(
                        "\n"
                        "You can't move - wall ahead"
                        "\n"
                    )
            else:
                print("You have gone beyond the map.")
        else:
            print("Wrong control command")

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


def play1():
    is_win = False
    map = create_map()
    result = move_player(map)
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