from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 10  # 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для наследования"""

    position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
    body_color = (0, 0, 0)

    def __init__(self):
        self.position = GameObject.position
        self.body_color = GameObject.body_color

    def draw(self):
        """Заготовка метода отрисовки объекта на игровом поле"""

        pass


class Apple(GameObject):
    """Наследуемый класс описывающий яблоко и действия с ним"""

    body_color = (255, 0, 0)

    def __init__(self):
        self.body_color = Apple.body_color
        self.position = Apple.randomize_position(self)

    def randomize_position(self):
        """Метод задачи координат случайного положения яблока на поле"""

        return (
            randint(0, GRID_WIDTH) * GRID_SIZE,
            randint(0, GRID_HEIGHT) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод отрисовки яблока на игровом поле"""

        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Наследуемый класс описывающий змейку и действия с ней"""

    length = 1
    direction = RIGHT
    next_direction = None
    body_color = (0, 255, 0)

    def __init__(self):
        self.length = Snake.length
        self.direction = Snake.direction
        self.body_color = Snake.body_color
        self.last = None
        super().__init__()

    def update_direction(self):
        """Метод обновления движения змейки"""

        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращающий координаты головы змеи"""

        return self.position[0]

    def move(self, apple_position):
        """Метод задачи координат змейки на игровом поле"""

        head_now = self.get_head_position()
        if head_now[0] == SCREEN_WIDTH:
            head_then = (
                (head_now[0] + self.direction[0] * GRID_SIZE - SCREEN_WIDTH),
                (head_now[1] + self.direction[1] * GRID_SIZE),
            )
        elif head_now[1] == SCREEN_HEIGHT:
            head_then = (
                (head_now[0] + self.direction[0] * GRID_SIZE),
                (head_now[1] + self.direction[1] * GRID_SIZE - SCREEN_HEIGHT),
            )
        elif head_now[0] == 0:
            head_then = (
                (head_now[0] + self.direction[0] * GRID_SIZE + SCREEN_WIDTH),
                (head_now[1] + self.direction[1] * GRID_SIZE),
            )
        elif head_now[1] == 0:
            head_then = (
                (head_now[0] + self.direction[0] * GRID_SIZE),
                (head_now[1] + self.direction[1] * GRID_SIZE + SCREEN_HEIGHT),
            )
        else:
            head_then = (
                (head_now[0] + self.direction[0] * GRID_SIZE),
                (head_now[1] + self.direction[1] * GRID_SIZE),
            )

        # Проверка на столкновение
        if head_then in self.position:
            self.reset()
        # Перемещаем голову на новое место
        self.position.insert(0, head_then)

        # Проверяем не съела ли змея яблоко
        if head_then == apple_position:
            self.length += 1
            return True

        # Убираем след от хвоста
        if self.length < len(self.position):
            self.last = list.pop(self.position, -1)

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле"""

        for position in self.position[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)
        # Отрисовка головы змейки
        head = self.position[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сброса змейки при столкновении"""

        self.length = 1
        self.position = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция обработки нажатия клавиш"""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция основного цикла игры"""

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        if snake.move(apple.position):
            apple = Apple()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
