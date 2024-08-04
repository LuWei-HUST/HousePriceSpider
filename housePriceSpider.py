import re
import os
import time
import json
import copy
import random
import requests
from lxml import etree
import pandas as pd

if __name__ == "__main__":
    
    tempPath = "/home/luwei/code/HousePriceSpider/data/temp"
    dataPath = "/home/luwei/code/HousePriceSpider/data"
    
    urlFormat = "https://hz.fang.lianjia.com/loupan/xiaoshan/nht1pg{}/#xiaoshan"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    
    i = 1
    while True:
        
        time.sleep(random.randint(1, 5))
        
        url = urlFormat.format(i)

        r = requests.get(url=url, headers=headers)
    
        print("got page ", i)
    
        text = r.text
    
        with open((tempPath + "/page{}.html").format(i), "w", encoding="utf-8") as f:
            f.write(text)
            
        i += 1
        if i > 10:
            break

    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()))
    
    res = []
    for i in range(1, 11):
        
        print(i)
        dataDict = {}
        
        with open((tempPath + "/page{}.html").format(i), "r", encoding="utf-8") as fin:
            text = fin.read()
    
            root = etree.HTML(text)
            lis = root.xpath("//li[@class='resblock-list post_ulog_exposure_scroll has-results']")
    
            print(len(lis))
            
            for li in lis:
                title = li.xpath("./a/@title")[0]
                print(title)
                herf = li.xpath("./a/@href")[0]
                print(herf)
                saleStatus = li.xpath("./div/div[@class='resblock-name']/span[@class='sale-status']/text()")[0]
                print(saleStatus)
                location0 = li.xpath("./div/div[@class='resblock-location']/span/text()")[0]
                print(location0)
                location1 = li.xpath("./div/div[@class='resblock-location']/span/text()")[1]
                print(location1)
                location2 = li.xpath("./div/div[@class='resblock-location']/a/text()")[0]
                print(location2)
                area = None
                try:
                    area = li.xpath("./div/div[@class='resblock-area']/span/text()")[0]
                except Exception as e:
                    pass
                print(area)
                avgPrice =None
                try:
                    avgPrice = li.xpath("./div/div[@class='resblock-price']/div[@class='main-price']/span[@class='number']/text()")[0]
                except Exception as e:
                    pass
                print(avgPrice)
                totalPrice = None
                try:
                    totalPrice = li.xpath("./div/div[@class='resblock-price']/div[@class='second']/text()")[0]
                except Exception as e:
                    pass
                print(totalPrice)
                
                
                print("-"*80)
                
                dataDict["title"] = title
                dataDict["herf"] = herf
                dataDict["saleStatus"] = saleStatus
                dataDict["location0"] = location0
                dataDict["location1"] = location1
                dataDict["location2"] = location2
                dataDict["area"] = area
                dataDict["avgPrice"] = avgPrice
                dataDict["totalPrice"] = totalPrice
                dataDict["updateTime"] =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                
                tmp = copy.deepcopy(dataDict)
                res.append(tmp)
                
                
    df = pd.DataFrame(res)
    
    date = time.strftime('%Y%m%d%H%M%S',time.localtime())
    df.to_csv((dataPath + "/info{}.csv").format(date), header=False, index=False)
    # df.to_excel((dataPath + "/info{}.xls").format(date), header=True)
    
    # df = pd.read_excel("./data/info.xls", header=0)
    
    # print(df.head)
    # baseUrl = "https://hz.fang.lianjia.com"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    # }
    
    # updateTime = time.strftime('%Y-%m-%d_%H%M%S',time.localtime())
    # for index, row in df.iterrows():
    #     time.sleep(random.randint(1, 3))
        
    #     herf = row["herf"]
    #     url = baseUrl + herf
        
    #     r = requests.get(url=url, headers=headers)
        
    #     fileName = herf.split("/")[-2]
    #     # print(fileName)
    #     with open("./data/page/"+fileName+"_"+updateTime+".html", "w", encoding="utf-8") as fout:
    #         fout.write(r.text)
        