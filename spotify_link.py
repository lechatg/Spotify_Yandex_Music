from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

def ParseSpotyLink(initial_link):
    """
    Parse a Spotify link using Selenium and return a dictionary containing
    the artist, album, and song names.
    """
    clean_link = initial_link.split('?')[0]
    
    # Use --headless=new selenium mode so that the browser window wouldn’t be visible 
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Use basic selenium mode to see what's going on in the browser window
    # driver = webdriver.Chrome()

    # Open spotify page with given track
    driver.get(clean_link)
    driver.implicitly_wait(5)

    Artist_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/section/div[1]/div[5]/div/div/span/a').get_attribute('text')
    print(Artist_name)

    Album_name = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/section/div[1]/div[5]/div/span[1]/a').get_attribute('text')
    print(Album_name)
    driver.implicitly_wait(5)

    Str_with_Song_name = driver.find_element(by=By.XPATH, value='/html/head/title').get_attribute('text')

    if ' - song by' in Str_with_Song_name:
        Song_name = Str_with_Song_name.split(' - song by')[0]
    elif ' - song and lyrics by' in Str_with_Song_name:
        Song_name = Str_with_Song_name.split(' - song and lyrics by')[0]
    else:
        Song_name = Str_with_Song_name
    print(Song_name)

    dictREQ = {'Artist_name' : Artist_name, 'Album_name' : Album_name, 'Song_name': Song_name }

    return dictREQ

# Uncomment and run test
# ParseSpotyLink('https://open.spotify.com/track/6LgJvl0Xdtc73RJ1mmpotq')

def CompileLinkOnSpotify(search_artist_name, search_album, search_song_name):
    """
    Generate a Spotify link for a specific track using provided artist, album, and song names.

    This function takes the names of an artist, album, and song as input parameters
    and uses Selenium to search for the corresponding track on Spotify. It then
    constructs and returns a Spotify link to the identified track.
    """
    # Use --headless=new selenium mode so that the browser window wouldn’t be visible 
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Use basic selenium mode to see what's going on in the browser window
    # driver = webdriver.Chrome()

    driver.implicitly_wait(5)

    # Open spotify search page
    driver.get("https://open.spotify.com/search")
    driver.implicitly_wait(5)

    # Type artist name in input field
    textBox = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[3]/header/div[3]/div/div/form/input')
    textBox.send_keys(search_artist_name)
    driver.implicitly_wait(5)

    # Click on 'artists' (because best result can simply be a song/album of the same name as artist instead of artist name, that we need on this stage)
    driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/div[1]/div/div/div/div/div/a[3]/button').click()
    driver.implicitly_wait(5)
    
    # Click on first artist in results
    driver.find_element(by=By.XPATH, value='//*[@id="searchPage"]/div/div/div/div[1]/div[1]/div[1]').click()
    artist_url = driver.current_url
    driver.implicitly_wait(2)

    driver.maximize_window()
    # Click 'see discography'
    driver.find_element(by=By.XPATH, value='//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div[2]/main/section/div/div[2]/div[3]/section[2]/div[1]/div/a').click()
    
    # Find album
    # (It works, but better to be improved in future. Because as for now it clicks on the first match found, and since the artist may have both the track and the album called same, it may fail)
    try:
        driver.find_element(By.LINK_TEXT, search_album).click()
    except:
        driver.quit()
        print(artist_url)
        return artist_url

    album_url = driver.current_url
    driver.implicitly_wait(10)

    try:
        el = driver.find_element(By.LINK_TEXT, search_song_name)

        # IMPORTANT. Just 'click' doesn't work in this case because of some invisible overlapping elements
        # So this won't work:
        # driver.find_element(By.LINK_TEXT, search_song_name).click()
        # send_keys('\n')- is the solution (https://stackoverflow.com/questions/11908249/debugging-element-is-not-clickable-at-point-error)

        el.send_keys('\n')
        driver.implicitly_wait(10)
        # Store current url - if success it is an actual track link we need
        get_url = driver.current_url
    except:
        driver.quit()
        print(album_url)
        return album_url

    driver.quit()
    
    return get_url

# Uncomment and run test
# parsed_data = {'Artist_name': 'Radiohead', 'Album_name': 'OK Computer', 'Song_name': 'Paranoid Android'}
# link = CompileLinkOnSpotify(parsed_data['Artist_name'], parsed_data['Album_name'], parsed_data['Song_name'])
# print(link)