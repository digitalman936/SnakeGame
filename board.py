import pygame


class Board:

    def __init__(self):
        self.w = 800
        self.h = 800
        self.block_size = 20
        self.game_speed = 25

        # Colors
        self.blue = (0, 0, 255)
        self.inner_blue = (0, 100, 255)
        self.green = (0, 255, 0)
        self.red = (200, 0, 0)
        self.black = (0, 0, 0)

        # Get window
        self.window_x = self.w
        self.window_y = self.h
        self.window_size = [self.window_x, self.window_y]

        # Calculate rows and columns based on window size and block_size
        self.board = [[0] * (self.w // self.block_size) for _ in range(self.h // self.block_size)]

        # Calculate number of blocks for x and y
        self.num_blocks_x = self.w // self.block_size
        self.num_blocks_y = self.h // self.block_size

        # Get number of blocks in window
        self.total_num_blocks = self.num_blocks_x * self.num_blocks_y

    def draw_grid(self, screen):
        for x in range(0, self.w, self.block_size):
            pygame.draw.line(screen, "black", (x, 0), (x, self.h))
        for y in range(0, self.h, self.block_size):
            pygame.draw.line(screen, "black", (0, y), (self.w, y))
