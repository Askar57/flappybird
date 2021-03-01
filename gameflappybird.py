import cfg
import sys
import random
import pygame
import itertools

'''Инициализация игры'''


def initGame():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((cfg.SCREENWIDTH, cfg.SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bird by Askar57')
    return screen


'''Показать текущий счет'''


def showScore(screen, score, number_images):
    digits = list(str(int(score)))
    width = 0
    for d in digits:
        width += number_images.get(d).get_width()
    offset = (cfg.SCREENWIDTH - width) / 2
    for d in digits:
        screen.blit(number_images.get(d), (offset, cfg.SCREENHEIGHT * 0.1))
        offset += number_images.get(d).get_width()


'''Основная функция'''


def main():
    screen = initGame()
    # Загрузим необходимые игровые ресурсы
    # Импорт цифровых изображений
    number_images = dict()
    for key, value in cfg.NUMBER_IMAGE_PATHS.items():
        number_images[key] = pygame.image.load(value).convert_alpha()
    # Импорт аудио
    sounds = dict()
    for key, sound in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(sound)
    # Труба
    pipe_images = dict()
    pipe_sprites = pygame.sprite.Group()

    pipe_images['bottom'] = pygame.image.load(random.choice
                                              (list
                                               (cfg.PIPE_IMAGE_PATHS.values())
                                               )).convert_alpha()
    pipe_images['top'] = pygame.transform.rotate(pipe_images['bottom'], 180)
    for i in range(2):
        pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
        pipe_sprites.add(Pipe(image=pipe_images.get('top'),
                              position=(cfg.SCREENWIDTH + 200 + i * cfg.SCREENWIDTH / 2,
                                        pipe_pos.get('top')[-1])))
        pipe_sprites.add(Pipe(image=pipe_images.get('bottom'),
                              position=(cfg.SCREENWIDTH + 200 + i * cfg.SCREENWIDTH / 2,
                                        pipe_pos.get('bottom')[-1])))
    # Картинки птиц
    bird_images = dict()
    for key, image_bird in cfg.BIRD_IMAGE_PATHS[random.choice(list(cfg.BIRD_IMAGE_PATHS.keys()))].items():
        bird_images[key] = pygame.image.load(image_bird).convert_alpha()
    # Фоновое изображение
    bg_image = pygame.image.load(random.choice
                                 (list
                                  (cfg.BACKGROUND_IMAGE_PATHS.values())
                                  )).convert_alpha()
    # Другие картинки
    other_images = dict()
    for key, image_bg in cfg.OTHER_IMAGE_PATHS.items():
        other_images[key] = pygame.image.load(image_bg).convert_alpha()
    # Интерфейс запуска игры
    game_start = startGame(screen, sounds, bird_images,
                           other_images, bg_image, cfg)
    # Войти в основную игру
    score = 0
    bird_pos, base_pos, bird_idd = list(game_start.values())
    base_bg_width = other_images['base'].get_width() - bg_image.get_width()
    clock = pygame.time.Clock()
    # класс птички
    bird = Bird(images=bird_images, idd=bird_idd, pos=bird_pos)
    # Увеличивать трубу
    add_pipe = True
    # Идет ли игра
    is_running = True
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                             and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.setFlapped()
                    sounds['wing'].play()
        # Проверка удара
        for pipe in pipe_sprites:
            if pygame.sprite.collide_mask(bird, pipe):
                is_running = False
                sounds['hit'].play()
        # Обновить птичку
        boundary_values = [0, base_pos[-1]]
        is_dead = bird.update(boundary_values, float(clock.tick(cfg.FPS)) / 1000)
        if is_dead:
            is_running = False
            sounds['hit'].play()
            sounds['die'].play()
        # Перемещение травы, для того чтобы добиться эффекта полета птицы
        base_pos[0] = -((-base_pos[0] + 4) % base_bg_width)
        # Перемещение трубы, для того чтобы добиться эффекта летящей вперед птицы
        key = False
        for pipe in pipe_sprites:
            pipe.rect.left -= 4
            if pipe.rect.centerx < bird.rect.centerx and not pipe.used_for_score:
                pipe.used_for_score = True
                score += 0.5
                if '.5' in str(score):
                    sounds['point'].play()
            if 5 > pipe.rect.left > 0 and add_pipe:
                pipe_pos = Pipe.randomPipe(cfg, pipe_images.get('top'))
                pipe_sprites.add(Pipe(image=pipe_images.get('top'),
                                      position=pipe_pos.get('top')))
                pipe_sprites.add(Pipe(image=pipe_images.get('bottom'),
                                      position=pipe_pos.get('bottom')))
                add_pipe = False
            elif pipe.rect.right < 0:
                pipe_sprites.remove(pipe)
                key = True
        if key:
            add_pipe = True
        # Привязать необходимые элементы на экране
        screen.blit(bg_image, (0, 0))
        pipe_sprites.draw(screen)
        showScore(screen, score, number_images)
        screen.blit(other_images['base'], base_pos)
        bird.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)
    endGame(screen, showScore, score, number_images,
            bird, pipe_sprites, bg_image, other_images,
            base_pos, cfg)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


'''Начальный экран'''


def startGame(screen, sounds, bird_images, other_images, bg_image, cfg):
    clock = pygame.time.Clock()
    shift = 1
    base_pos = [0, cfg.SCREENHEIGHT * 0.79]
    base_bg = other_images['base'].get_width() - bg_image.get_width()
    msg_pos = [(cfg.SCREENWIDTH - other_images['message'].get_width()) / 2, cfg.SCREENHEIGHT * 0.12]
    bird_id = 0
    bird_id_change_count = 0
    bird_id_cycle = itertools.cycle([0, 1, 2, 1])
    bird_pos = [cfg.SCREENWIDTH * 0.2, (cfg.SCREENHEIGHT - list(bird_images.values())[0].get_height()) / 2]
    bird_y_count = 0
    bird_y_max = 9
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    return {'bird_pos': bird_pos, 'base_pos': base_pos, 'bird_id': bird_id}
                sounds['wing'].play()
        bird_id_change_count += 1
        if bird_id_change_count % 5 == 0:
            bird_id = next(bird_id_cycle)
            bird_id_change_count = 0
        base_pos[0] = -((-base_pos[0] + 4) % base_bg)
        bird_y_count += 1
        if bird_y_count == bird_y_max:
            bird_y_max = 16
            shift = -1 * shift
            bird_y_count = 0
        bird_pos[-1] = bird_pos[-1] + shift
        screen.blit(bg_image, (0, 0))
        screen.blit(list(bird_images.values())[bird_id], bird_pos)
        screen.blit(other_images['message'], msg_pos)
        screen.blit(other_images['base'], base_pos)
        pygame.display.update()
        clock.tick(cfg.FPS)


'''Интерфейс конца игры'''


def endGame(screen, showScore, score, number_images,
            bird, pipe_sprites, bg_image, other_images,
            base_pos, cfg):
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    return
        boundary_values = [0, base_pos[-1]]
        bird.update(boundary_values, float(clock.tick(cfg.FPS)) / 1000.)
        screen.blit(bg_image, (0, 0))
        pipe_sprites.draw(screen)
        screen.blit(other_images['base'], base_pos)
        showScore(screen, score, number_images)
        bird.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)


