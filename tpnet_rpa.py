import pymysql
from datetime import datetime, date,timezone,timedelta
from bs4 import BeautifulSoup
import requests
import time 
import dbconfig
conn = pymysql.connect(host=dbconfig.host, port=dbconfig.port, user=dbconfig.user, passwd=dbconfig.passwd, db='logistic')
cur = conn.cursor()

cur.execute('delete from logistic.tpnet') 
cur.execute('ALTER TABLE logistic.tpnet AUTO_INCREMENT = 1')

before = 4
after = 32
beforeDate = (datetime.today() - timedelta(days=before)).strftime('%Y/%m/%d 00:00')
afterDate = (datetime.today() + timedelta(days=after)).strftime('%Y/%m/%d 00:00')
cityList = ['KEL','TPE', 'TXG', 'KHH']
city = cityList[0]
#print(beforeDate,afterDate)

initUrl = 'https://tpnet.twport.com.tw/IFAWeb/Reports/InPortShipList/Details?selectPort={}&orderBy=expectDt&orderAsc=ASC&spExpectDtFrom={}&spExpectDtTo={}&shipType=B11&special01=False&special02=False&page={}'
dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
creationdate = dt1.astimezone(timezone(timedelta(hours=8))).strftime('%Y/%m/%d %H:%M:%S')  # 轉換時區 -> 東八區

