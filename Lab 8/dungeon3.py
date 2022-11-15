import copy

MAP_FILE = 'cave_map.txt'

def load_map(map_file: str) -> list[list[str]]:
    grid = []
    with open(map_file, 'r') as file: 
        for line in file:
            convert = list(line.strip()) # Converts to a list and strips the "\n"
            grid.append(convert) # Appends the lists to the list grid
    return grid

def find_start(grid: list[list[str]]) -> list[int, int]:
    starting_letter = "S"
    starting_index = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == starting_letter:
                starting_index.append(i)
                starting_index.append(j)
                break
    return starting_index

def get_command() -> str:
    while True:
        user_input = input("> ")
        if user_input.lower() in ["go north", "go south", "go east", "go west", "show map", "escape"]:
            return user_input
        print("I do not understand.")

def display_map(grid: list[list[str]], player_position: list[int, int]) -> None:
    new_grid = copy.deepcopy(grid)
    row = player_position[0]
    col = player_position[1]
    new_grid[row][col] = "@"
    for i in new_grid:
        for j in i:
            print(j, end = "")
        print()

def get_grid_size(grid: list[list[str]]) -> list[int, int]:
    """
    Returns the size of the grid.
    """
    rows = len(grid)
    cols = len(grid[0])
    return [rows, cols]
    
def is_inside_grid(grid: list[list[str]], position: list[int, int]) -> bool:
    """
    Checks if a given position is valid (inside the grid).
    """
    grid_rows, grid_cols = get_grid_size(grid)
    if (position[0] >= grid_rows) or (position[1] >= grid_cols):
        return False
    elif (position[0] < 0) or (position[1] < 0):
        return False
    else:
        return True

def look_around(grid: list[list[str]], player_position: list[int, int]) -> list:
    """
    Returns the allowed directions.
    """
    allowed_objects = ('S', 'F', '*')
    row = player_position[0]
    col = player_position[1]
    directions = []
    if is_inside_grid(grid, [row - 1, col]) and grid[row - 1][col] in allowed_objects:
        directions.append('north')
    if is_inside_grid(grid, [row + 1, col]) and grid[row + 1][col] in allowed_objects:
        directions.append('south')
    if is_inside_grid(grid, [row, col + 1]) and grid[row][col + 1] in allowed_objects:
        directions.append('east')
    if is_inside_grid(grid, [row, col - 1]) and grid[row][col - 1] in allowed_objects:
        directions.append('west')

    return directions

def move(direction: str, player_position: list[int, int], grid: list[list[str]]) -> bool:
    # print("direction = ", direction)
    valid_directions = look_around(grid, player_position)
    direction = direction.split(" ")[1]
    print(direction)
    print(player_position)
    row = player_position[0]
    col = player_position[1]
    if not direction in valid_directions:
        print("There is no way there.")
        return False
    if direction.lower() == "north":
        player_position[0] = player_position[0] - 1 
    elif direction.lower() == "south":
        player_position[0] = player_position[0] + 1 
    elif direction.lower() == "west":
        player_position[1] = player_position[1] - 1
    elif direction.lower() == "east":
        player_position[1] = player_position[1] + 1
    display_valid_directions(grid, player_position)
    return True, row, col

def display_valid_directions(grid, player_position):
    directions = look_around(grid, player_position)
    joined_directions = ", ".join(directions)
    print(f"You can go {joined_directions}")

def main():
    grid = load_map(MAP_FILE)
    starting_position = find_start(grid)
    look_around(grid, starting_position)
    display_valid_directions(grid, starting_position)
    while True:
        user_command = get_command()
        direction = user_command 
        if user_command.lower() == "escape":
            exit()
        elif user_command.lower() == "show map":
            display_map(grid, starting_position)
            display_valid_directions(grid, starting_position)
            continue
        get_grid_size(grid)
        move(direction, starting_position, grid)
        
if __name__ == '__main__':
    main()