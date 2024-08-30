import pygame

WIDTH, HEIGHT = 900, 900
FPS = 60
CHARACTER_SPEED = 5

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Box Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.MAIN_BODY = pygame.image.load('Assets/Box.png')
        self.main_body_rect = self.MAIN_BODY.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def draw_window(self):
        self.screen.fill("white")
        self.screen.blit(self.MAIN_BODY, self.main_body_rect.topleft)

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.main_body_rect.x -= CHARACTER_SPEED
        if keys[pygame.K_RIGHT]:
            self.main_body_rect.x += CHARACTER_SPEED
        if keys[pygame.K_UP]:
            self.main_body_rect.y -= CHARACTER_SPEED
        if keys[pygame.K_DOWN]:
            self.main_body_rect.y += CHARACTER_SPEED
        
        self.main_body_rect.x = max(0, min(WIDTH - self.main_body_rect.width, self.main_body_rect.x))
        self.main_body_rect.y = max(0, min(HEIGHT - self.main_body_rect.height, self.main_body_rect.y))

    def main(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_movement()
            self.draw_window()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    Game().main()
