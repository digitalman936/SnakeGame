import pygame
import sys

from snake import Snake
from fruit import Fruit
from board import Board
from stats import Statistic


class Main:

    def __init__(self):
        pygame.init()

        # Instances
        self.board = Board()
        self.fruit = Fruit(self.board)
        self.snake = Snake(self.board, self.fruit, 3)
        self.stats = Statistic(self.snake, self.board)

        self.game_over = False
        self.running = True

        self.title = "Tutorial Snake Game"

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.screen = pygame.display.set_mode((self.board.w, self.board.h))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

    def run_again(self):
        self.game_over = False

        while not self.game_over:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                    pygame.quit()
                    sys.exit()

            # Draw the prompt
            self.stats.display_final_stats(self.screen)

            # Update the screen
            pygame.display.flip()

            # Wait for user input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_n] or keys[pygame.K_ESCAPE]:
                self.game_over = True
            elif keys[pygame.K_y]:
                self.game_over = False

                self.fruit.__init__(self.board)
                self.fruit.spawn_fruit(self.screen)

                self.board = Board()
                self.snake = Snake(self.board, self.fruit, 3)
                self.stats = Statistic(self.snake, self.board)

                self.run_game()

        self.stats.clear_high_score()
        pygame.quit()

    def run_game(self):
        while not self.game_over:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()

                if event.type == pygame.QUIT:
                    self.game_over = True
                    break

                if keys[pygame.K_ESCAPE]:
                    self.game_over = True
                    break

            self.screen.fill(self.board.black)

            # Move snake
            self.snake.move_snake()

            if self.snake.handle_collision():
                self.game_over = True
                self.run_again()
                return

            if self.snake.eat_fruit():
                # Randomize the fruit position
                self.fruit.__init__(self.board)

                self.fruit.spawn_fruit(self.screen)

            # Generate the board, fruit, and update score snake
            self.board.draw_grid(self.screen)
            self.fruit.spawn_fruit(self.screen)
            self.snake.draw_snake(self.screen)

            # Create and load json file
            self.stats.save_high_score()
            self.stats.load_high_score()

            # Update and display score
            self.stats.display_score_stats(self.screen)
            self.stats.display_clock(self.screen)

            self.snake.handle_fruit_distance()

            pygame.display.flip()
            self.clock.tick(self.board.game_speed)

        self.stats.clear_high_score()
        pygame.quit()


if __name__ == '__main__':
    main = Main()

    main.run_game()
