from flask import Flask
import psycopg2
from flask import render_template
import logging
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote
from flask import request
from flask import send_from_directory,make_response

app = Flask(__name__,template_folder='templates')
handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)

@app.route('/',methods=["GET","POST"])
def link_sql():
    if request.method=="GET":
        reli=get_sql()
        return render_template('index.html',reli=reli)
    if request.method=="POST":
        print(request.form.to_dict())
        key_word=request.form.to_dict()['key_word']
        if key_word[:5]=='clear':
                sql_empty()
        else:
            update_sql(key_word)

        update_sql(key_word)
        reli=get_sql()
        return render_template('index.html',reli=reli)
def get_sql():
    con=psycopg2.connect(
        host='',
        user='',
        password='',
        database=''
    )
    c=con.cursor()
    sql='select * from xxq'
    c.execute(sql)
    rs=c.fetchall()
    con.close()
    return list(rs)
def get_info(key):
    #print(key)
    key = quote(key, 'gbk')
    r = requests.get(r'https://search.17k.com/search.xhtml?c.q={}'.format(key), headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62'})
    print(r'https://search.17k.com/search.xhtml?q={}'.format(key))
    r.encoding = r.apparent_encoding
    #print(r.text)
    soup = BeautifulSoup(r.text)
    ls = soup.find_all('div', attrs={"class": "textmiddle"})
    pattern = re.compile(r'\s+')
    lis_square = []
    for l in ls:
        lis = []
        lis.append(re.sub(pattern, '', l.find('dl').find('dt').find('a').text))
        temp = l.find('li', attrs={'class': 'bq'}).find_all('span')
        lis.append(re.sub(pattern, '', temp[0].find('a').text))
        lis.append(re.sub(pattern, '', temp[1].find('a').text))
        lis.append(re.sub(pattern, '', temp[2].find('code').text))
        lis.append(l.find('dl').find('dt').find('a').attrs['href'])
        lis.append(temp[0].find('a').attrs['href'])
        lis_square.append(lis)
    return lis_square
def update_sql(keyword):
    lis_square=get_info(keyword)
    con = psycopg2.connect(
        host='',
        user='',
        password='',
        database=''
    )
    c = con.cursor()
    for lis in lis_square:
        try:
            sql = "insert into xxq (name,author,length,category,url1,url2)values ('{}','{}','{}','{}','{}','{}');".format(lis[0],lis[1],lis[3],lis[2],lis[4].split('.')[-2].split('/')[-1],lis[5].split('.')[-2].split('/')[-1])
            print(sql)
            c.execute(sql)
            con.commit()
        except Exception as e:
            con.commit()
            print(e)
    con.close()
def sql_empty():
    con = psycopg2.connect(
        host='',
        user='',
        password='',
        database=''
    )
    c = con.cursor()
    sql="delete from xxq where 1=1"
    c.execute(sql)
    con.commit()
    con.close()
    return

@app.route('/d')
def down():
    f=open('/var/www/xxq/down/data.csv','wb')
    liss=get_sql()
    for lis in liss:
        f.write(lis[0].encode('utf-8'))
        f.write(','.encode('utf-8'))
        f.write(lis[1].encode('utf-8'))
        f.write(','.encode('utf-8'))
        f.write(lis[2].encode('utf-8'))
        f.write(','.encode('utf-8'))
        f.write(lis[3].encode('utf-8'))
        f.write(','.encode('utf-8'))
        f.write('https://www.17k.com/book/{}.html'.format(lis[4]).encode('utf-8'))
        f.write(','.encode('utf-8'))
        f.write('https://user.17k.com/see/www/{}.html'.format(lis[5]).encode('utf-8'))
        f.write(','.encode('utf-8'))
        f.write('\n'.encode('utf-8'))
    f.close()
    return make_response(send_from_directory('down','data.csv',as_attachment=True))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=500)

