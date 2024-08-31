import pygame
import sys

# Initialize Pygame
pygame.init()

# Get the screen size from the system
screen_info = pygame.display.Info()
screen_width = 400
screen_height = 400

# Create the screen object
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Responsive Screen Example")
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            screen_width = event.w
            screen_height = event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw game elements here

    # Update the display
    pygame.display.flip()
