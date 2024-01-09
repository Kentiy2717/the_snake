from random import choice, randint

import pygame as pg
import sys

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
SPEED = 5  # 20 было. Будет возрастать в ходе игры.

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Центр игрового поля
SCREEN_CENTER = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка -лучшая игра! Для выхода жми "X" или "Esc"')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для наследования"""

    def __init__(self,
                 body_color_value=None,
                 position_value=SCREEN_CENTER,
                 foreground_color=BOARD_BACKGROUND_COLOR
                 ) -> None:
        # Цвет объекта, поумолчанию не определён.
        self.body_color = body_color_value
        # Цвет бордера, поумолчанию FOREGOUND_COLOR.
        self.foreground_color = foreground_color
        # Позиция объекта, поумолчанию центральная точка экрана.
        self.position = position_value

    def draw(
            self,
            surface,
            position_value,
            body_color_value,
            foreground_color_value):
        """Заготовка метода отрисовки объекта на игровом поле"""
        rect = pg.Rect(
            (position_value[0], position_value[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pg.draw.rect(surface, body_color_value, rect)
        pg.draw.rect(surface, foreground_color_value, rect, 1)


class Apple(GameObject):
    """Наследуемый класс описывающий яблоко и действия с ним"""

    def __init__(self, snake_positions=SCREEN_CENTER) -> None:
        self.body_color = RED
        self.snake_positions = snake_positions
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод задачи координат случайного положения яблока на поле"""
        # Не понял что значит "Вместо возврата лучше изменить поля."
        # Я все-таки лучше бы проверку тоже в main делал.
        # Не понимаю зачем позицию змейки в яблоко тащить.
        apple_position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

        while apple_position in self.snake_positions:
            print('Попал в змею')
            clock.tick(0.5)
            apple_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
        return apple_position

    def draw(self, surface):
        """Метод отрисовки яблока на игровом поле"""
        GameObject.draw(self, surface, self.position, self.body_color, BLUE)


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

    def move(self, snake_eat_apple=False):
        """Метод задачи координат змейки на игровом поле"""
        head_now = self.get_head_position()
        head_then = (
            (head_now[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_now[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )

        # Перемещаем голову на новое место
        self.positions.insert(0, head_then)

        # Убираем след от хвоста
        if not snake_eat_apple:
            self.last = list.pop(self.positions, -1)

    def draw(self, surface):
        """Метод отрисовки змейки на игровом поле"""
        for position in self.positions[:-1]:
            GameObject.draw(self, surface, position,
                            self.body_color, self.foreground_color)
        # Отрисовка головы змейки
        GameObject.draw(self, surface, self.get_head_position(),
                        self.body_color, self.body_color)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Метод сброса змейки при столкновении"""
        # Совсем не понял как я должен 165-167 заменить на конструктор.
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        # 167 вообще нельзя на конструктор менять.
        # В задании начальное движение это RIGHT.
        # А после выигрыша/проирыша рандобное.
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        # Что значит "нужно менять поля, а не рисовать"?
        # Мне поле же надо черным сделать, чтобы закрасить прошлое.
        # Потом на черном поле уже заново отрисуется змейка и яблоко.
        screen.fill(BOARD_BACKGROUND_COLOR)
        global SPEED
        SPEED = 5


def handle_keys(game_object):
    """Функция обработки нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                sys.exit()


def main():
    """Функция основного цикла игры"""
    # Инициализация pg:
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        global SPEED
        clock.tick(SPEED)

        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение. Выводим "экран лузера"
        for _ in range(1, len(snake.positions)):
            if snake.positions[0] == snake.positions[_]:
                car_surf = pg.image.load("game-over.jpg")
                car_rect = car_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                )
                screen.blit(car_surf, car_rect)
                pg.display.update()
                clock.tick(0.5)
                snake.reset()
                break

        # Если змея съела яблоко:
        if snake.positions[0] == apple.position:
            # "удлиняем" змею
            snake.move(True)
            # "кидаем" новое яблоко.
            apple.position = apple.randomize_position()
            # Я бы оставил так как ниже. Зачем делать эту проверку в apple?
            # Проверяем не попали ли в змею. Если попали, то куда "отскочило".
            # while apple.position in snake.positions:
            #     apple.position = apple.randomize_position()
            # Увеличиваем скорость.
            SPEED += 1
        # проверяем на выигрышь и выводим "экран победителя"
        if SPEED == 30:
            car_surf = pg.image.load("win.jpg")
            car_rect = car_surf.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            screen.blit(car_surf, car_rect)
            pg.display.update()
            clock.tick(0.5)
            snake.reset()
        apple.draw(screen)
        snake.draw(screen)
        pg.display.update()


if __name__ == "__main__":
    main()
