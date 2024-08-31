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
        img = pygame.image.load(BASE_IMG_PATH + filename)
        return img

class GameTesting:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.Run = True

        # Load images
        self.assets = {
            'player': Utils().load_image('Box.png'),
            'wall': Utils().load_image('wall.jpg')
        }

        # Scale images to the default TILE_SIZE
        self.player_image = pygame.transform.scale(self.assets['player'], (TILE_SIZE, TILE_SIZE))
        self.wall_image = pygame.transform.scale(self.assets['wall'], (TILE_SIZE, TILE_SIZE))

        # Initialize player
        self.player_rect = self.player_image.get_rect(centerx=200, centery=HEIGHT)

        # Load and scale map
        self.map_layout = self.load_map_from_csv(BASE_IMG_PATH + 'FinalMazaMap.csv')
        self.tile_size = TILE_SIZE
        self.update_map_dimensions()

    def load_map_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            map_data = [[int(tile) for tile in row] for row in reader]
        return map_data
    
    def update_map_dimensions(self):
        self.map_width = len(self.map_layout[0]) * self.tile_size
        self.map_height = len(self.map_layout) * self.tile_size

    def draw_map(self):
        for y, row in enumerate(self.map_layout):
            for x, tile in enumerate(row):
                if tile == 0:
                    self.screen.blit(self.wall_image, (x * self.tile_size, y * self.tile_size))

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
        self.player_rect.move_ip(movement.x, movement.y)

        # Keep player within screen bounds
        self.player_rect.x = max(0, min(self.player_rect.x, WIDTH - self.player_rect.width))
        self.player_rect.y = max(0, min(self.player_rect.y, HEIGHT - self.player_rect.height))

    def game(self):
        while self.Run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Run = False

            self.movementController()

            self.screen.fill((255, 255, 255))  # Fill the screen with white
            self.draw_map()
            self.screen.blit(self.player_image, self.player_rect.topleft)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    GameTesting().game()
