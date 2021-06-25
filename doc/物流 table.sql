
ship_call_sign,imo,ship_type,agent_name,shipname_en,shipname_tw,visa,action,scheduled_arrival_datetime,through_port_datetime,scheduled_berthing_datetime,scheduled_departure_datetime,berthing,berthing_datetime,former_port,second_port,vhf_datetime,captain_eta,length_m,tonnage,anchor_datetime,five_miles_datetime,city,creationdate

ALTER TABLE logistic.tpnet AUTO_INCREMENT = 1
CREATE TABLE logistic.tpnet(
id int NOT NULL AUTO_INCREMENT,
ship_call_sign varchar(30) NULL, -- 船舶呼號	
imo int NULL, -- IMO
ship_type varchar(50) NULL, -- 船種	
agent_name varchar(50) NULL, -- 港口代理
shipname_en varchar(100) NULL, -- 英文船名
shipname_tw varchar(100) NULL, -- 中文船名 
visa varchar(100) NULL, -- 簽證編號
action varchar(50) NULL, -- 到港目的
scheduled_arrival_datetime DATETIME NULL, -- 預報進港時間	
through_port_datetime DATETIME NULL, -- 進港通過港口時間
scheduled_berthing_datetime DATETIME NULL, -- 預定靠泊時間
scheduled_departure_datetime DATETIME NULL, -- 預定離泊時間
berthing varchar(50) NULL, -- 靠泊碼頭
berthing_datetime DATETIME NULL, -- 靠泊時間
former_port varchar(100) NULL, -- 前一港	
second_port_country varchar(50) NULL, -- 次一港(國家)
second_port_city varchar(50) NULL, -- 次一港(城市)
vhf_datetime DATETIME NULL, -- VHF報到時間	
captain_eta DATETIME NULL, -- 船長報到ETA
length_m FLOAT NULL, -- 船長(M)	
tonnage FLOAT NULL, -- 總噸
anchor_datetime DATETIME NULL, -- 下錨時間
five_miles_datetime DATETIME NULL, -- 進港通過5浬時間
city varchar(50) NULL, -- 城市(基/北/中/高)
creationdate DATETIME NULL, -- 建立時間
PRIMARY KEY(id) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 20210601 加上備份機制，以利後續慶世分析
CREATE TABLE logistic.tpnet_log(
id int NOT NULL AUTO_INCREMENT,
ship_call_sign varchar(30) NULL, -- 船舶呼號	
imo int NULL, -- IMO
ship_type varchar(50) NULL, -- 船種	
agent_name varchar(50) NULL, -- 港口代理
shipname_en varchar(100) NULL, -- 英文船名
shipname_tw varchar(100) NULL, -- 中文船名 
visa varchar(100) NULL, -- 簽證編號
action varchar(50) NULL, -- 到港目的
scheduled_arrival_datetime DATETIME NULL, -- 預報進港時間	
through_port_datetime DATETIME NULL, -- 進港通過港口時間
scheduled_berthing_datetime DATETIME NULL, -- 預定靠泊時間
scheduled_departure_datetime DATETIME NULL, -- 預定離泊時間
berthing varchar(50) NULL, -- 靠泊碼頭
berthing_datetime DATETIME NULL, -- 靠泊時間
former_port varchar(100) NULL, -- 前一港	
second_port_country varchar(50) NULL, -- 次一港(國家)
second_port_city varchar(50) NULL, -- 次一港(城市)
vhf_datetime DATETIME NULL, -- VHF報到時間	
captain_eta DATETIME NULL, -- 船長報到ETA
length_m FLOAT NULL, -- 船長(M)	
tonnage FLOAT NULL, -- 總噸
anchor_datetime DATETIME NULL, -- 下錨時間
five_miles_datetime DATETIME NULL, -- 進港通過5浬時間
city varchar(50) NULL, -- 城市(基/北/中/高)
creationdate DATETIME NULL, -- 建立時間
PRIMARY KEY(id) ,
CONSTRAINT tpnet_log_uk UNIQUE (imo,berthing_datetime)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


1.ship_call_sign, 船舶呼號	
2.imo, IMO
3.ship_type, 船種	
4.agent_name, 港口代理
5.shipname_en, 英文船名
6.shipname_tw, 中文船名 
7.visa, 簽證編號
8.action, 到港目的
9.scheduled_arrival_datetime, 預報進港時間	
10.through_port_datetime, 進港通過港口時間
11.scheduled_berthing_datetime, 預定靠泊時間

12.scheduled_departure_datetime, 預定離泊時間
13.berthing, 靠泊碼頭
14.berthing_datetime, 靠泊時間
15.former_port, 前一港	
16.second_port, 次一港(second_port_country,second_port_city)
17.vhf_datetime, VHF報到時間	
18.captain_eta, 船長報到ETA
19.length_m, 船長(M)	
20.tonnage, 總噸
21.anchor_datetime, 下錨時間
22.five_miles_datetime, 進港通過5浬時間
23.city, 城市(基/北/中/高)


ALTER TABLE logistic.khbweb AUTO_INCREMENT = 1
CREATE TABLE logistic.khbweb(
id int NOT NULL AUTO_INCREMENT,
shipno int NULL, -- 船編
voyage varchar(20) NULL, -- 航次
berthing int NULL, -- 靠泊碼頭
shipname_tw varchar(100) NULL, -- 船名(中)
shipname_en varchar(100) NULL, -- 船名(英)
length_m int NULL, -- 總長
tonnage int NULL, -- 噸位
agent_no int NULL, -- 港代理(編號)
agent_name varchar(50) NULL, -- 港代理(名稱)
pilot_apply_datetime DATETIME NULL, -- 申請引水
pilot_apply_YC varchar(5) NULL,  -- 申請引水審核
check_datetime DATETIME NULL, -- 聯檢派檢
check_YC varchar(5) NULL, -- 聯檢派檢審核	 
scheduled_arrival_datetime DATETIME NULL, -- 預定進港
captain_eta DATETIME NULL, -- 船長ETA	 
actually_arrived_datetime DATETIME NULL, -- 實際到達時間
anchor_datetime DATETIME NULL, -- 下錨時間	 
harbor int NULL, -- 進出港口
action varchar(50) NULL, -- 目的	 
shiptype varchar(50) NULL, -- 船舶種類
destination varchar(50) NULL, -- 航線	 
imo int NULL, -- IMO
rescue int NULL, -- 保全
issc_csr varchar(5) NULL, -- ISSC-CSR
PRIMARY KEY(id) 
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

預定進港頁彙整的資料
第1欄---------------
1.shipno, 船編
2.voyage, 航次
第2欄---------------
3.berthing, 靠泊碼頭
第3欄---------------
4.shipname_tw, 船名(中)
5.shipname_en, 船名(英)
第4欄---------------
6.length_m, 總長
7.tonnage, 噸位
8.agent_no, 港代理(編號)
9.agent_name, 港代理(名稱)
第5欄---------------
10.pilot_apply_datetime, 申請引水
11.pilot_apply_YC, 申請引水審核
12.check_datetime, 聯檢派檢
13.check_YC, 聯檢派檢審核	 
第7欄---------------
14.scheduled_arrival_datetime, 預定進港
15.captain_eta, 船長ETA	 
第8欄---------------
16.actually_arrived_datetime, 實際到達時間
17.anchor_datetime, 下錨時間	 
第9欄---------------
18.harbor, 進出港口
19.action, 目的	 
第10欄---------------
20.shiptype, 船舶種類
21.destination, 航線	 
第11欄---------------
22.imo, IMO
23.rescue, 保全
24.issc_csr, ISSC-CSR