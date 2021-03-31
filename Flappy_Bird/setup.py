# From https://www.youtube.com/watch?v=u4ykDbciXa8

from setuptools import setup

##APP = ['testapp.py']
##DATA_FILES = ['1.gif','2.gif']
##OPTIONS = {
## 'iconfile':'logoapp.icns',
## 'argv_emulation': True,
## 'packages': [''],
##}
##
##setup(
##    app=APP,
##    data_files=DATA_FILES,
##    options={'py2app': OPTIONS},
##    setup_requires=['py2app'],
##)


APP = ['/Users/brandonthio/Python/Flappy_Bird/Flappy_Bird.py']
DATA_FILES = ['/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_BG.png',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_2.1.png',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_2(10).png',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_2(20).png',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_2(30).png',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_JUMP.ogg',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_SCORE1.ogg',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_GO.ogg',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_PIPEUP.png',
              '/Users/brandonthio/Python/Flappy_Bird/Graphics/F_BIRD_PIPEDOWN.png']
OPTIONS = {
 'iconfile':'/Users/brandonthio/Python/Flappy_Bird/FLAPPY_BIRD_ICON.icns',
 'argv_emulation': False,
 'packages': ['certifi'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
