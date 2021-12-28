import requests
import json


def GetAlbum():
    response = requests.get("http://ws.audioscrobbler.com/2.0/?method=album.search&album=a&api_key=a55968a48ea6772da02a89946eed999e&format=json&limit=350")
    albumsJson = response.json()['results']['albummatches']['album']
    albums = []
    for x in albumsJson:
        if x['mbid'] == '':
            continue
        album = {}
        album['name'] = x['name']
        album['artist'] = x['artist']
        album['image'] = next(filter(lambda x: x['size'] == 'extralarge', x['image']))['#text']
        album['id'] = x['mbid']
        albums.append(album)

    for album in albums:
        response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=a55968a48ea6772da02a89946eed999e&mbid={album['id']}&format=json")
        album['songs'] = []

        try:
            albumsData = response.json()['album']
            album['published'] = albumsData['wiki']['published']
            album['genre'] = albumsData['tags']['tag'][0]['name']

            for x in albumsData['tracks']['track']:
                album['songs'].append(x['name'])
        except:
            print(albumsData)

    with open('data.json', 'w') as f:
        json.dump(albums, f)

#GetAlbum()


def CreateDb(albums):
    from albums.models import Album, AlbumsSong
    from song.models import Song

    for data in albums:
        album = Album(name=data['name'], artist=data['artist'], image_url=data['image'], public=True)
        album.save()

        for dataSong in data['songs']:
            song = Song(title=dataSong, performer=data['artist'], year=data['published'].split(' ')[2][0:4], genre=data['genre'].capitalize())
            song.save()

            albumSong = AlbumsSong(album=album, song=song)
            albumSong.save()
