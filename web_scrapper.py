import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
from unidecode import unidecode


songs = pd.read_csv('canciones_religiosas.txt', sep='\t')

# url to scrape the lyrics from
base_url = "https://www.letras.com/canciones-religiosas/{}/"

all_lyrics    = []
all_url       = []
all_song_name = [] 

for idx, r in songs.iterrows():
    song_name = unidecode(r['song_name'].lower())
    final_url = base_url.format('-'.join(song_name.split(' ')))

    try: 
        html_page = urlopen(final_url)
        soup = BeautifulSoup(html_page, 'html.parser')

        html_pointer = soup.find('div', attrs={'class':'cnt-letra-trad g-pr g-sp'})
        object_l = html_pointer.find_next('div')
        lyrics = ''.join(str(object_l.contents)).replace('<br/>', '\n').replace('</br>', '') #.replace('<p>', ' ').replace('<br>', ' ').replace('</br>', ' ').replace('</p>', ' ')
        lyrics = lyrics.replace('</p>', '').replace('<p>', '')
        lyrics = lyrics[6:-6]

        all_url.append(final_url)
        all_song_name.append(r['song_name'])
        all_lyrics.append(lyrics)
    except:
        print('Lyrics not found for {}'.format(r['song_name']))

df_lyrics1 = pd.DataFrame(columns =['lyrics', 'url', 'song_name'])
df_lyrics1['lyrics']    = all_lyrics 
df_lyrics1['url']       =  all_url 
df_lyrics1['song_name'] = all_song_name 

df_lyrics1.to_csv('lyrics_canciones-religiosas_letras-com.csv')


base_url =  "https://www.musica.com/{}"

# Scrapping to get song names
list_song_names = "https://www.musica.com/letras.asp?letras=16677&orden=alf"
html_page = urlopen(list_song_names)
soup = BeautifulSoup(html_page, 'html.parser')

html_pointer = soup.find('href') #, attrs={'class':'cnt-letra-trad g-pr g-sp'})
html_pointer = soup.find_all('div', attrs={'class':'imagen-cancion'})

song_html = html_pointer[1]
songs_url  = []
songs_name = []
for song_html in html_pointer:
    try:
        songs_url.append( base_url.format(song_html.findNext('a')['href'] ))
        songs_name.append( song_html.findNext('a')['title'] )
    except:
        None


df_lyrics2 = pd.DataFrame(columns =['lyrics', 'url', 'song_name'])
df_lyrics2['url']       =  songs_url 
df_lyrics2['song_name'] = songs_name 

lyrics_all = []
for idx, r in df_lyrics2.iterrows(): #['url'].iloc[10]
    try:
        html_page = urlopen( r['url'])
        soup = BeautifulSoup(html_page, 'html.parser')
        l = soup.find('div', attrs={'letra'}).find_all('div', attrs={'id':'letra'})[0]        
        
        l = l.find_all('p')
        l = ''.join([i.decode_contents() for i in l]).replace('<br/>', ' \n ').replace('</br>', '').replace('</p>', '').replace('<p>', '')
        lyrics_all.append(l)
    except:
        lyrics_all.append('NaN')
        print('Lyrics not found for {}'.format(r['song_name']))


df_lyrics2['lyrics'] = lyrics_all

df_lyrics_all = [df_lyrics1, df_lyrics2]
df_lyrics_all = pd.concat(df_lyrics_all)

df_lyrics_all.to_csv('lyrics_canciones-religiosas.csv')