begin_time = time.time()
for city in cityList :
    url = initUrl.format(city,beforeDate,afterDate,1)
    res = requests.get(url) 
    soup = BeautifulSoup(res.text, 'html.parser')
    finalPage = int(soup.select('li.PagedList-skipToLast a')[0].get('href').split('&')[-1].replace('page=',''))
    for p in range(1,finalPage+1) :
        url = initUrl.format(city,beforeDate,afterDate,p)
        
        res = requests.get(url) 
        soup = BeautifulSoup(res.text, 'html.parser')
        trList = soup.select('tbody tr')
        print(city,' Page:',p,' count:',int((len(trList)-3)/2))
        for i in range(0,int((len(trList)-3)/2)) :
            try :
                td = trList[3+i*2].select('td')

                # 1.船舶呼號
                ship_call_sign = None if td[0].text.strip() == '' else td[0].text.strip()

                # 3.船種
                ship_type = None if td[1].text.strip() == '' else td[1].text.strip()

                # 5.英文船名
                shipname_en = None if td[2].text.strip() == '' else td[2].text.strip()

                # 7.簽證編號
                visa = None if td[3].text.strip() == '' else td[3].text.strip()    

                # 9.預報進港時間
                scheduled_arrival_datetime = None if td[4].text.strip() == '' else td[4].text.strip()

                # 11.預定靠泊時間
                scheduled_berthing_datetime = None if td[5].text.strip() == '' else td[5].text.strip()

                # 13.靠泊碼頭
                berthing = None if td[6].text.strip() == '' else td[6].text.strip()

                # 15.前一港
                former_port = None if td[7].text.strip() == '' else td[7].text.strip()

                # 17.VHF報到時間
                vhf_datetime = None if td[8].text.strip() == '' else td[8].text.strip()

                # 19.船長(M)
                length_m = None if td[9].text.strip() == '' else td[9].text.strip()

                # 21.下錨時間
                anchor_datetime = None if td[10].text.strip() == '' else td[10].text.strip()       

                """
                print('ship_call_sign:',ship_call_sign,' ship_type:',ship_type,' shipname_en:',shipname_en,' visa:',visa,
                      ' scheduled_arrival_datetime:',scheduled_arrival_datetime,' scheduled_berthing_datetime:',scheduled_berthing_datetime,
                      ' berthing:',berthing,' former_port:',former_port,' vhf_datetime:',vhf_datetime,' length_m:',length_m,
                      ' anchor_datetime',anchor_datetime)
                """
                td = trList[3+i*2+1].select('td')

                # 2.imo
                imo = None if td[0].text.strip() == '' else td[0].text.strip()

                # 4.港口代理
                agent_name = None if td[1].text.strip() == '' else td[1].text.strip()

                # 6.中文船名
                shipname_tw = None if td[2].text.strip() == '' else td[2].text.strip()

                # 8.到港目的
                action = None if td[3].text.strip() == '' else td[3].text.strip()  

                # 10.進港通過港口時間
                through_port_datetime = None if td[4].text.strip() == '' else td[4].text.strip()

                # 12.預定離泊時間
                scheduled_departure_datetime = None if td[5].text.strip() == '' else td[5].text.strip()

                # 14.靠泊時間
                berthing_datetime = None if td[6].text.strip() == '' else td[6].text.strip()

                # 16.次一港
                second_port_country = None
                second_port_city = None
                second_port = None if td[7].text.strip() == '' else td[7].text.strip()
                if second_port != None :
                    second_port_country = second_port.split(' ')[0]
                    second_port_city = second_port.split(' ')[1]

                # 18.船長報到ETA
                captain_eta = None if td[8].text.strip() == '' else td[8].text.strip()

                # 20.總噸
                tonnage = None if td[9].text.strip() == '' else td[9].text.strip()

                # 22.進港通過5浬時間
                five_miles_datetime = None if td[10].text.strip() == '' else td[10].text.strip()
                """
                print('imo:',imo,' agent_name:',agent_name,' shipname_tw:',shipname_tw,' action:',action,' through_port_datetime:',through_port_datetime,
                      ' scheduled_departure_datetime:',scheduled_departure_datetime,' berthing_datetime:',berthing_datetime,
                      ' second_port:',second_port,' captain_eta:',captain_eta,' tonnage:',tonnage,' five_miles_datetime:',five_miles_datetime)         
                print('\n')
                """
                cur.execute('insert into logistic.tpnet(ship_call_sign,imo,ship_type,agent_name,shipname_en,shipname_tw,visa,action,scheduled_arrival_datetime,through_port_datetime,scheduled_berthing_datetime,scheduled_departure_datetime,berthing,berthing_datetime,former_port,second_port_country,second_port_city,vhf_datetime,captain_eta,length_m,tonnage,anchor_datetime,five_miles_datetime,city,creationdate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(ship_call_sign,imo,ship_type,agent_name,shipname_en,shipname_tw,visa,action,scheduled_arrival_datetime,through_port_datetime,scheduled_berthing_datetime,scheduled_departure_datetime,berthing,berthing_datetime,former_port,second_port_country,second_port_city,vhf_datetime,captain_eta,length_m,tonnage,anchor_datetime,five_miles_datetime,city,creationdate))
                
                # 20210601 加上備份機制，以利後續慶世分析
                cur.execute('insert ignore into logistic.tpnet_log(ship_call_sign,imo,ship_type,agent_name,shipname_en,shipname_tw,visa,action,scheduled_arrival_datetime,through_port_datetime,scheduled_berthing_datetime,scheduled_departure_datetime,berthing,berthing_datetime,former_port,second_port_country,second_port_city,vhf_datetime,captain_eta,length_m,tonnage,anchor_datetime,five_miles_datetime,city,creationdate)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(ship_call_sign,imo,ship_type,agent_name,shipname_en,shipname_tw,visa,action,scheduled_arrival_datetime,through_port_datetime,scheduled_berthing_datetime,scheduled_departure_datetime,berthing,berthing_datetime,former_port,second_port_country,second_port_city,vhf_datetime,captain_eta,length_m,tonnage,anchor_datetime,five_miles_datetime,city,creationdate))
                
                cur.execute('commit')
            except Exception as e :
                print('ship_call_sign:',ship_call_sign,' ship_type:',ship_type,' shipname_en:',shipname_en,' visa:',visa,
                      ' scheduled_arrival_datetime:',scheduled_arrival_datetime,' scheduled_berthing_datetime:',scheduled_berthing_datetime,
                      ' berthing:',berthing,' former_port:',former_port,' vhf_datetime:',vhf_datetime,' length_m:',length_m,
                      ' anchor_datetime',anchor_datetime)
                print('imo:',imo,' agent_name:',agent_name,' shipname_tw:',shipname_tw,' action:',action,' through_port_datetime:',through_port_datetime,
                      ' scheduled_departure_datetime:',scheduled_departure_datetime,' berthing_datetime:',berthing_datetime,
                      ' second_port_country:',second_port_country,' second_port_city:',second_port_city,' captain_eta:',captain_eta,' tonnage:',tonnage,' five_miles_datetime:',five_miles_datetime)         
                print('\n')
end_time = time.time()
print('process time: ' + str(round(end_time-begin_time, 2)) + ' seconds')

res.close()
cur.close()
conn.close()        