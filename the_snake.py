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

# Цвета игры - крысный, зеленый, синий:
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Скорость движения змейки:
SPEED = 10  # 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Центр игрового поля
SCREEN_CENTER = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для наследования"""

    def __init__(self,
                 body_color_value=None,
                 position_value=SCREEN_CENTER,
                 foreground_color=BOARD_BACKGROUND_COLOR,
                 ) -> None:
        # Цвет объекта, поумолчанию не определён.
        self.body_color = body_color_value
        # Цвет бордера, поумолчанию FOREGOUND_COLOR.
        self.foreground_color = foreground_color
        # Позиция объекта, поумолчанию центральная точка экрана.
        self.position = position_value

    def draw(self):
        """Заготовка метода отрисовки объекта на игровом поле"""
        pass


class Apple(GameObject):
    """Наследуемый класс описывающий яблоко и действия с ним"""

    def __init__(self,
                 body_color_value=RED,
                 ) -> None:
        self.body_color = body_color_value
        self.position = Apple.randomize_position(self)

    def randomize_position(self):
        """Метод задачи координат случайного положения яблока на поле"""

        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод отрисовки яблока на игровом поле"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BLUE, rect, 1)


class Snake(GameObject):
    """Наследуемый класс описывающий змейку и действия с ней"""

    def __init__(self,
                 body_color_value=GREEN,
                 direction=RIGHT,
                 last=None,
                 length=1,
                 next_direction=None,
                 positions_value=SCREEN_CENTER,
                 foreground_color=None
                 ) -> None:
        super().__init__(foreground_color)
        self.body_color = body_color_value
        self.direction = direction
        self.last = last
        self.length = length
        self.next_direction = next_direction
        self.positions = positions_value

    def update_direction(self):
        """Метод обновления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращающий координаты головы змеи"""
        return self.positions[0]

    def move(self, apple_position):
        """Метод задачи координат змейки на игровом поле"""
        head_now = self.get_head_position()
        head_then = (
            (head_now[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_now[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Проверка на столкновение
        if head_then in self.positions:
            self.reset()
        # Перемещаем голову на новое место
        self.positions.insert(0, head_then)

        # Проверяем не съела ли змея яблоко
        if head_then == apple_position:
            self.length += 1
            return True

        # Убираем след от хвоста
        if self.length < len(self.positions):
            self.last = list.pop(self.positions, -1)

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, self.foreground_color, rect, 1)
        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, self.body_color, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сброса змейки при столкновении"""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
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
        # Если змея съела яблоко, то "кидаем" новое
        if snake.move(apple.position):
            apple.position = apple.randomize_position()
        # Если попали в змею, то "отскачило" в новое положение
        while apple.position in snake.positions:
            apple.position = apple.randomize_position()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
