import pygame

WIDTH, HEIGHT = 900, 900
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Box Adventure")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.MAIN_BODY = pygame.image.load('Assets/Box.png')

    def draw_window(self):
        self.screen.fill("white")
        self.screen.blit(self.MAIN_BODY, (200, 200))
        

    def main(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_window()
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    Game().main()

    