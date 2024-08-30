import pygame
import csv

# Constants
WIDTH, HEIGHT = 990, 1030
FPS = 60
CHARACTER_SPEED = 5
TILE_SIZE = 18
MAP_FILE = 'Assets/FinalMazaMap.csv'
WALL_TILE = 0  # Represents walls in the map
EMPTY_TILE = 1  # Represents empty spaces in the map

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Box Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # Load images
        self.tile_image = pygame.image.load('Assets/wall.jpg')
        self.tile_image = pygame.transform.scale(self.tile_image, (TILE_SIZE, TILE_SIZE))
        self.empty_tile_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.empty_tile_image.fill((255, 255, 255))  # White tiles for empty spaces
        self.character_image = pygame.image.load('Assets/Box.png')
        self.character_image = pygame.transform.scale(self.character_image, (TILE_SIZE, TILE_SIZE))

        # Load map layout from CSV
        self.map_layout = self.load_map_from_csv(MAP_FILE)
        self.map_width = len(self.map_layout[0]) * TILE_SIZE
        self.map_height = len(self.map_layout) * TILE_SIZE

        # Calculate character starting position (bottom center of the map)
        self.character_rect = self.character_image.get_rect(
            center=(self.map_width // 2, self.map_height - TILE_SIZE // 2)
        )
        
        # Initialize map position
        self.map_x, self.map_y = 0, 0

        # Create wall rectangles for collision detection
        self.wall_rects = self.create_wall_rects()
        self.map_surface = pygame.Surface((self.map_width, self.map_height))

    def load_map_from_csv(self, filename):
        """Load map layout from a CSV file."""
        with open(filename, newline='') as csvfile:
            return [[int(tile) for tile in row] for row in csv.reader(csvfile)]

    def create_wall_rects(self):
        """Create a list of rectangles representing wall tiles."""
        wall_rects = []
        for y, row in enumerate(self.map_layout):
            for x, tile in enumerate(row):
                if tile == WALL_TILE:
                    wall_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return wall_rects

    def draw_map(self):
        """Draw the map on the off-screen surface and blit to the screen."""
        self.map_surface.fill((255, 255, 255))  # Fill with white
        for y, row in enumerate(self.map_layout):
            for x, tile in enumerate(row):
                tile_image = self.tile_image if tile == WALL_TILE else self.empty_tile_image
                self.map_surface.blit(tile_image, (x * TILE_SIZE, y * TILE_SIZE))

        # Draw the map surface to the screen with scrolling
        self.screen.blit(self.map_surface, (-self.map_x, -self.map_y))

    def draw_character(self):
        """Draw the character on the screen."""
        self.screen.blit(self.character_image, self.character_rect.topleft)

    def handle_movement(self):
        """Handle movement of the character and scrolling of the map."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -CHARACTER_SPEED
        if keys[pygame.K_RIGHT]:
            dx = CHARACTER_SPEED
        if keys[pygame.K_UP]:
            dy = -CHARACTER_SPEED
        if keys[pygame.K_DOWN]:
            dy = CHARACTER_SPEED

        # Move character
        new_rect = self.character_rect.move(dx, dy)

        # Check for collisions with walls
        for wall_rect in self.wall_rects:
            if new_rect.colliderect(wall_rect):
                if dx > 0:  # Moving right
                    new_rect.right = wall_rect.left
                if dx < 0:  # Moving left
                    new_rect.left = wall_rect.right
                if dy > 0:  # Moving down
                    new_rect.bottom = wall_rect.top
                if dy < 0:  # Moving up
                    new_rect.top = wall_rect.bottom

        # Update character position
        self.character_rect = new_rect


        # Clamp map position to keep the map within the window
        self.map_x = max(0, min(self.map_x, self.map_width - WIDTH))
        self.map_y = max(0, min(self.map_y, self.map_height - HEIGHT))

    def main(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_movement()
            self.screen.fill((255, 255, 255))  # Clear the screen with white
            self.draw_map()
            self.draw_character()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    Game().main()
