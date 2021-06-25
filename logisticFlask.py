from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
from collections import OrderedDict
import pymysql
import time
import json
from datetime import datetime, date,   timezone,timedelta

from bs4 import BeautifulSoup
import requests

import warnings
warnings.filterwarnings('ignore')
import dbconfig

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# db config 

@app.route("/getTpnet", methods=['GET'])
def getTpnet():
    conn = pymysql.connect(host=dbconfig.host, port=dbconfig.port, user=dbconfig.user, passwd=dbconfig.passwd, db='logistic')
    cur = conn.cursor()
    before = 4
    after = 32
    beforeDate = (datetime.today() - timedelta(days=before)).strftime('%Y/%m/%d 00:00')
    afterDate = (datetime.today() + timedelta(days=after)).strftime('%Y/%m/%d 00:00')
    PortList = ['KEL','TPE', 'TXG', 'KHH']
    print('beforeDate:',beforeDate,',afterDate:',afterDate)
    
    tpnet_list = OrderedDict()
    cur.execute("select id,ship_call_sign,imo,ship_type,agent_name,shipname_en,shipname_tw,visa,action, \
                DATE_FORMAT(scheduled_arrival_datetime,'%Y-%m-%d %H:%i:%S'),DATE_FORMAT(through_port_datetime,'%Y-%m-%d %H:%i:%S'),\
                DATE_FORMAT(scheduled_berthing_datetime,'%Y-%m-%d %H:%i:%S'),DATE_FORMAT(scheduled_departure_datetime,'%Y-%m-%d %H:%i:%S'),\
                berthing,DATE_FORMAT(berthing_datetime,'%Y-%m-%d %H:%i:%S'),former_port,second_port_country,second_port_city,\
                DATE_FORMAT(vhf_datetime,'%Y-%m-%d %H:%i:%S'),DATE_FORMAT(captain_eta,'%Y-%m-%d %H:%i:%S'),length_m,tonnage,\
                DATE_FORMAT(anchor_datetime,'%Y-%m-%d %H:%i:%S'),DATE_FORMAT(five_miles_datetime,'%Y-%m-%d %H:%i:%S'),city,DATE_FORMAT(creationdate,'%Y-%m-%d %H:%i:%S')\
                from tpnet order by id")
    c=0
    for r in cur :    
        tmp = OrderedDict()
        tmp['id'] = r[0]
        tmp['ship_call_sign'] = r[1]
        tmp['imo'] = r[2]
        tmp['ship_type'] = r[3]
        tmp['agent_name'] = r[4]
        tmp['shipname_en'] = r[5]
        tmp['shipname_tw'] = r[6]
        tmp['visa'] = r[7]
        tmp['action'] = r[8]
        tmp['scheduled_arrival_datetime'] = r[9]
        tmp['through_port_datetime'] = r[10]
        tmp['scheduled_berthing_datetime'] = r[11]
        tmp['scheduled_departure_datetime'] = r[12]
        tmp['berthing'] = r[13]
        tmp['berthing_datetime'] = r[14]
        tmp['former_port'] = r[15]
        tmp['second_port_country'] = r[16]
        tmp['second_port_city'] = r[17]
        tmp['vhf_datetime'] = r[18]
        tmp['captain_eta'] = r[19]
        tmp['length_m'] = r[20]
        tmp['tonnage'] = r[21]
        tmp['anchor_datetime'] = r[22]
        tmp['five_miles_datetime'] = r[23]
        tmp['city'] = r[24]
        tmp['creationdate'] = r[25] 
        tpnet_list[c] = tmp
        c=c+1
    
    second_port_country_list = OrderedDict()
    
    cur.execute("SELECT second_port_country,count(1) c FROM tpnet group by second_port_country order by c desc")
    c=1
    total_c = 0
    for r in cur :    
        tmp = OrderedDict()
        tmp['second_port_country'] = r[0]
        tmp['count'] = r[1]
        total_c = total_c + r[1]
        second_port_country_list[c] = tmp
        c=c+1
    second_port_country_list[0] = {'second_port_country':'全部','count':total_c}
    
    second_port_city_list = OrderedDict()
    second_port_city_list['全部'] = ['全部']
    cur.execute("SELECT second_port_country,second_port_city,count(1) c FROM tpnet group by second_port_country,second_port_city order by second_port_country,c desc")
    c=0
    tmp = list()
    for r in cur :    
        if c > 0 and r[0] != second_port_country :
            second_port_city_list[second_port_country] = tmp
            tmp = list()
        tmp.append(r[1])          
        second_port_country = r[0]
        #second_port_city = r[1]
        c=c+1
    second_port_city_list[second_port_country] = tmp
    
    cur.close()
    conn.close()  
    returnData = OrderedDict(); 
    returnData['tpnet_list'] = tpnet_list
    returnData['second_port_country_list'] = second_port_country_list
    returnData['second_port_city_list'] = second_port_city_list
    
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    

@app.route("/getKhbweb", methods=['GET'])
def getKhbweb():
    conn = pymysql.connect(host=host, port=port,user=user, passwd=passwd, db=db)
    cur = conn.cursor()
    
    cur.execute("SELECT id,shipno,voyage,berthing,shipname_tw,shipname_en,length_m,tonnage,agent_no,agent_name,pilot_apply_datetime,pilot_apply_YC,check_datetime,check_YC,scheduled_arrival_datetime,captain_eta,actually_arrived_datetime,anchor_datetime,harbor,action,shiptype,destination,imo,rescue,issc_csr from khbweb order by id")    
    khbweb_list = OrderedDict();
    c=0
    for r in cur :    
        tmp = OrderedDict()
        tmp['id'] = r[0]
        tmp['shipno'] = r[1]
        tmp['voyage'] = r[2]
        tmp['berthing'] = r[3]
        tmp['shipname_tw'] = r[4]
        tmp['shipname_en'] = r[5]
        tmp['length_m'] = r[6]
        tmp['tonnage'] = r[7]
        tmp['agent_no'] = r[8]
        tmp['agent_name'] = r[9]
        tmp['pilot_apply_datetime'] = r[10]
        tmp['pilot_apply_YC'] = r[11]
        tmp['check_datetime'] = r[12]
        tmp['check_YC'] = r[13]
        tmp['scheduled_arrival_datetime'] = r[14]
        tmp['captain_eta'] = r[15]
        tmp['actually_arrived_datetime'] = r[16]
        tmp['anchor_datetime'] = r[17]
        tmp['harbor'] = r[18]
        tmp['action'] = r[19]
        tmp['shiptype'] = r[20]
        tmp['destination'] = r[21]
        tmp['imo'] = r[22]
        tmp['rescue'] = r[23]
        tmp['issc_csr'] = r[24]
        khbweb_list[c] = tmp
        c=c+1
        
    cur.close()
    conn.close()  
    returnData = OrderedDict(); 
    returnData['khbweb_list'] = khbweb_list
    response = jsonify(returnData)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=89)  # 34089  
    #app.run(host='127.0.0.1', port=89)    
    #app.run(host='PC89600059495S', port=85) 