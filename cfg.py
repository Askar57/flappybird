'''Конфигурационный файл'''


import os


# FPS
FPS = 60
# экран
SCREENWIDTH = 288
SCREENHEIGHT = 512
# Зазор между трубами
PIPE_GAP_SIZE = 200
# образ
BIRD_IMAGE_PATHS = {
    'red': {
     'up': os.path.join(os.getcwd(), 'images/redbird-upflap.png'),
     'mid': os.path.join(os.getcwd(), 'images/redbird-midflap.png'),
     'down': os.path.join(os.getcwd(), 'images/redbird-downflap.png')
    }
}
BACKGROUND_IMAGE_PATHS = {
    'day': os.path.join(os.getcwd(), 'images/background-day.png'),
    'night': os.path.join(os.getcwd(), 'images/background-night.png')
}
PIPE_IMAGE_PATHS = {
    'green': os.path.join(os.getcwd(), 'images/pipe-green.png'),
}
OTHER_IMAGE_PATHS = {
    'message': os.path.join(os.getcwd(), 'images/message.png'),
    'base': os.path.join(os.getcwd(), 'images/base.png')
}
# Аудио тракт
AUDIO_PATHS = {
    'die': os.path.join(os.getcwd(), 'sounds/die.mp3'),
    'hit': os.path.join(os.getcwd(), 'sounds/hit.mp3'),
    'point': os.path.join(os.getcwd(), 'sounds/point.mp3'),
    'swoosh': os.path.join(os.getcwd(), 'sounds/swoosh.mp3'),
    'wing': os.path.join(os.getcwd(), 'sounds/wing.mp3')
}
