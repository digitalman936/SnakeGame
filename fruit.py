import pygame
import random


class Fruit:

    def __init__(self, board):
        self.board = board

        self.fruit_size = board.block_size

        self.x = random.randint(0, self.board.w // self.fruit_size - 1) * self.fruit_size
        self.y = random.randint(0, self.board.h // self.fruit_size - 1) * self.fruit_size
        self.position = (self.x, self.y)

    def spawn_fruit(self, screen):
        x, y = self.position

        # Draw the new fruit
        pygame.draw.rect(screen, self.board.red,
                         [self.x, self.y, self.fruit_size, self.fruit_size])

        self.position = (x, y)
