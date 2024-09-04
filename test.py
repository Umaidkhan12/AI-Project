import random

'''
[                                   [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],     [False, False, False, False, False, False, False, False, False, False], 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]      [False, False, False, False, False, False, False, False, False, False], 
]                                   ]
'''

def generate_maze_dfs(width, height):
    # Initialize the maze with walls (0 represents walls)
    maze = [[0 for _ in range(width)] for _ in range(height)]
    # Stack for DFS
    stack = []
    visited = [[False for _ in range(width)] for _ in range(height)]

    def is_valid(x, y):
        """Check if the position (x, y) is within maze boundaries and unvisited."""
        return 0 <= x <= width and 0 <= y <= height and not visited[y][x]

    def get_neighbors(x, y):
        """Get unvisited neighbors."""
        neighbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                neighbors.append((nx, ny))
        return neighbors

    def dfs(x, y):
        stack.append((x, y))
        visited[y][x] = True
        maze[y][x] = 1  # Mark the cell as part of the maze (1 represents path)

        while stack:
            x, y = stack[-1]
            neighbors = get_neighbors(x, y)
            if neighbors:
                nx, ny = random.choice(neighbors)
                # Remove the wall between (x, y) and (nx, ny)
                maze[(y + ny) // 2][(x + nx) // 2] = 1
                maze[ny][nx] = 1
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

    # Start DFS from the top-left corner
    dfs(1, 1)

    return maze

# Example usage
width, height = 100, 100
maze = generate_maze_dfs(width, height)

for row in maze:
    print(' '.join(['#' if cell == 0 else '.' for cell in row]))
