import os
from dotenv import load_dotenv
import json
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve cookies from environment variable COOKIES_JSON
COOKIES_JSON = os.getenv("COOKIES_JSON")

# requests.get() expects cookies in dictionary type, so need to convert them from JSON to dict
COOKIES = json.loads(COOKIES_JSON)

def ParseYandexLink(initial_link):
    """
    Parse a Yandex Music link and extract artist, album, and song names in a dictionary.
    
    Expected input link looks like "https://music.yandex.ru/album/3389007/track/330813"
    """
    
    # Extract album ID and track ID from the initial link
    found_album_link = initial_link.split('/track')[0]
    found_album_id = found_album_link.split('/album/')[1]
    found_track_id_for_request = initial_link.split('/track/')[1]


    # Construct request to retrieve album information (from Album page)
    params = {
        'album': found_album_id,
        'light': 'true',
        'sortOrder': '',
        'lang': 'ru',
        'external-domain': 'music.yandex.ru',
        'overembed': 'false',
        'ncrnd': '0.14640685812238985',
    }

    response = requests.get('https://music.yandex.ru/handlers/album.jsx', params=params, cookies=COOKIES)
    result = response.json()

    # Extract artist, album, and song names from the response
    Artist_name = result['artists'][0]['name']
    Album_name = result['title']

    for songJSON in result['volumes'][0]:
        if songJSON['id'] == found_track_id_for_request:
            Song_name = songJSON['title']
            break

    dictREQ = {'Artist_name' : Artist_name, 'Album_name' : Album_name, 'Song_name': Song_name }
    return(dictREQ)

def CompileLinkOnYandexMusic(search_artist_name, search_album, search_song_name):
    """
    Generate a Yandex Music link for a specific track using provided artist, album, and song names.

    This function takes the names of an artist, album, and song as input parameters
    and in a few iterations of http-requests tries to find the corresponding track on Yandex Music. It then
    constructs and returns a Yandex Music link to the identified track.
    """
    
    # Construct 1st request - search for the artist
    params_artist = {
        'text': search_artist_name,
        'type': 'artists',
        'ncrnd': '0.8632064493644813',
        'clientNow': '1704408588224',
        'lang': 'ru',
        'external-domain': 'music.yandex.ru',
        'overembed': 'false',
    }

    response_artist = requests.get('https://music.yandex.ru/handlers/music-search.jsx', params=params_artist, cookies=COOKIES)
    
    # Pick up first found artist
    best_result_artist = response_artist.json()['artists']['items'][0]
    best_result_artist_id = best_result_artist['id']
    artist_url = 'https://music.yandex.ru/artist/' + str(best_result_artist_id)

    # Construct 2nd request - Search for the albums of the detected artist
    params_albums = {
        'artist': best_result_artist_id,
        'what': 'albums',
        'sort': 'year',
        'dir': '',
        'period': 'month',
        'trackPage': '0',
        'trackPageSize': '100',
        'lang': 'ru',
        'external-domain': 'music.yandex.ru',
        'overembed': 'false',
        'ncrnd': '0.8649229141460504',
    }

    response_albums = requests.get('https://music.yandex.ru/handlers/artist.jsx', params=params_albums, cookies=COOKIES)
    albums_of_artist = response_albums.json()['albums']
    
    # Find the album ID matching the provided album name
    found_album_id = None
    for album in albums_of_artist:
        found_album_id = None
        if album['title'] == search_album:
            found_album_id = album['id']
            break
    
    if found_album_id == None:
        print('Found artist, but not an album')
        return artist_url

    album_url = 'https://music.yandex.ru/album/' + str(found_album_id)


    # Construct 3rd request - for a detected album page
    params_found_album = {
        'album': found_album_id,
        'light': 'true',
        'sortOrder': '',
        'lang': 'ru',
        'external-domain': 'music.yandex.ru',
        'overembed': 'false',
        'ncrnd': '0.14640685812238985',
    }

    response_found_album = requests.get('https://music.yandex.ru/handlers/album.jsx', params=params_found_album, cookies=COOKIES)
    album_tracks_id = response_found_album.json()['trackIds']

    # Construct 4th request - for a song page (for songs from the detected album)
    found_song_id = None
    for track_id_for_check in album_tracks_id:
        
        track_id_for_request = str(track_id_for_check) + ':' + str(found_album_id)
        
        params_song = {
            'track': track_id_for_request,
            'lang': 'ru',
            'external-domain': 'music.yandex.ru',
            'overembed': 'false',
            'ncrnd': '0.3032588195970749',
        }

        response_song = requests.get('https://music.yandex.ru/handlers/track.jsx', params=params_song, cookies=COOKIES)
        tracknameforcheck = response_song.json()['track']['title']
        if tracknameforcheck == search_song_name:
            found_song_id = track_id_for_check
            break
        
    if found_song_id == None:
        print('Found artist, album but not a song')
        return album_url

    link_for_song_YM = 'https://music.yandex.ru/album/' + str(found_album_id) +'/track/' + str(found_song_id)

    return link_for_song_YM

# Uncomment and run tests
# print(ParseYandexLink("https://music.yandex.ru/album/3389007/track/330813"))
# print(CompileLinkOnYandexMusic('Radiohead', 'OK Computer', 'Paranoid Android'))
