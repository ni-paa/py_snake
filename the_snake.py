"""Модуль the_snake.py реализует игру 'Змейка' с использованием библиотеки pg.
Игра включает основные элементы управления змейкой, отображение игрового поля,
счетчик очков и обработку столкновений.
Использование: Для запуска игры выполните этот файл python.
Особенности реализации:
*Управление змейкой осуществляется клавишами стрелок вверх-вниз-влево-вправо.
*Игровое поле ограничено рамками экрана.
*Если змея сталкивается сама с собой или с границами окна — игра заканчивается.
*После каждого съеденного яблока длина змеи увеличивается.
Автор: MbIcJIu
Версия: 1.0.
"""
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480  # Ширина и высота игрового окна
GRID_SIZE = 20  # Размер клетки в пикселях
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE  # Ширина сетки в клетках
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE  # Высота сетки в клетках

# Заранее вычислим центр окна и будем его вызывать
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)  # Вверх
DOWN = (0, 1)  # Вниз
LEFT = (-1, 0)  # Влево
RIGHT = (1, 0)  # Вправо

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)  # Цвет фона - черный
BORDER_COLOR = (93, 216, 228)  # Цвет границы ячейки
APPLE_COLOR = (255, 0, 0)  # Цвет яблока - красный
SNAKE_COLOR = (0, 255, 0)  # Цвет змейки - зеленый

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pg.time.Clock()  # Настройка времени для управления FPS
pg.display.set_caption('Змейка (v.0.1)')  # Заголовок окна


class GameObject:
    """Класс. Игровые объекты."""

    def __init__(self) -> None:
        """Инициализация значений по умолчанию."""
        self.position = CENTER
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    """Класс. Яблоко."""

    def __init__(self, positions_head=None):
        """Инициализация значений по умолчанию."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(positions_head)

    def draw(self):
        """Метода отрисовки яблочка."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, checking_occurrence):
        """Случайное положение яблока на игровом поле."""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if not checking_occurrence or self.position not in checking_occurrence:
                break


class Snake(GameObject):
    """Класс. Змейка."""

    def __init__(self):
        """Инициализация значений по умолчанию."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [CENTER]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.reset()

    def get_head_position(self):
        """Метод возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет положение."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки на основе текущего направления."""
        head_x, head_y = self.get_head_position()
        x_cord, y_cord = self.direction
        new_pos = ((head_x + (x_cord * GRID_SIZE)) % SCREEN_WIDTH,
                   (head_y + (y_cord * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)
        if len(self.positions) != self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовывает змейку."""
        rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        # Начальная позиция
        self.positions = [CENTER]
        self.last = None


def handle_keys(game_object):
    """Функция управления движением змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция запуска игры."""
    pg.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)  # Обработка перемещения
        snake.update_direction()  # Обновление позиции змейки
        snake.move()
        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif head_position in snake.positions[1:]:
            snake.reset()  # Сбрасываем игру
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()  # Отрисовка змейки
        apple.draw()
        pg.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
