import pygame
from pygame import Vector2
from random import randrange


TILE_SIZE = 48

WIDTH = 16 * TILE_SIZE
HEIGHT = 16 * TILE_SIZE

win = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.Surface(win.get_size())
for y in range(16):
    for x in range(16):
        pygame.draw.rect(
            bg,
            "#c0cbdc" if y % 2 == x % 2 else "#8b9bb4",
            (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        )


class Snake:
    def __init__(self, x: int, y: int) -> None:
        self.direction: Vector2 = Vector2(0, 0)
        self.grow = False
        self.body: list[Vector2] = [
            Vector2(x, y),
            Vector2(0, 0),
            Vector2(0, 0),
            Vector2(0, 0),
        ]

    def move(self) -> None:
        head = self.body[0] + self.direction
        if head.x >= 16:
            head.x = 0
        if head.y >= 16:
            head.y = 0
        if head.x < 0:
            head.x = 15
        if head.y < 0:
            head.y = 15
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1].copy()
        self.body[0] = head

    def draw(self, surf: pygame.Surface) -> None:
        for p in self.body:
            pygame.draw.rect(surf, "#63c74d", (p * TILE_SIZE, (TILE_SIZE, TILE_SIZE)))

    def collides(self, pos: Vector2, ignore_head: bool = False) -> bool:
        return any([pos == i for i in self.body[int(ignore_head):]])


class Apple:
    def __init__(self) -> None:
        self.pos = Vector2(randrange(0, 16), randrange(0, 16))

    def draw(self, surf: pygame.Surface) -> None:
        pygame.draw.rect(
            surf, "#ff0044", (self.pos * TILE_SIZE, (TILE_SIZE, TILE_SIZE))
        )


clock = pygame.time.Clock()
time = 0
snake = Snake(8, 8)
apple = Apple()
new_direction = Vector2(0, 0)




def draw():
    win.blit(bg, (0, 0))
    apple.draw(win)
    snake.draw(win)
    pygame.display.flip()


draw()
while True:
    dt = clock.tick(60) / 1000

    time += dt

    if time > 0.2:
        time -= 0.2
        snake.direction = new_direction
        
        if snake.body[0] == apple.pos:
            while snake.collides(apple.pos):
                apple = Apple()
            snake.body.append(snake.body[-1].copy())
        snake.move()
        if snake.collides(snake.body[0], True):
            snake.body=[Vector2(8, 8)]
       
        draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w) and snake.direction.y != 1:
                new_direction = Vector2(0, -1)
            if event.key in (pygame.K_DOWN, pygame.K_s) and snake.direction.y != -1:
                new_direction = Vector2(0, 1)
            if event.key in (pygame.K_LEFT, pygame.K_a) and snake.direction.x != 1:
                new_direction = Vector2(-1, 0)
            if event.key in (pygame.K_RIGHT, pygame.K_d) and snake.direction.x != -1:
                new_direction = Vector2(1, 0)
