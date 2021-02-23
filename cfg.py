"""Конфигурационный файл"""


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
    },
    'blue': {
        'up': os.path.join(os.getcwd(), 'images/bluebird-upflap.png'),
        'mid': os.path.join(os.getcwd(), 'images/bluebird-midflap.png'),
        'down': os.path.join(os.getcwd(), 'images/bluebird-downflap.png')
    },
    'yellow': {
        'up': os.path.join(os.getcwd(), 'images/yellowbird-upflap.png'),
        'mid': os.path.join(os.getcwd(), 'images/yellowbird-midflap.png'),
        'down': os.path.join(os.getcwd(), 'images/yellowbird-downflap.png')
    }

}
NUMBER_IMAGE_PATHS = {
    '0': os.path.join(os.getcwd(), 'images/0.png'),
    '1': os.path.join(os.getcwd(), 'images/1.png'),
    '2': os.path.join(os.getcwd(), 'images/2.png'),
    '3': os.path.join(os.getcwd(), 'images/3.png'),
    '4': os.path.join(os.getcwd(), 'images/4.png'),
    '5': os.path.join(os.getcwd(), 'images/5.png'),
    '6': os.path.join(os.getcwd(), 'images/6.png'),
    '7': os.path.join(os.getcwd(), 'images/7.png'),
    '8': os.path.join(os.getcwd(), 'images/8.png'),
    '9': os.path.join(os.getcwd(), 'images/9.png')
}
BACKGROUND_IMAGE_PATHS = {
    'day': os.path.join(os.getcwd(), 'images/background-day.png'),
    'night': os.path.join(os.getcwd(), 'images/background-night.png')
}
PIPE_IMAGE_PATHS = {
    'green': os.path.join(os.getcwd(), 'images/pipe-green.png'),
    'red': os.path.join(os.getcwd(), 'images/pipe-red.png')

}
OTHER_IMAGE_PATHS = {
    'message': os.path.join(os.getcwd(), 'images/message.png'),
    'base': os.path.join(os.getcwd(), 'images/base.png'),
    'gameover': os.path.join(os.getcwd(), 'images/gameover.png'),

}
# Аудио тракт
AUDIO_PATHS = {
    'die': os.path.join(os.getcwd(), 'sounds/die.mp3'),
    'hit': os.path.join(os.getcwd(), 'sounds/hit.mp3'),
    'point': os.path.join(os.getcwd(), 'sounds/point.mp3'),
    'swoosh': os.path.join(os.getcwd(), 'sounds/swoosh.mp3'),
    'wing': os.path.join(os.getcwd(), 'sounds/wing.mp3')
}
