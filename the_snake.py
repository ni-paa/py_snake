from random import randint

import pygame

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
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
clock = pygame.time.Clock()  # Настройка времени для управления FPS
pygame.display.set_caption('Змейка (v.0.1)')  # Заголовок окна


class GameObject:
    """Класс. Игровые объекты"""

    def __init__(self) -> None:
        self.position = CENTER
        self.body_color = None

    def draw(self):
        """Инициализация пустого метода в классе, который будет
        переопределен в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс. Яблоко"""

    def __init__(self, snake_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake_positions)

    def draw(self):
        """Метода отрисовки яблочка"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, snake_positions):
        """Случайное положение яблока на игровом поле"""
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if not snake_positions or self.position not in snake_positions:
                break


class Snake(GameObject):
    """Класс. Змейка"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [CENTER]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Метод возвращает позицию головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Обновляет положение"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки на основе текущего направления"""
        head_pos = self.get_head_position()
        x, y = self.direction
        new_pos = ((head_pos[0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                   (head_pos[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        self.positions.insert(0, new_pos)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
            if self.last:
                last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        return True

    def draw(self):
        """Отрисовывает змейку"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        """Затирание последнего сегмента"""
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние"""
        self.length = 1
        # Начальная позиция
        self.positions = [CENTER]


def handle_keys(game_object):
    """Функция управления движением змейки"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
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
    """Основная функция запуска игры"""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)  # Обработка перемещения
        apple.draw()
        snake.update_direction()  # Обновление позиции змейки
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple(snake.positions)
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()  # Сбрасываем игру
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()  # Отрисовка змейки
        pygame.display.update()  # Обновление экрана


if __name__ == '__main__':
    main()
