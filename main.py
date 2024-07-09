import pygame
import sys
import os
from snake import Snake
from food import Food
from constants import *

# Initialize Pygame
pygame.init()

HIGH_SCORE_FILE = 'highscore.txt'
if not os.path.exists(HIGH_SCORE_FILE):
    with open(HIGH_SCORE_FILE, 'w') as f:
        f.write('0')

def get_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0
    
prev_score=get_high_score()
def show_game_over_screen(screen, score):
    font = pygame.font.Font(None, 36)
    text = font.render(f'Game Over! Score: {score}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    screen.blit(text, text_rect)

    # Determine if it's a high score
    current_high_score = prev_score
    is_high_score = score > current_high_score
    print(is_high_score)
    # Display high score message
    if is_high_score:
        high_score_text = font.render('New High Score!', True, (255, 255, 255))
        high_score_rect = high_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 90))
        screen.blit(high_score_text, high_score_rect)

    # Display restart and exit options
    font = pygame.font.Font(None, 24)
    restart_text = font.render('Press R to Restart', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
    screen.blit(restart_text, restart_rect)

    exit_text = font.render('Press ESC to Exit', True, (255, 255, 255))
    exit_rect = exit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
    screen.blit(exit_text, exit_rect)

    pygame.display.flip()


# Function to update and save high score
def update_high_score(score):
    with open(HIGH_SCORE_FILE, 'r') as f:
        current_high_score = int(f.read())

    if score > current_high_score:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
    pygame.display.set_caption('Snake Game')

    snake = Snake()
    food = Food()

    while True:
        snake.handle_keys()
        snake.move()

        # Check for collisions
        if snake.get_head_position() in snake.get_body_positions():
            # print("Collision Detected!")
            update_high_score(snake.length - 1)
            show_game_over_screen(screen, snake.length - 1)
            
            # Wait for 10 seconds or until user input
            start_time = pygame.time.get_ticks()
            waiting = True
            while waiting:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - start_time
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Restart game
                            snake.reset()
                            waiting = False  # Exit the loop
                        elif event.key == pygame.K_ESCAPE:  # Exit game
                            pygame.quit()
                            sys.exit()

                # Check if 10 seconds have passed
                if elapsed_time >= 10000:  # 10000 milliseconds = 10 seconds
                    waiting = False

            # Optional: Clear any remaining events in the queue
            pygame.event.clear()



        if snake.collision_with_food(food.position):
            food.randomize_position()

        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        food.draw(screen)
        pygame.display.update()

        # Adjust game speed
        clock.tick(FPS)

# Run the game
if __name__ == '__main__':
    main()
