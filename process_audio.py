import mutagen
from mutagen.easyid3 import EasyID3
from mutagen.id3 import USLT, ID3, APIC


def process_audio(filePath: str, title=None, artist=None, album=None, genre=None, tracknumber=None, lyricist=None,
                  volume=None, version=None, date=None, picFile=None, lyrics=None, lyrics_lang=None):
    try:
        audiofile = EasyID3(filePath)
    except mutagen.id3.ID3NoHeaderError:
        audiofile = mutagen.File(filePath, easy=True)
        audiofile.add_tags()
    if title:
        audiofile["title"] = title
    if artist:
        audiofile["artist"] = artist
    if album:
        audiofile["album"] = album
    if artist:
        audiofile["albumartist"] = artist
    if genre:
        audiofile["genre"] = genre
    if tracknumber:
        audiofile["tracknumber"] = tracknumber
    if lyricist:
        audiofile["lyricist"] = lyricist
    if volume:
        audiofile["volume"] = volume
    if version:
        audiofile["version"] = version
    if date:
        audiofile["date"] = date
    audiofile.save()
    audiofile = ID3(filePath)
    if picFile:
        imagedata = open(picFile, 'rb').read()
        audiofile.add(APIC(3, 'image/jpeg', 3, 'Front cover', imagedata))
    if lyrics:
        uslt = USLT(encoding=3, desc=u'desc', text=lyrics)
        if lyrics_lang:
            uslt.lang = lyrics_lang
        audiofile.add(uslt)
    audiofile.save()
