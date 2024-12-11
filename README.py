from asyncore import read
from json import load
#from openpyxl import Workbook,load_workbook
import json
#import openpyxl
from pathlib import Path
from pickle import TRUE
from traceback import print_tb
from xml.dom.minidom import Entity
import requests
import urllib3
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xlsxwriter
import datetime
import pytz
 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Environment
ProdEnv = "3f2c3bac-8f12-4c72-8ade-c9ccfa775b54"
TestEnv = "86fc6e59-1938-4084-a56a-773c9a2ac6e6"
GlobalB = "77aa454c-c992-42e1-9f0c-283c1aa68466"

#Api-Token
ProdToken = "Api-Token "
TestToken = "Api-Token "
GlobalBToken = "Api-Token "

ClusterToken = "Api-Token "

GeneralUrl = "https://dynatrace.turkcell.com.tr"


def timestamp_to_saat(time):
                    milisaniyeUtc = time
                    #Milisaniye saniye dönüştürme
                    saniyeUTC = milisaniyeUtc / 1000.0
                    # GMT+3 saat dilimi
                    utz = pytz.timezone('UTC')
                    GMT3 = pytz.timezone('Europe/Istanbul')
                    # timestamp'i datetime yapma
                    utc_time = datetime.datetime.fromtimestamp(saniyeUTC, tz=utz)
                    gmt3_time = GMT3.normalize(utc_time)
                    #excel format
                    gmt3_time_string = gmt3_time.strftime("%Y-%m-%d %H:%M:%S %z")
                    return gmt3_time_string

