# Spotify <-> Yandex Music

This app allows you to convert Spotify track links to Yandex Music links, and vice versa. Its primary purpose is to simplify music sharing for those who prefer different streaming services. 😏

<img src="images_for_readme/demo_2.png" width="30%">

<img src="images_for_readme/demo_1.png" width="30%">



## API vs Selenium + requests

For various reasons, I chose not to use the Spotify/Yandex API directly. Instead, Selenium is used for parsing Spotify web pages. Parsing Yandex Music, on the other hand, only requires well-configured HTTP requests. This approach enables anyone to use this app without needing any API keys.

## Installation and Usage

To install this app, clone this repo, create Python venv and install the required packages. You can use either `requirements-base.txt` for essential libraries or `requirements.txt` for all dependencies:
```bash
pip install -r requirements.txt
```

You may need to obtain cookies for your requests to Yandex Music. You may also find `about_cookies.py` and `.sample_env` useful for that.

If you want to use this app as a Telegram bot, obtain a Telegram bot token, store it in the `.env` file, and then run `tgbot.py`. Alternatively, you can use `spotify_link.py` or `yandexmusic_link.py` for your specific tasks.
