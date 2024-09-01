import pygame
import pygame.math as math
import csv

# Constants
BASE_IMG_PATH = 'Assets/'
WIDTH, HEIGHT = 900, 900
FPS = 60
CHARACTER_SPEED = 5
TILE_SIZE = 16

class Utils:
    def load_image(self, filename):
        return pygame.image.load(BASE_IMG_PATH + filename)

class GameTesting:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.Run = True

        # Load and scale images
        self.assets = {
            'player': Utils().load_image('Box.png'),
            'wall': Utils().load_image('wall.jpg'),
            'ground': Utils().load_image('ground.jpg')
        }
        self.player_image = pygame.transform.scale(self.assets['player'], (TILE_SIZE, TILE_SIZE))
        self.wall_image = pygame.transform.scale(self.assets['wall'], (TILE_SIZE, TILE_SIZE))
        self.ground_image = pygame.transform.scale(self.assets['ground'], (TILE_SIZE, TILE_SIZE))

        # Initialize player
        self.player_rect = self.player_image.get_rect(centerx=200, centery=HEIGHT - TILE_SIZE)

        # Load and scale map
        map_layout = self.load_map_from_csv(BASE_IMG_PATH + 'FinalMazeMap.csv')
        
        # Create a duplicate of map_layout for map creation
        self.map_creation = [row[:] for row in map_layout]
        
        # Generate wall rectangles
        self.wall_rects = self.map_wall_rect()

        # Track whether player is in the touch range
        self.in_touch_range = False

    def map_wall_rect(self):
        wall_rects = []
        for y, row in enumerate(self.map_creation):
            for x, tile in enumerate(row):
                if tile == 0:
                    wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return wall_rects

    def load_map_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            return [[int(tile) for tile in row] for row in reader]

    def draw_map(self):
        for y, row in enumerate(self.map_creation):
            for x, tile in enumerate(row):
                if tile == 0:
                    self.screen.blit(self.wall_image, (x * TILE_SIZE, y * TILE_SIZE))
                elif tile == -1:
                    self.screen.blit(self.ground_image, (x * TILE_SIZE, y * TILE_SIZE))

    def update_map(self, start_x, start_y, end_x, end_y, new_value):
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if 0 <= y < len(self.map_creation) and 0 <= x < len(self.map_creation[y]):
                    self.map_creation[y][x] = new_value
        # Recalculate wall rects after map update
        self.wall_rects = self.map_wall_rect()

    def movementController(self):
        keys = pygame.key.get_pressed()
        direction = math.Vector2(0, 0)
        
        if keys[pygame.K_LEFT]:
            direction.x = -1
        if keys[pygame.K_RIGHT]:
            direction.x = 1
        if keys[pygame.K_UP]:
            direction.y = -1
        if keys[pygame.K_DOWN]:
            direction.y = 1

        if direction.length() > 0:
            direction.normalize_ip()
        
        movement = direction * CHARACTER_SPEED
        new_player_rect = self.player_rect.move(movement.x, movement.y)

        # Check for collisions
        if not any(new_player_rect.colliderect(wall_rect) for wall_rect in self.wall_rects):
            self.player_rect.move_ip(movement.x, movement.y)

        # Keep player within screen bounds
        self.player_rect.x = max(0, min(self.player_rect.x, WIDTH - self.player_rect.width))
        self.player_rect.y = max(0, min(self.player_rect.y, HEIGHT - self.player_rect.height))

        # Check if the player is on the target tile
        tile_x = self.player_rect.x // TILE_SIZE
        tile_y = self.player_rect.y // TILE_SIZE
        print(tile_x," ", tile_y)

        # Check if the player is in the touch range of the tile
        rightMostWall = pygame.Rect(42 * TILE_SIZE, 32 * TILE_SIZE, 
                                        (45 - 42 + 1) * TILE_SIZE, 
                                        (37 - 32 + 1) * TILE_SIZE)

        if rightMostWall.colliderect(self.player_rect):
            if not self.in_touch_range:
                self.in_touch_range = True
                self.update_map(46, 33, 46, 36, 0)
        else:
            if self.in_touch_range:
                self.in_touch_range = False
                self.update_map(46, 33, 46, 36, -1)
        
    def game(self):
        while self.Run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Run = False

            self.movementController()
            self.screen.fill((255, 255, 255))
            self.draw_map()
            self.screen.blit(self.player_image, self.player_rect.topleft)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    GameTesting().game()
