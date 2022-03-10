import collections
import os
import subprocess
import urllib
from multiprocessing import Pool

import requests
import vk_api
from vk_api.audio import VkAudio

from process_audio import process_audio


class VkMusicGetter:
    def __init__(self, login, password):
        self.vkSession = vk_api.VkApi(login, password)
        try:
            self.vkSession.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return

    def downloadTrack(self, track: dict):
        title = track['title'][:60] + ' - ' + track['artist'][:60] + ".mp3"
        print(title)
        filePath = os.path.join("vkMusic", title)
        if os.path.exists(filePath):
            return
        subprocess.call(["ffmpeg", "-n", "-http_persistent", "false", "-i", track['url'], "-c", "copy", filePath],
                        stderr=subprocess.DEVNULL)
        if (len(track['track_covers'])):
            request = requests.get(track['track_covers'][-1])
            if request.status_code == requests.codes.ok:
                with open("picFile", 'wb') as file:
                    file.write(request.content)
            process_audio(filePath,
                          title=track['title'],
                          artist=track['artist'],
                          album=track.get('album'),
                          picFile="picFile")
        else:
            process_audio(filePath,
                          title=track['title'],
                          artist=track['artist'],
                          album=track.get('album'))

    def getMusic(self):
        Pool(16).map(self.downloadTrack, VkAudio(self.vkSession).get())
