import re
import urllib.request
from bs4 import BeautifulSoup
import requests


agent = 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) \
        Gecko/20100101 Firefox/24.0'
headers = {'User-Agent': agent}
base = "https://www.azlyrics.com/"
 
def get_lyrics(artist,song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/"+artist+"/"+song_title+".html"
    
    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>','').replace('</br>','').replace('</div>','').strip()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" +str(e)

#Fuente: https://github.com/adhorrig/azlyrics/blob/master/azlyrics/azlyrics.py
def get_artists(letter):
    if letter.isalpha() and len(letter) is 1:
        letter = letter.lower()
        url = base + letter + ".html"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        data = []

        for div in soup.find_all("div", {"class": "container main-page"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip().lower())
        return (data)
    else:
        raise Exception("Unexpected Input")


def search_artist(artist):
    artist = artist.lower()

    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    if artist.startswith("the"):    # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    print(artist)
    artists = (get_artists(artist[0].lower()))


    return list(filter(lambda x: artist in x, artists))

def get_songs_by_artist(artist):
    artist = artist.lower()
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    if artist.startswith("the"):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]
    url = "http://azlyrics.com/" + artist[0] + "/" + artist + ".html"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        data = []
        for div in soup.find_all("div", {"id": "listAlbum"}):
            links = div.findAll('a')
            for a in links:
                data.append(a.text.strip())
        return data

    except Exception as e:
        return "Exception occurred \n" + str(e)

print(search_artist("the Who"))

print(get_songs_by_artist(search_artist("the Who")[2]))