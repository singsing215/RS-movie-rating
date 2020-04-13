import requests
from bs4 import BeautifulSoup
import pandas as pd


movie = 'https://maoyan.com/films?yearId=15&showType=3&sortId=3' 
html = requests.get(movie) # connect to the server 
#print(html.text)

bs = BeautifulSoup(html.text, 'lxml') # manage tags in HTML document

table = bs.find('div', {'class': 'movie-list'})
print(table)
#movie_list = table.find_all('dd')


'''
movie_name_list=[]
release_year_list=[]
rank_moving_list=[]
movie_rate_list=[]
movie_desc_list=[]
for ml in movie_list:
    #movie name
    movie_name = ml.find('td', {'class': 'titleColumn'}).find('a').get_text()
    movie_name_list.append(movie_name)
    #release year
    release_year = ml.find('span', {'class': 'secondaryInfo'}).get_text()
    release_year_list.append(release_year)
    #rank moving
    rank_moving = str(ml.find('span', {'class': 'global-sprite'}))
    rank_moving_list.append(rank_moving)
    #movie rate
    movie_rate = ml.find('td', {'class': 'ratingColumn imdbRating'}).get_text().strip()
    movie_rate_list.append(movie_rate)
    #movie desc
    movie_id= ml.find('td', {'class': 'titleColumn'}).find('a')['href']
    movie_link = 'http://www.imdb.com' + movie_id 
    print(movie_link)
    new = requests.get(movie_link)
    bs = BeautifulSoup(new.text, 'lxml')
    desc = bs.find('div', {'class': 'summary_text'})
    movie_desc = desc.get_text().strip()
    print(movie_desc)
    movie_desc_list.append(movie_desc)
    #poster
    poster = bs.find('div', {'class': 'poster'}).find('a').find('img')
    img_link = poster['src']
    image = requests.get(img_link)
    name = movie_name + '.jpg'
    with open(name, 'wb') as f:
        f.write(image.content) # writing the picture

def rename(rank_moving_list):
    a=[]
    for w in rank_moving_list:
        if w == '<span class="global-sprite titlemeter down"></span>':
            a.append('down')
        elif w == '<span class="global-sprite titlemeter up"></span>':
            a.append('up')
        else:
            a.append('no change')
    return a

#print(rename(rank_moving_list))
'''


'''
output=pd.DataFrame({'movie name':movie_name_list,'release year':release_year_list,'rank moving':rename(rank_moving_list),'movie rate':movie_rate_list,'movie desc':movie_desc_list})
output.to_csv('C:\\Users\\SingSing\\Documents\\GitHub\\exercise\\extract-top-100-movies\\output.csv')
print('File Output Success')
'''

