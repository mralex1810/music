import os

from vkMusic import VkMusicGetter
from yandexMusic import YandexMusicGetter

if __name__ == '__main__':
    YandexMusicGetter(os.getenv("YANDEX_TOKEN")).getMusic()
    VkMusicGetter(os.getenv("VK_LOGIN"), os.getenv("VK_PASSWORD")).getMusic()
