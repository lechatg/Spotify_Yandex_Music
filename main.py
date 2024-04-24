from spotify_link import ParseSpotyLink, CompileLinkOnSpotify
from yandexmusic_link import ParseYandexLink, CompileLinkOnYandexMusic

# Detect link type
def consume_link(given_link):
    if ('spotify' not in given_link) and ('yandex' not in given_link):
        return 'Это не похоже на ссылку для Спотифая или Яндекс Музыки'
    if 'spotify' in given_link:
        return convert_spoty_to_yandex(given_link)
    if 'yandex' in given_link:
        return convert_yandex_to_spoty(given_link)

# Get spotify link for a track and return yandex link
def convert_spoty_to_yandex(given_link):
    parsed_data = ParseSpotyLink(given_link)
    print(parsed_data)

    link = CompileLinkOnYandexMusic(parsed_data['Artist_name'], parsed_data['Album_name'], parsed_data['Song_name'])
    print(link)
    return link

# Get yandex link for a track and return spotify link
def convert_yandex_to_spoty(given_link):
    parsed_data = ParseYandexLink(given_link)
    print(parsed_data)

    link = CompileLinkOnSpotify(parsed_data['Artist_name'], parsed_data['Album_name'], parsed_data['Song_name'])
    print(link)
    return link

# Uncomment and run test for spotify link
# given_link = 'https://open.spotify.com/track/6LgJvl0Xdtc73RJ1mmpotq'
# consume_link(given_link)

# Uncomment and run test for yandex link
# given_link = 'https://music.yandex.ru/album/3389007/track/330813'
# consume_link(given_link)