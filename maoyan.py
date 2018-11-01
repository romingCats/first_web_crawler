import requests
from bs4 import BeautifulSoup as bs
import sqlite3

conn = sqlite3.connect('maoyan_movie.sqlite3')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Movies (movie_name VARCHAR(128), movie_rating VARCHAR(128))")

p1=0
def url_paras(p1):
    params= {'offset':p1}
    return params

def one_page():
    headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15'}
    op=requests.get('http://maoyan.com/board/4',headers=headers,params=url_paras(p1))
    op.encoding = 'UTF-8'
    html= op.text
    return html

def analysis_write(conn,cur):
    soup=bs(one_page(),'html.parser')
    movies = soup.find_all('div',class_='board-item-content')

    for movie in movies:
        movie_name= movie.a['title']
        movie_rating_1= movie.find('i',class_=('integer'))
        movie_rating_2=movie.find('i',class_=('fraction'))
        movie_rating = movie_rating_1.get_text()+movie_rating_2.get_text()
        #with open('maoyan.txt','a') as f:
            #f.write(movie_name+' '+movie_rating+'\n')
        sql = "INSERT INTO Movies (movie_name,movie_rating) VALUES (?,?)"
        val = (movie_name,movie_rating)
        cur.execute(sql,val)
        conn.commit()

if __name__ == '__main__':
    for i in range(10):
        analysis_write(conn,cur)
        p1+=10
