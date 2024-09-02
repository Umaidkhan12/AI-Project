import pygame
import pygame.math as math
import csv

# Constants
BASE_IMG_PATH = 'Assets/'
WIDTH, HEIGHT = 900, 900
FPS = 60
CHARACTER_SPEED = 5
TILE_SIZE = 16
FONT_SIZE = 36
TEXT_COLOR = (0, 0, 0) 
LINE_SPACING = 5

class Utils:
    @staticmethod
    def load_image(filename):
        return pygame.image.load(BASE_IMG_PATH + filename)
    
class Button:
    def __init__(self, text, font, color, x, y, width, height):
        self.font = font
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self._update_surface()

    def _update_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.text_rect = self.surface.get_rect(center=self.rect.center)
    
    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)  # Button background
        screen.blit(self.surface, self.text_rect)  # Button text
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class GameTesting:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.reset_flags()
        
        # Load and scale images
        self.load_assets()

        # Initialize player and map
        self.initialize_player()
        self.initialize_map()
        
        # Initialize message display and restart button
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.restart_button = Button("Restart", self.font, (0, 0, 0), WIDTH // 2 - 50, HEIGHT // 2 + 50, 90, 40)

    def load_assets(self):
        self.assets = {
            'player': Utils.load_image('Box.png'),
            'wall': Utils.load_image('wall.jpg'),
            'grass': Utils.load_image('grass.jpg'),
            'ground': Utils.load_image('ground.png'),
            'finish': Utils.load_image('finish.png')
        }
        self.player_image = pygame.transform.scale(self.assets['player'], (TILE_SIZE, TILE_SIZE))
        self.wall_image = pygame.transform.scale(self.assets['wall'], (TILE_SIZE, TILE_SIZE))
        self.grass_image = pygame.transform.scale(self.assets['grass'], (TILE_SIZE, TILE_SIZE))
        self.ground_image = pygame.transform.scale(self.assets['ground'], (TILE_SIZE, TILE_SIZE))
        self.finish_image = pygame.transform.scale(self.assets['finish'], (TILE_SIZE, TILE_SIZE))

    def get_wall_rects(self):
        return [pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                for y, row in enumerate(self.map_creation)
                for x, tile in enumerate(row)
                if tile == 0]

    def load_map_from_csv(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            return [[int(tile) for tile in row] for row in reader]

    def draw_map(self):
        for y, row in enumerate(self.map_creation):
            for x, tile in enumerate(row):
                if tile == 0:
                    self.screen.blit(self.wall_image, (x * TILE_SIZE, y * TILE_SIZE))
                if tile == 1:
                    self.screen.blit(self.grass_image, (x * TILE_SIZE, y * TILE_SIZE))
                if tile == 2:
                    self.screen.blit(self.finish_image, (x * TILE_SIZE, y * TILE_SIZE))
                if tile == 3:
                    self.screen.blit(self.ground_image, (x * TILE_SIZE, y * TILE_SIZE))

        self.display_messages()

    def display_messages(self):
        if self.reach_center:
            self.show_msg("You've reached the center area!\nNow find the true exit!")
        if self.is_trapped:
            self.show_msg("You're trapped. Restart the game!")
            self.button_visible = True
            self.restart_button.draw(self.screen)
        if self.instantDeath:
            self.show_msg("You stepped on something you shouldn't have.\nRestart the game!")
            self.button_visible = True
            self.restart_button.draw(self.screen)
        if self.noEntry:
            self.show_msg("You are not eligible to enter")
        if self.game_over:
            self.show_msg("Congratulation!\nNew Game")
            self.button_visible = True
            self.restart_button.draw(self.screen)

    def update_map(self, start_x, start_y, end_x, end_y, new_value):
        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                if 0 <= y < len(self.map_creation) and 0 <= x < len(self.map_creation[y]):
                    self.map_creation[y][x] = new_value
        self.wall_rects = self.get_wall_rects()

    def movement_controller(self):
        if self.is_trapped or self.instantDeath or self.game_over:
            return

        keys = pygame.key.get_pressed()
        direction = math.Vector2(
            (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]),
            (keys[pygame.K_DOWN] - keys[pygame.K_UP])
        )

        if direction.length() > 0:
            direction.normalize_ip()
        
        movement = direction * CHARACTER_SPEED
        new_player_rect = self.player_rect.move(movement.x, movement.y)

        if not any(new_player_rect.colliderect(wall_rect) for wall_rect in self.wall_rects):
            self.player_rect.move_ip(movement.x, movement.y)

        self.player_rect.x = max(0, min(self.player_rect.x, WIDTH - self.player_rect.width))
        self.player_rect.y = max(0, min(self.player_rect.y, HEIGHT - self.player_rect.height))

        self.map_logic()

    def map_logic(self):
        tile_x = self.player_rect.x // TILE_SIZE
        tile_y = self.player_rect.y // TILE_SIZE

        rects = {
            'trueExit': pygame.Rect(1 * TILE_SIZE, 15 * TILE_SIZE, (3 - 1 + 1) * TILE_SIZE, (20 - 15 + 1) * TILE_SIZE),
            'centerRectWall1': pygame.Rect(30 * TILE_SIZE, 18 * TILE_SIZE, (33 - 30 + 1) * TILE_SIZE, (21 - 18 + 1) * TILE_SIZE),
            'centerRectWall2': pygame.Rect(28 * TILE_SIZE, 16 * TILE_SIZE, (35 - 28 + 1) * TILE_SIZE, (22 - 16 + 1) * TILE_SIZE),
            'upperTunnelWall': pygame.Rect(30 * TILE_SIZE, 10 * TILE_SIZE, (32 - 30 + 1) * TILE_SIZE, (14 - 10 + 1) * TILE_SIZE),
            'bottomTunnelWall': pygame.Rect(31 * TILE_SIZE, 25 * TILE_SIZE, (32 - 31 + 1) * TILE_SIZE, (28 - 25 + 1) * TILE_SIZE),
            'leftTunnelWall': pygame.Rect(21 * TILE_SIZE, 19 * TILE_SIZE, (26 - 21 + 1) * TILE_SIZE, (20 - 19 + 1) * TILE_SIZE),
            'leftUpperRectWall': pygame.Rect(19 * TILE_SIZE, 10 * TILE_SIZE, (26 - 19 + 1) * TILE_SIZE, (18 - 10 + 1) * TILE_SIZE),
            'rightUpperRectWall' : pygame.Rect(37 * TILE_SIZE, 16 * TILE_SIZE, (42 - 37 + 1) * TILE_SIZE, (18 - 16 + 1) * TILE_SIZE),
            'rightBottomRectWall': pygame.Rect(37 * TILE_SIZE, 21 * TILE_SIZE, (43 - 37 + 1) * TILE_SIZE, (24 - 21 + 1) * TILE_SIZE),
            'bottomTrapWall': pygame.Rect(25 * TILE_SIZE, 49 * TILE_SIZE, (30 - 25 + 1) * TILE_SIZE, (51 - 49 + 1) * TILE_SIZE),
            'rightMostWall': pygame.Rect(46 * TILE_SIZE, 32 * TILE_SIZE, (49 - 46 + 1) * TILE_SIZE, (38 - 32 + 1) * TILE_SIZE),
            'rightUpperWall': pygame.Rect(49 * TILE_SIZE, 6 * TILE_SIZE, (53 - 49 + 1) * TILE_SIZE, (8 - 6 + 1) * TILE_SIZE),
            'middleUpperWall': pygame.Rect(20 * TILE_SIZE, 1 * TILE_SIZE, (24 - 20 + 1) * TILE_SIZE, (6 - 1 + 1) * TILE_SIZE),
            'centerUpperWall': pygame.Rect(30 * TILE_SIZE, 7 * TILE_SIZE, (33 - 30 + 1) * TILE_SIZE, (10 - 7 + 1) * TILE_SIZE),
            'leftCenterWall': pygame.Rect(16 * TILE_SIZE, 25 * TILE_SIZE, (18 - 16 + 1) * TILE_SIZE, (27 - 25 + 1) * TILE_SIZE),
            'instantDeath': pygame.Rect(34 * TILE_SIZE, 34 * TILE_SIZE, (37 - 34 + 1) * TILE_SIZE, (35 - 34 + 1) * TILE_SIZE),
            'rightOfUpperRectWall': pygame.Rect(43 * TILE_SIZE, 10 * TILE_SIZE, (46 - 43 + 1) * TILE_SIZE, (16 - 10 + 1) * TILE_SIZE),
            'centerBottomWall' : pygame.Rect(28 * TILE_SIZE, 40 * TILE_SIZE, (31 - 28 + 1) * TILE_SIZE, (42 - 40 + 1) * TILE_SIZE),
            'exitClueEntry1' : pygame.Rect(15 * TILE_SIZE, 31 * TILE_SIZE, (17 - 15 + 1) * TILE_SIZE, (31 - 31 + 1) * TILE_SIZE),
            'exitClueExit1' : pygame.Rect(9 * TILE_SIZE, 28 * TILE_SIZE, (14 - 9 + 1) * TILE_SIZE, (31 - 28 + 1) * TILE_SIZE),
            'leftBottomWall' : pygame.Rect(1 * TILE_SIZE, 47 * TILE_SIZE, (4 - 1 + 1) * TILE_SIZE, (48 - 47 + 1) * TILE_SIZE),
            'exitClueEntry2' : pygame.Rect(13 * TILE_SIZE, 46 * TILE_SIZE, (15 - 13 + 1) * TILE_SIZE, (47 - 46 + 1) * TILE_SIZE),
            'exitClueExit2' : pygame.Rect(19 * TILE_SIZE, 50 * TILE_SIZE, (20 - 19 + 1) * TILE_SIZE, (52 - 50 + 1) * TILE_SIZE),
        }

        if rects['trueExit'].colliderect(self.player_rect):
            if not self.is_eligible:
                self.update_map(3, 15, 3, 20, 0)
                self.noEntry = True
            elif self.is_eligible:
                if self.exit_clue != [True, True, True]:
                    self.update_map(3, 15, 3, 20, 0)
                    self.noEntry = True
                else:
                    self.game_over = True

        else:
            self.update_map(3, 15, 3, 20, 2)
            self.noEntry = False

        self.reach_center = rects['centerRectWall1'].colliderect(self.player_rect)

        if rects['centerRectWall2'].colliderect(self.player_rect):
            self.update_map(27, 19, 27, 20, 0)
            self.update_map(31, 24, 32, 24, 0)
            self.is_eligible = True
        else:
            self.update_map(27, 19, 27, 20, 1)
            self.update_map(31, 24, 32, 24, 1)

        if rects['upperTunnelWall'].colliderect(self.player_rect):
            self.update_map(30, 10, 30, 14, 1)
        else:
            self.update_map(30, 10, 30, 14, 0)

        if rects['bottomTunnelWall'].colliderect(self.player_rect):
            self.update_map(31, 30, 32, 30, 0)
            self.update_map(31, 24, 32, 24, 0)
            self.is_trapped = True

        if rects['leftTunnelWall'].colliderect(self.player_rect):
            self.update_map(19, 19, 19, 20, 0)
            self.update_map(27, 19, 27, 20, 0)
            self.is_trapped = True

        if rects['leftUpperRectWall'].colliderect(self.player_rect):
            self.update_map(19, 10, 19, 11, 0)
            self.update_map(20, 18, 26, 18, 1)
        else:
            self.update_map(19, 10, 19, 11, 1)
            self.update_map(20, 18, 26, 18, 0)

        if rects['rightUpperRectWall'].colliderect(self.player_rect):
            self.update_map(37, 18, 42, 18, 1)
        else:
            self.update_map(37, 18, 42, 18, 0)

        if rects['rightBottomRectWall'].colliderect(self.player_rect):
            self.update_map(37, 21, 42, 21, 1)
        else:
            self.update_map(37, 21, 42, 21, 0)

        if rects['bottomTrapWall'].colliderect(self.player_rect):
            self.update_map(25, 47, 27, 47, 0)
            self.update_map(28, 53, 30, 53, 0)
            self.is_trapped = True

        if rects['rightMostWall'].colliderect(self.player_rect):
            self.update_map(46, 33, 46, 36, 0)
        else:
            self.update_map(46, 33, 46, 36, 1)

        if rects['rightUpperWall'].colliderect(self.player_rect):
            self.update_map(50, 6, 52, 6, 1)
            self.update_map(49, 7, 49, 8, 0)
        else:
            self.update_map(50, 6, 52, 6, 0)
            self.update_map(49, 7, 49, 8, 1)

        if rects['middleUpperWall'].colliderect(self.player_rect):
            self.update_map(21, 6, 24, 6, 1)
        else:
            self.update_map(21, 6, 24, 6, 0)

        if rects['centerUpperWall'].colliderect(self.player_rect):
            self.update_map(31, 9, 32, 9, 0)
        else:
            self.update_map(31, 9, 32, 9, 1)

        if rects['leftCenterWall'].colliderect(self.player_rect):
            self.update_map(16, 27, 18, 27, 1)
        else:
            self.update_map(16, 27, 18, 27, 0)

        if rects['instantDeath'].colliderect(self.player_rect):
            if not self.is_eligible:
                self.instantDeath = True
            elif self.is_eligible:
                self.exit_clue[2] = True
                self.instantDeath = False

        if rects['rightOfUpperRectWall'].colliderect(self.player_rect):
            self.update_map(43, 11, 43, 15, 1)
        else:
            self.update_map(43, 11, 43, 15, 0)

        if rects['centerBottomWall'].colliderect(self.player_rect):
            self.update_map(31, 40, 31, 41, 0)
        else:
            self.update_map(31, 40, 31, 41, 1)

        if rects['exitClueEntry1'].colliderect(self.player_rect):
            if self.is_eligible:
                self.update_map(15, 30, 15, 31, 1)
        else:
            self.update_map(15, 30, 15, 31, 0)

        if rects['exitClueExit1'].colliderect(self.player_rect):
            self.update_map(9, 30, 9, 31, 1)
            self.exit_clue[0] = True
        else:
            self.update_map(9, 30, 9, 31, 0)

        if rects['leftBottomWall'].colliderect(self.player_rect):
            self.update_map(1, 48, 4, 48, 1)
        else:
            self.update_map(1, 48, 4, 48, 0)

        if rects['exitClueEntry2'].colliderect(self.player_rect):
            if self.is_eligible:
                self.update_map(13, 47, 15, 47, 1)
                self.update_map(13, 48, 13, 48, 1)
        else:
            self.update_map(13, 47, 15, 47, 0)
            self.update_map(13, 48, 13, 48, 0)

        if rects['exitClueExit2'].colliderect(self.player_rect):
            self.update_map(20, 50, 20, 52, 1)
            self.exit_clue[1] = True
        else:
            self.update_map(20, 50, 20, 52, 0)

    def initialize_player(self):
        self.player_rect = self.player_image.get_rect(centerx=200, centery=HEIGHT - TILE_SIZE)

    def initialize_map(self):
        self.map_layout = self.load_map_from_csv(BASE_IMG_PATH + 'FinalMazeMap.csv')
        self.map_creation = [row[:] for row in self.map_layout]
        self.wall_rects = self.get_wall_rects()

    def reset_flags(self):
        self.is_trapped = False
        self.reach_center = False
        self.instantDeath = False
        self.is_eligible = False
        self.noEntry = False
        self.exit_clue = [False, False, False]
        self.game_over = False
        self.button_visible = False

    def restart_game(self):
        self.initialize_player()
        self.initialize_map()
        self.reset_flags()
        

    def show_msg(self, text):
        lines = text.split('\n')
        y_offset = HEIGHT // 2 - (len(lines) * FONT_SIZE + (len(lines) - 1) * LINE_SPACING) // 2
        for line in lines:
            message_surface = self.font.render(line, True, TEXT_COLOR)
            message_rect = message_surface.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(message_surface, message_rect)
            y_offset += FONT_SIZE + LINE_SPACING
    
    def game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.restart_button.is_clicked(event.pos):
                    if self.button_visible:
                        self.restart_game()

            self.movement_controller()
            self.screen.fill((255, 255, 255))
            self.draw_map()
            self.screen.blit(self.player_image, self.player_rect.topleft)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    GameTesting().game()
