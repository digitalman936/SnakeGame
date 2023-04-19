import pygame
from enum import Enum
import math


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class Snake:

    def __init__(self, board, fruit, snake_length=3):
        # Instances
        self.board = board
        self.fruit = fruit

        # Snake Attributes
        self.snake_block_size = board.block_size

        # Game State
        x = (self.board.num_blocks_x // 2) * self.snake_block_size
        y = (self.board.num_blocks_y // 2) * self.snake_block_size

        self.snake_head = (x, y)
        self.snake_body = [(x - i * self.snake_block_size, y) for i in range(1, snake_length + 1)]

        self.direction = Direction.RIGHT

        self.score = 0

    def draw_snake(self, screen):
        if self.score < 10:
            # Draw the snake head in green
            pygame.draw.rect(screen, "yellow",
                             [self.snake_head[0], self.snake_head[1], self.snake_block_size, self.snake_block_size])

        elif 10 <= self.score < 20:
            # Draw the snake head in green
            pygame.draw.rect(screen, "orange",
                             [self.snake_head[0], self.snake_head[1], self.snake_block_size, self.snake_block_size])

        else:
            # Draw the snake head in green
            pygame.draw.rect(screen, "red",
                             [self.snake_head[0], self.snake_head[1], self.snake_block_size, self.snake_block_size])

        # Draw the rest of the snake body in blue
        for i, x in enumerate(self.snake_body):
            if i == 0:
                continue

            # Draws a blue rectangle for each block size
            pygame.draw.rect(screen, self.board.blue, [x[0], x[1], self.snake_block_size, self.snake_block_size])

            # Calculates an inner rectangle for each block size in the list based on the offset
            inner_rect_size = self.snake_block_size * 0.5
            inner_rect_offset = (self.snake_block_size - inner_rect_size) // 2  # EXAMPLE: 50 - 40 / 2 = 5 (5 pixel difference)
            inner_rect = [x[0] + inner_rect_offset, x[1] + inner_rect_offset, inner_rect_size, inner_rect_size]
            pygame.draw.rect(screen, self.board.inner_blue, inner_rect)

    def move_snake(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.direction = Direction.LEFT
        elif keys[pygame.K_d]:
            self.direction = Direction.RIGHT
        elif keys[pygame.K_w]:
            self.direction = Direction.UP
        elif keys[pygame.K_s]:
            self.direction = Direction.DOWN

        x, y = self.snake_head
        if self.direction == Direction.RIGHT:
            x += self.snake_block_size
        elif self.direction == Direction.LEFT:
            x -= self.snake_block_size
        elif self.direction == Direction.DOWN:
            y += self.snake_block_size
        elif self.direction == Direction.UP:
            y -= self.snake_block_size

        self.snake_head = (x, y)

        self.snake_body.insert(0, self.snake_head)
        self.snake_body.pop()

    def handle_collision(self):
        head_x, head_y = self.snake_head

        # Hits window boundary
        if head_x < 0 or head_x >= self.board.w or head_y < 0 or head_y >= self.board.h:
            return True

        # Hits itself
        if self.snake_head in self.snake_body[1:]:
            return True

        return False

    def handle_border_distance(self):
        head_x, head_y = self.snake_head

        # Get the distance between the head and window borders
        right_border = self.board.w - head_x - self.snake_block_size
        left_border = head_x
        top_border = head_y
        bottom_border = self.board.h - head_y - self.snake_block_size

        # Stores border distances
        border_distances = [
            right_border, left_border, top_border, bottom_border
        ]

        return border_distances[0], border_distances[1], border_distances[2], border_distances[3]

    def handle_fruit_distance(self):
        fruit_x, fruit_y = self.fruit.position
        head_x, head_y = self.snake_head
        fruit_distance = math.sqrt((fruit_x - head_x) ** 2 + (fruit_y - head_y) ** 2)

        return fruit_distance

    def eat_fruit(self):
        if self.snake_head == self.fruit.position or self.snake_body == self.fruit.position:
            self.snake_body.append(self.snake_body[-1])

            self.score += 1

            return True, self.score

        return False

    def return_score(self):
        return self.score