'''Труба'''


class Pipe(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = position
        self.used_for_score = False

    @staticmethod
    def randomPipe(cfg, image):
        base_y = 0.79 * cfg.SCREENHEIGHT
        rand_pipe_y = int(base_y * 0.2) + random.randrange(0, int(base_y * 0.6 - cfg.PIPE_GAP_SIZE))
        return {'top': (cfg.SCREENWIDTH + 10, rand_pipe_y - image.get_height()),
                'bottom': (cfg.SCREENWIDTH + 10, rand_pipe_y + cfg.PIPE_GAP_SIZE)}


'''Класс птички'''


class Bird(pygame.sprite.Sprite):
    def __init__(self, images, idd, pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = images
        self.image = list(images.values())[idd]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = pos
        # Переменные, необходимые для вертикального перемещения
        self.is_flapped = False
        self.min_height = 0
        self.max_height = 10
        # Сменить форму птицы
        self.bird_id = id
        self.bird_id_cycle = itertools.cycle([0, 1, 2, 1])
        self.bird_id_count = 0

    '''Обновить'''

    def update(self, boundary_values, pass_time):
        # Обновление положения по вертикали
        if self.is_flapped:
            self.max_height -= 60 * pass_time
            self.rect.top -= self.max_height
            if self.max_height <= 0:
                self.unsetFlapped()
                self.min_height = 0
                self.max_height = 10
        else:
            self.min_height += 40 * pass_time
            self.rect.bottom += self.min_height
        # Определить, разбилась ли птица из-за того,
        # что она попала в верхнюю и нижнюю границы
        is_dead = False
        if self.rect.bottom > boundary_values[1]:
            is_dead = True
            self.max_height = 0
            self.min_height = 0
            self.rect.bottom = boundary_values[1]
        if self.rect.top < boundary_values[0]:
            is_dead = True
            self.max_height = 0
            self.min_height = 0
            self.rect.top = boundary_values[0]
        # Включите симуляцию формы птицы, чтобы имитировать эффект крыльев вентилятора
        self.bird_id_count += 1
        if self.bird_id_count % 5 == 0:
            self.bird_id = next(self.bird_id_cycle)
            self.image = list(self.images.values())[self.bird_id]
            self.bird_id_count = 0
        return is_dead

    '''Установить в "режим полета"'''

    def setFlapped(self):
        if self.is_flapped:
            self.max_height = max(12, self.max_height + 1)
        else:
            self.is_flapped = True

    '''Установить в "режим сброса"'''

    def unsetFlapped(self):
        self.is_flapped = False

    '''Привязка к экрану'''

    def draw(self, screen):
        screen.blit(self.image, self.rect)


'''летс гоу XDD'''
if __name__ == '__main__':
    while True:
        main()
