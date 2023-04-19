import json
import pygame
import os


class Statistic:

    def __init__(self, snake, board):
        # Instances
        self.snake = snake
        self.board = board

        self.font = pygame.font.Font('freesansbold.ttf', 30)

        self.game_score = self.snake.score

        # Load high score from file
        self.high_score = self.load_high_score()

        # Gets stats and json path
        self.stats_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stats'))
        self.file_path = os.path.join(self.stats_dir, "score_stats.json")

        # Clock
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    def display_score_stats(self, screen):
        self.game_score = self.snake.return_score()

        # Update high score if necessary
        if self.game_score > self.high_score:
            self.high_score = self.game_score

        # Display score realtime
        score_surface = self.font.render(f"Score: {self.game_score}", True, "blue")
        score_rect = score_surface.get_rect()
        score_rect.topleft = (10, 10)
        screen.blit(score_surface, score_rect)

        # Display high score realtime
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, "red")
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.topright = (screen.get_width() - 10, 10)
        screen.blit(high_score_surface, high_score_rect)

        return self.game_score, self.high_score

    def display_final_stats(self, screen):
        screen.fill(self.board.black)

        # Display score
        score_surface = self.font.render(f"Score: {self.game_score}", True, self.board.blue)
        score_rect = score_surface.get_rect()
        score_rect.centerx = self.board.w // 2 + 90
        score_rect.centery = self.board.h // 2
        screen.blit(score_surface, score_rect)

        # Display high score
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, self.board.red)
        high_score_rect = high_score_surface.get_rect()
        high_score_rect.centerx = self.board.w // 2 - 90
        high_score_rect.centery = self.board.h // 2
        screen.blit(high_score_surface, high_score_rect)

        # Prompt user
        prompt_surface = self.font.render("Do you want to play again Y/N?", True, "orange")
        prompt_rect = prompt_surface.get_rect()
        prompt_rect.centerx = self.board.w // 2
        prompt_rect.centery = self.board.h // 2 + 50
        screen.blit(prompt_surface, prompt_rect)

    def display_clock(self, screen):
        # Calculate elapsed time in milliseconds
        elapsed_time = pygame.time.get_ticks() - self.start_time

        seconds = int((elapsed_time % 60000) / 1000)
        minutes = int(elapsed_time / 60000)
        hours = int(elapsed_time / 3600000)

        clock_text = f'Time: {hours:02d}:{minutes:02d}:{seconds:02d}'

        # Display the clock
        clock_surface = self.font.render(clock_text, True, 'orange')
        clock_rect = clock_surface.get_rect()
        clock_rect.topright = (self.board.w - 10 - clock_rect.width, 10)
        screen.blit(clock_surface, clock_rect)

    def save_high_score(self):
        self.stats_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stats'))
        self.file_path = os.path.join(self.stats_dir, "score_stats.json")

        if not os.path.exists(self.stats_dir):
            os.makedirs(self.stats_dir)

        high_score = self.load_high_score()

        # Update the high score if the new score is higher
        if self.high_score > high_score:
            high_score = self.high_score

            # Write the updated high score to the file
            with open(self.file_path, "w") as f:
                json.dump(high_score, f)

        return high_score

    def load_high_score(self):
        self.stats_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stats'))
        self.file_path = os.path.join(self.stats_dir, "score_stats.json")

        # Read the current high score from the file
        try:
            with open(self.file_path, "r") as f:
                high_score = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            high_score = 0

        return high_score

    def clear_high_score(self):
        self.stats_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'stats'))
        self.file_path = os.path.join(self.stats_dir, "score_stats.json")

        if os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                f.write('0')
