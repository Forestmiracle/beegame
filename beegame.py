import pygame
import random
from PIL import Image, ImageDraw

# Функции для создания изображений


def create_bee_image():
    # Создание изображения пчелы
    bee_image = Image.new("RGB", (40, 40), "yellow")
    draw = ImageDraw.Draw(bee_image)
    draw.ellipse([5, 5, 35, 35], fill="yellow", outline="black")  # Тело пчелы
    draw.line([20, 0, 20, 20], fill="black", width=2)  # Усики
    draw.line([0, 20, 40, 20], fill="black", width=2)  # Полоски на теле
    bee_image.save("bee.png")  # Сохранение изображения пчелы


def create_honey_pot_image():
    # Создание изображения горшка с медом
    honey_pot_image = Image.new("RGB", (30, 30), "brown")
    draw = ImageDraw.Draw(honey_pot_image)
    draw.rectangle([5, 5, 25, 25], fill="brown", outline="black")  # Горшок
    draw.ellipse([8, 8, 22, 22], fill="yellow", outline="black")  # Мед внутри
    honey_pot_image.save("honey_pot.png")  # Сохранение изображения горшка с медом


# Создание изображений пчелы и горшков с медом
create_bee_image()
create_honey_pot_image()

# Инициализация Pygame
pygame.init()

# Определение цветов
white = (255, 255, 255)
black = (0, 0, 0)

# Размеры дисплея
display_width = 800
display_height = 600

# Создание дисплея
game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Пчела собирает горшки")

# Загрузка спрайтов
bee_img = pygame.image.load("bee.png")
honey_pot_img = pygame.image.load("honey_pot.png")

# Скорость пчелы
bee_speed = 5


# Класс для пчелы
class Bee:
    def __init__(self):
        self.image = bee_img  # Изображение пчелы
        self.x = display_width * 0.5  # Начальная координата X
        self.y = display_height * 0.5  # Начальная координата Y
        self.move_x = 0  # Изменение координаты X
        self.move_y = 0  # Изменение координаты Y
        self.score = 0  # Начальный счет

    def move(self):
        # Обновление позиции пчелы
        self.x += self.move_x
        self.y += self.move_y
        # Ограничиваем движение пчелы в пределах экрана
        self.x = max(0, min(self.x, display_width - self.image.get_width()))
        self.y = max(0, min(self.y, display_height - self.image.get_height()))

    def draw(self):
        # Рисование пчелы на экране
        game_display.blit(self.image, (self.x, self.y))

    def update(self):
        # Обновление положения и рисование пчелы
        self.move()
        self.draw()


# Класс для горшков с медом
class HoneyPot:
    def __init__(self):
        self.image = honey_pot_img  # Изображение горшка с медом
        # Случайные начальные координаты горшка с медом
        self.x = random.randint(0, display_width - self.image.get_width())
        self.y = random.randint(0, display_height - self.image.get_height())

    def draw(self):
        # Рисование горшка с медом на экране
        game_display.blit(self.image, (self.x, self.y))


# Главная функция игры
def game_loop():
    bee = Bee()  # Создание объекта пчелы
    honey_pots = [HoneyPot() for _ in range(5)]  # Создание списка горшков с медом
    game_exit = False  # Переменная для выхода из игры

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True  # Выход из игры при закрытии окна
            if event.type == pygame.KEYDOWN:
                # Обработка нажатий клавиш для управления пчелой
                if event.key == pygame.K_LEFT:
                    bee.move_x = -bee_speed
                elif event.key == pygame.K_RIGHT:
                    bee.move_x = bee_speed
                elif event.key == pygame.K_UP:
                    bee.move_y = -bee_speed
                elif event.key == pygame.K_DOWN:
                    bee.move_y = bee_speed
            if event.type == pygame.KEYUP:
                # Остановка движения пчелы при отпускании клавиш
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    bee.move_x = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    bee.move_y = 0

        game_display.fill(white)  # Заполнение экрана белым цветом
        bee.update()  # Обновление положения пчелы и рисование

        for honey_pot in honey_pots:
            honey_pot.draw()  # Рисование горшков с медом
            # Проверка столкновения пчелы с горшком с медом
            if (
                bee.x < honey_pot.x + honey_pot.image.get_width()
                and bee.x + bee.image.get_width() > honey_pot.x
                and bee.y < honey_pot.y + honey_pot.image.get_height()
                and bee.y + bee.image.get_height() > honey_pot.y
            ):
                honey_pots.remove(honey_pot)  # Удаление собранного горшка с медом
                bee.score += 1  # Увеличение счета
                honey_pots.append(HoneyPot())  # Добавление нового горшка с медом

        # Отображение текущего счета на экране
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Очки: {bee.score}", True, black)
        game_display.blit(score_text, (10, 10))

        pygame.display.update()  # Обновление экрана

    pygame.quit()  # Завершение работы Pygame
    quit()  # Завершение скрипта


# Запуск игры
game_loop()
