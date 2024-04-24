# In order to make Yandex Music parsing work you may need to retrieve cookies from http-get request (e.g. copy them from your request to their web using devtools)
# You may try your requests without cookies, but for me it fails
# It should look like this:
cookies = {
        'i': 'xxx',
        'yandexuid': 'xxx',
        'device_id': 'xxx',
        'yashr': 'xxx',
        'gdpr': 'xxx',
        '_ym_uid': 'xxx',
        '_ym_d': 'xxx',
        '_ym_isad': 'xxx',
        'yuidss': 'xxx',
        'ymex': 'xxx',
        'bh': 'xxx',
        '_ym_visorc': 'xxx',
        '_yasc': 'xxx',
        'spravka': 'xxx',
        'active-browser-timestamp': 'xxx',
    }
# Then you should store it as JSON in one line in .env (see .sample_env)