# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:23:56 2020

@author: SingSing
"""
import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import pandas as pd

user_id_list=[]
user_rate_list=[]
movie_name_list=[]
movie_id_list=[]
uid_list=[]
movie_link_list=[]
movie_desc_list=[]


def get_html(url):
    pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
    resopnse = requests.get(url, proxies={'http': random.choice(pro)})
    html_doc = resopnse.text
    return html_doc


if __name__ == "__main__":
    m='https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    bs = BeautifulSoup(get_html(m), 'lxml')
    table = bs.find('tbody', {'class': 'lister-list'})
    m_list = table.find_all('tr')
    
    for ml in m_list:
        m_id= ml.find('td', {'class': 'titleColumn'}).find('a')['href']
        movie_link_list.append(m_id)
    
    #top 100 movie range(0,100)
    for i in movie_link_list[:100]:
        m = 'https://www.imdb.com'+i+'reviews?ref_=tt_urv' 
        bs = BeautifulSoup(get_html(m), 'lxml')
        table = bs.find('div', {'class': 'lister-list'})
        comd_list = table.find_all('span', {'class': 'display-name-link'})
        
        for ml in comd_list:
            user_id= ml.find('a')['href'].strip('/user')
            user_id_list.append(user_id)
            
        #user list
        for user in user_id_list[:4]:#from each top 100 movie comment page, select top 4 active comment users
            user_link = 'https://www.imdb.com/user/ur' + user +'/reviews'
            print(user_link)
            bs = BeautifulSoup(get_html(user_link), 'lxml')
            comment_list = bs.find_all('div', {'class': 'lister-item-content'})
            #comment list
            for cl in comment_list[:5]:#acquire 5 movie comment data from each 4 users
                #movie name
                movie_name = cl.find('div', {'class': 'lister-item-header'}).find('a').get_text()
                movie_name_list.append(movie_name)
                #movie id
                movie_id = cl.find('div', {'class': 'lister-item-header'}).find('a')['href'].strip('/tile')
                movie_id_list.append(movie_id)
                #user rate
                user_rate = cl.find('span', {'class': ''}).get_text().strip('Was this review helpful?  Sign in to vote.\n')
                user_rate_list.append(user_rate)
                #user id
                uid = user
                uid_list.append(uid)
                print(len(uid_list))
                #movie desc
                movie_link = 'https://www.imdb.com/title/tt' + movie_id
                bs = BeautifulSoup(get_html(movie_link), 'lxml')
                desc = bs.find('div', {'class': 'summary_text'})
                movie_desc = desc.get_text().strip()
                movie_desc_list.append(movie_desc)
                sleep(random.random() * 3)
        
    output=pd.DataFrame({'user id':uid_list,'movie name':movie_name_list,'movie id':movie_id_list, 'user rate':user_rate_list,'movie desc':movie_desc_list})
    output.to_csv('C:\\Users\\SingSing\\Documents\\test2.csv')
    print('File Output Success')


    

