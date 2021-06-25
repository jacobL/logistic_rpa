import pymysql
from datetime import datetime, date,timezone,timedelta
import time 

from bs4 import BeautifulSoup
import requests
import dbconfig

conn = pymysql.connect(host=dbconfig.host, port=dbconfig.port, user=dbconfig.user, passwd=dbconfig.passwd, db='idap')
cur = conn.cursor()

dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
y = str(89+int(dt1.astimezone(timezone(timedelta(hours=8))).strftime('%y')))
ym = dt1.astimezone(timezone(timedelta(hours=8))).strftime('%y%m')  # 轉換時區 -> 東八區
ymd = dt1.astimezone(timezone(timedelta(hours=8))).strftime('%y%m%d')  
creationdate = dt1.astimezone(timezone(timedelta(hours=8))).strftime('%Y/%m/%d %H:%M:%S')  # 轉換時區 -> 東八區
publishdate = dt1.astimezone(timezone(timedelta(hours=8))).strftime('%Y%m%d')  
########

tag = 'logistic'
web = 'cdnsp'
url = 'http://www.cdnsp.com.tw/news/newsold/'+y+'/PDF/P'+ym+'/'+ymd+'.htm'
#publishdate = '20210408'
#url = 'http://www.cdnsp.com.tw/news/newsold/110/PDF/P2104/210408.htm'
print(url)
res = requests.get(url)
#res.encoding = 'utf-8'
res.encoding = 'big5'
soup = BeautifulSoup(res.text, 'html.parser')
plist = soup.select('p')
c = 1
title = ''
content = ''
for i in range(0,len(plist)):    
    tmp = plist[i].text.strip()
    #print(tmp,'\n  ========= ',len(tmp),'==========')
    if len(tmp) > 5 and len(tmp) < 80 and '記者' in tmp :   # 去掉記者 
        continue
        
    if len(tmp) > 5 and i > 0 : 
        if len(tmp) > 50 :            
            content = tmp 
            #print('content:\n',content)
            urltmp = url+str(c)
            cur.execute('insert ignore into news_daily(web, title, content, tag, publishdate, url, creationdate)values(%s, %s, %s, %s, %s, %s, %s)', (web, title, content, tag, publishdate, urltmp, creationdate))
            c = c + 1
        else :
            title = tmp
            if title == '技術資訊 (供技術支援人員使用)' :
                #print('新聞尚未上架')
                break
            #print('a title:',title)
            continue
            
        if len(plist[i].select('font')) == 1 :
            title = plist[i].select('font')[0].text.strip()
            #if '請點擊' not in title and (len(title) > 5 or '版' not in title) :
                #print('c title:',title)
            #else :
            #    break                
        elif len(plist[i].select('font')) == 2 :
            title = plist[i].select('font')[1].text.strip()
            #if '請點擊' not in title and (len(title) > 5 or '版' not in title) :
            #    print('b title:',title)
            #else :
            #    break
    if len(tmp) < 5 :
        break
        
    #print(p)
cur.execute('commit')    
res.close()
cur.close()
conn.close()