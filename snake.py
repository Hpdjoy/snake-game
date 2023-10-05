import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize the clock
clock = pygame.time.Clock()

# Initialize the Snake
snake = [(5, 5)]
snake_direction = (1, 0)  # Start moving to the right

# Initialize the Food
food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

# Game over flag
game_over = False

# Menu variables
in_menu = True
selected_speed = "Medium"
speeds = ["Slow", "Medium", "Fast"]
selected_option = "Start"

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if in_menu:
                if event.key == pygame.K_UP:
                    selected_speed = speeds[(speeds.index(selected_speed) - 1) % len(speeds)]
                elif event.key == pygame.K_DOWN:
                    selected_speed = speeds[(speeds.index(selected_speed) + 1) % len(speeds)]
                elif event.key == pygame.K_RETURN:
                    if selected_option == "Start":
                        in_menu = False
                        clock.tick({"Slow": 5, "Medium": 10, "Fast": 15}[selected_speed])
                        snake = [(5, 5)]
                        snake_direction = (1, 0)
                        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                        game_over = False
                    elif selected_option == "Exit":
                        game_over = True

            else:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

    # Move the Snake
    new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
    snake.insert(0, new_head)

    # Check for collisions
    if snake[0] == food:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    else:
        snake.pop()

    # Check for game over conditions
    if (
        snake[0][0] < 0
        or snake[0][0] >= GRID_WIDTH
        or snake[0][1] < 0
        or snake[0][1] >= GRID_HEIGHT
        or snake[0] in snake[1:]
    ):
        in_menu = True
        selected_option = "Restart"
        game_over = True

    # Clear the screen
    screen.fill(BLACK)

    # Draw the Snake
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Draw the Food
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    if in_menu:
        # Display menu options and selected speed
        font = pygame.font.Font(None, 36)
        text = font.render("Snake Game", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - 100, 100))

        option_text = [f"Speed: {selected_speed}"]
        option_text.extend([f"> {option}" if option == selected_option else option for option in ["Start", "Exit"]])

        for i, opt in enumerate(option_text):
            text = font.render(opt, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - 100, 200 + i * 50))

    pygame.display.update()

# Quit Pygame
pygame.quit()
