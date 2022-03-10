from yandex_music import Client, Track

from process_audio import process_audio


class YandexMusicGetter:

    def __init__(self, token: str):
        self.client: Client = Client(token).init()


    def downloadTrack(self, track: Track, path: str):
        fileTitle = f'{track.title} - {track.artists[0].name}'
        filePath = path + fileTitle + ".mp3"
        print(fileTitle)
        if not track.available:
            print("Not downloaded")
            return
        track.download(filePath)
        lyrics = None
        lyrics_lang = None
        if track.lyrics_available:
            yandex_lyrics = track.getSupplement().lyrics
            if yandex_lyrics:
                if yandex_lyrics.text_language in [None, "en"]:
                    yandex_lyrics.text_language = "eng"
                if yandex_lyrics.text_language in ["ru"]:
                    yandex_lyrics.text_language = "rus"
                if yandex_lyrics.text_language in ["sw"]:
                    yandex_lyrics.text_language = "swe"
                if len(yandex_lyrics.text_language) != 3:
                    yandex_lyrics.text_language = "und"
                lyrics = yandex_lyrics.full_lyrics
                lyrics_lang = yandex_lyrics.text_language
        track.downloadCover("picFile")
        if track.meta_data:
            process_audio(filePath=filePath,
                          title=track.title,
                          album=track.albums[0].title,
                          artist=track.artists[0].name,
                          lyrics=lyrics,
                          lyrics_lang=lyrics_lang,
                          picFile="picFile",
                          genre=track.meta_data.genre,
                          date=track.meta_data.year,
                          version=track.meta_data.version,
                          volume=track.meta_data.volume,
                          lyricist=track.meta_data.lyricist,
                          tracknumber=track.meta_data.number)
        else:
            process_audio(filePath=filePath,
                          title=track.title,
                          album=track.albums[0].title,
                          artist=track.artists[0].name,
                          lyrics=lyrics,
                          lyrics_lang=lyrics_lang,
                          picFile="picFile")



    def getMusic(self):
        for track in self.client.usersLikesTracks():
            self.downloadTrack(track.fetchTrack(), "./yandexFavorite/")
        station = "user:onyourwave"
        downloaded = set()
        lastTrackId = -1
        self.client.rotorStationSettings2(station, mood_energy=u"all", diversity=u"favorite", language=u"any",
                                     type_=u"rotor")
        self.client.rotorStationFeedbackRadioStarted(station, client.device)
        while len(downloaded) < 500:
            if lastTrackId != -1:
                tracks = self.client.rotorStationTracks(station, settings2=True, queue=lastTrackId)
            else:
                tracks = self.client.rotorStationTracks(station, settings2=True)
            for track in tracks.sequence:
                track: Track = track.track
                if track.id in downloaded:
                    continue
                self.client.rotorStationFeedbackTrackStarted(station, track_id=track.id)
                self.downloadTrack(track, "./yandexMyWave/")
                downloaded.add(track.id)
                lastTrackId = track.id
                self.client.rotorStationFeedbackTrackFinished(station, track_id=track.id,
                                                         total_played_seconds=track.duration_ms / 1000)
