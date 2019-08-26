#google Drive のマウントを取る
from google.colab import drive
drive.mount('/content/gdrive')

from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request,urlopen
import csv
import os
import itertools
import datetime as dt


os.chdir("/content/gdrive/My Drive/Datasets/boat_data")
csvFile=open("boat_file3.csv",'wt',newline='',encoding="utf-8")
writer=csv.writer(csvFile)

index=[]
index.extend(['Date','Race',
              '6th-rank','6th-num',
              '5th-rank','5th-num',
              '4th-rank','4th-num',
              '3rd-rank','3rd-num',
              '2nd-rank','2nd-num',
              '1st-rank','1st-num',
             '6th-ratio','5th-ratio','4th-ratio','3rd-ratio','2nd-ratio','1st-ratio',
             '1st','2nd','3rd','4th','5th','6th',])

seq=(1,2,3,4,5,6)
index.extend(list(itertools.permutations(seq,3)))

writer.writerow(index)

#データの取得年月日指定
start=dt.date(2019,8,24)
period=2

i=0
for n in range(period):
    tstr=(start+dt.timedelta(n)).strftime('%Y%m%d')
    print(tstr)
    #レースでループ
    for j in range(12):
        url="https://sp.macour.jp/s/race/entry-info/jid/01/date/"+tstr+"/num/"+str(j+1)+"/"
    
        req =Request(url,headers={'User-Agent':'Mozilla/5.0'})
        html=urllib.request.urlopen(req,timeout=1000)
        soup=BeautifulSoup(html,"html.parser")
    
        rows=soup.findAll("table",class_="race entry")
        print(j+1)
    
        odds=[]
    
        odds.append(tstr)
        odds.append(j+1)
    
        entry=[]
    
        #クラス、選手番号
        for cell in rows[0].findAll("td",class_="racer-l-g2"):
            entry.append(cell.get_text())
        for cell in rows[0].findAll("td",class_="racer-l-y2"):
            entry.append(cell.get_text())
        for cell in rows[0].findAll("td",class_="racer-l-b2"):
            entry.append(cell.get_text())
        for cell in rows[0].findAll("td",class_="racer-l-r2"):
            entry.append(cell.get_text())
        for cell in rows[0].findAll("td",class_="racer-l-k2"):
            entry.append(cell.get_text())
        for cell in rows[0].findAll("td",class_="racer-l-w2"):
            entry.append(cell.get_text())
        
        
        for i in range(6):
            odds.extend(entry[i*7+1:i*7+3])
            
        #全国勝率
        rows=soup.findAll("tr",id="racer-all")
        
        entry=[]
        for cell in rows[0].findAll("td"):
            entry.append(cell.get_text())
        
        odds.extend(entry)
        
        
        url="https://sp.macour.jp/s/race/result-info/jid/01/date/"+tstr+"/num/"+str(j+1)+"/"
        
        req =Request(url,headers={'User-Agent':'Mozilla/5.0'})
        html=urllib.request.urlopen(req,timeout=1000)
        soup=BeautifulSoup(html,"html.parser")
    
        rows=soup.findAll("table",class_="race result2")
    
    
        result=[]
    
        for cell in rows[0].findAll(['span']):
            result.append(cell.get_text())
        
        #着順入力
        for i in range(6):
            odds.append(int(result[i]))

        url="https://sp.macour.jp/s/odds/odds-rentan/date/"+tstr+"/jid/01/num/"+str(j+1)+"/"
        
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req,timeout=1000)
        soup = BeautifulSoup(html, "html.parser")
    
        rows=soup.findAll("div",class_="col-6")
    
        for i in range(6):
            for cell in rows[i].findAll(['td']):
                odds.append(cell.get_text())
    
        writer.writerow(odds)
    
    
csvFile.close()
print("finish")