def UserControl(Env,EnvToken,ClusterToken,Url):
    #List
    Gruplar = ""
    User,UserGroup,GirisSayi,Event,Basarısı,Tarih = [],[],[],[],[],[]#Logın
    Basarılı,Basarısız,x,t=0,0,0,0
    lOGİN , CONFİG , AKTİF= [],[],[] #Aktıflık
    İslemler,EventConf ,TarihConf,BasarıConf = [],[],[],[] #conf
    indi = 0
    headers = {
        'accept': 'application/json',
        'Authorization': ClusterToken,
    }

    responseUser = requests.get(Url + '/api/v1.0/onpremise/users', headers=headers, verify=False)
    UserList = json.loads(responseUser.text)
    
    for user in UserList:
        
        true = True
        false = False
        Basarılı,Basarısız,x,t,z=0,0,0,0,0
        
        #print(user["id"])
        if "groups" in user :
            for grup in user["groups"]:
                if t == 0 :   
                    Gruplar = Gruplar  + str(grup)
                    t = t + 1
                else:
                    Gruplar = Gruplar +" - "+ str(grup)

                
        
        
        headers = {
            'accept': 'application/json; charset=utf-8',
            'Authorization': EnvToken,
        }

        params = {
            'pageSize': '5000',
            'sort': '-timestamp',
        }
        
        response = requests.get(
            Url + "/e/3f2c3bac-8f12-4c72-8ade-c9ccfa775b54/api/v2/auditlogs?filter=user%28%22" + user["id"] + "%22%29%2CeventType%28%22LOGIN%22%29&from=now-30d&sort=-timestamp",
            params=params,
            headers=headers,
            verify=False
        )
        Log = json.loads(response.text)
        #print(Log)
        if Log["totalCount"] != 0:
            GirisSayi.append(Log["totalCount"])
            User.append(user["id"])
            UserGroup.append(Gruplar)
            for ınfo in Log["auditLogs"]:
                if ınfo["success"] == true :
                    Basarılı = Basarılı + 1 
                else:
                    Basarısız = Basarısız + 1
                if x == 0:
                    Event.append(ınfo["eventType"])
                    #print(ınfo["timestamp"])
                    Tarih.append(timestamp_to_saat(ınfo["timestamp"]))
                    x= x + 1
            
            Basarısı.append("Başarılı:"+str(Basarılı)+" - "+"Başarısız:"+str(Basarısız))
        else:
            GirisSayi.append(Log["totalCount"])
            User.append(user["id"])
            Tarih.append("KULLANICI GİRİŞ YAPMADI")
            UserGroup.append(Gruplar)
            Event.append("LOGIN")
            Basarısı.append("Giriş Yapmadı")
             
        Basarılı,Basarısız=0,0 
        
        #Bunları excel formatında yazdırmak için worksheet kullanma
        workbook = xlsxwriter.Workbook('UserLogin.xlsx')
        worksheet = workbook.add_worksheet()
        Baslık = ["User Name","User Group","Tarih","Event","Giriş sayısı","Başarı Durumu"]

        worksheet.write_row(0, 0, Baslık)
        worksheet.write_column(1, 0, User)
        worksheet.write_column(1, 1, UserGroup)
        worksheet.write_column(1, 2, Tarih)
        worksheet.write_column(1, 3, Event)
        worksheet.write_column(1, 4, GirisSayi)
        worksheet.write_column(1, 5, Basarısı)
            
        workbook.close()   
        
        #LOGIN dısında config işlemleri
        
        headers = {
        'accept': 'application/json; charset=utf-8',
            'Authorization': EnvToken,
        }

        responseWithOutLogın = requests.get(
            Url + '/e/' + Env + '/api/v2/auditlogs?filter=user%28%22' + user["id"] + '%22%29&from=now-30d&sort=-timestamp',
            headers=headers,
            verify=False
        )
        ConfıgLog = json.loads(responseWithOutLogın.text)
        #print(ConfıgLog["auditLogs"])
        İslemSayısı = (ConfıgLog["totalCount"]) - (Log["totalCount"])
        İslemler.append(İslemSayısı)
        
        if İslemSayısı == 0 :
            EventConf.append("İŞLEM YAPMADI")
            TarihConf.append("KULLANICI İŞLEM YAPMADI")
            BasarıConf.append("İŞLEM YAPMADI")
        else:
            for conf in ConfıgLog["auditLogs"] :
                
                if conf["eventType"] != "LOGIN" :
                    
                    if conf["success"] == true :
                        Basarılı = Basarılı + 1
                    else:
                        Basarısız = Basarısız + 1
                    if z == 0 :
                        EvetsConf = conf["eventType"] +" - " + conf["category"]
                        EventConf.append(EvetsConf)
                        TarihConf.append(timestamp_to_saat(conf["timestamp"]))
                        z = z + 1
            BasarıConf.append("Başarılı:"+str(Basarılı)+" - "+"Başarısız:"+str(Basarısız))
            
                    
                    
        
            #Bunları excel formatında yazdırmak için worksheet kullanma
        workbook = xlsxwriter.Workbook('UserConfig.xlsx')
        worksheet = workbook.add_worksheet()
        Baslık = ["User Name","User Group","Tarih","Event","İşlem Sayısı","Başarı Durumu"]

        worksheet.write_row(0, 0, Baslık)
        worksheet.write_column(1, 0, User)
        worksheet.write_column(1, 1, UserGroup)
        worksheet.write_column(1, 2, TarihConf)
        worksheet.write_column(1, 3, EventConf)
        worksheet.write_column(1, 4, İslemler)
        worksheet.write_column(1, 5, BasarıConf)
            
        workbook.close()   
        #Hem Giriş Hem İşlem yapanlar
         
        if Log["totalCount"] != 0 and İslemSayısı != 0 :
            lOGİN.append("EVET")
            CONFİG.append("EVET")
        if Log["totalCount"] != 0 and İslemSayısı == 0 :
            lOGİN.append("EVET")
            CONFİG.append("HAYIR")
        #print(İslemSayısı)
        if Log["totalCount"] == 0 and İslemSayısı == 0 :
            lOGİN.append("HAYIR")
            CONFİG.append("HAYIR")
            
        if lOGİN[indi] == "EVET" and CONFİG[indi] == "EVET" :
            AKTİF.append("AKTİF")
        elif lOGİN[indi] == "EVET" and CONFİG[indi] == "HAYIR" :
            AKTİF.append("SADECE LOGİN")
        else:
            AKTİF.append("USER AKTİF DEĞİL")
            
        indi = indi + 1
        print(indi)
        
            #Bunları excel formatında yazdırmak için worksheet kullanma
        workbook = xlsxwriter.Workbook('UserAktiflik.xlsx')
        worksheet = workbook.add_worksheet()
        Baslık = ["User Name","User Group","LOGİN","CONFİG"]

        worksheet.write_row(0, 0, Baslık)
        worksheet.write_column(1, 0, User)
        worksheet.write_column(1, 1, UserGroup)
        worksheet.write_column(1, 2, lOGİN)
        worksheet.write_column(1, 3, CONFİG) 
        worksheet.write_column(1, 4, AKTİF) 
        workbook.close()      
        # print(sayac)   
            
        Gruplar = ""   
        

UserControl(ProdEnv,ProdToken,ClusterToken,GeneralUrl)
