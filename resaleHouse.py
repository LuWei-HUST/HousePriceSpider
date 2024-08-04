# -*- coding: utf-8 -*-
"""
Created on Tue May 21 23:19:03 2024

@author: 12615
"""
import re
import os
import time
import json
import copy
import shutil
import random
import requests
from lxml import etree
import pandas as pd
import psycopg2

if __name__ == "__main__":
    tempPath = "/home/luwei/code/HousePriceSpider/data/temp/"
    dataPath = "/home/luwei/code/HousePriceSpider/data/"
    urlFormat = "https://hz.lianjia.com/ershoufang/xiaoshan/pg{}/"

    if os.path.exists(tempPath):
        shutil.rmtree(tempPath)
        os.mkdir(tempPath)
    
    # exit()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    conn_params = {
        "dbname": "test",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost"
    }

    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()
    
    i = 1
    while True:
        
        time.sleep(random.randint(1, 5))
        
        url = urlFormat.format(i)
        print("loop {}, try {}".format(i, url))

        r = requests.get(url=url, headers=headers, timeout=30)
    
        # print(r.text)
    
        text = r.text
    
        with open((tempPath + "resale{}.html").format(i), "w", encoding="utf-8") as f:
            f.write(text)
            
        i += 1
        if i > 10:
            break
    
    res = []
    for i in range(1, 11):
        
        print(i)
        dataDict = {}
        
        with open((tempPath + "resale{}.html").format(i), "r", encoding="utf-8") as fin:
            text = fin.read()
    
            root = etree.HTML(text)
            lis = root.xpath("//li[@class='clear LOGVIEWDATA LOGCLICKDATA']")
    
            print(len(lis))
            
            for li in lis:
                housecode = li.xpath("./div[@class='info clear']/div[@class='title']/a/@data-housecode")[0]
                print(housecode)
                title = li.xpath("./div[@class='info clear']/div[@class='title']/a/text()")[0]
                print(title)
                herf = li.xpath("./div[@class='info clear']/div[@class='title']/a/@href")[0]
                print(herf)
                positionInfoItems = li.xpath("./div[@class='info clear']/div[@class='flood']/div[@class='positionInfo']/a")
                # print(positionInfoItems)
                positionInfo0 = positionInfoItems[0].xpath("./text()")[0]
                print(positionInfo0)
                positionInfo1 = positionInfoItems[1].xpath("./text()")[0]
                print(positionInfo1)
                houseInfo = li.xpath("./div[@class='info clear']/div[@class='address']/div[@class='houseInfo']/text()")[0]
                print(houseInfo)
                avgPrice =None
                try:
                    avgPrice = li.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='unitPrice']/span/text()")[0]
                except Exception as e:
                    pass
                print(avgPrice)
                totalPriceNum = li.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/span/text()")[0]
                totalPriceUnit = li.xpath("./div[@class='info clear']/div[@class='priceInfo']/div[@class='totalPrice totalPrice2']/i/text()")[1]
                totalPrice = str(totalPriceNum) + totalPriceUnit
                
                print("-"*80)
                
                dataDict["housecode"] = housecode
                dataDict["title"] = title
                dataDict["herf"] = herf
                dataDict["positionInfo0"] = positionInfo0
                dataDict["positionInfo1"] = positionInfo1
                dataDict["avgPrice"] = avgPrice.replace(",", "")
                dataDict["totalPrice"] = totalPrice
                dataDict["houseInfo"] = houseInfo
                dataDict["updateTime"] =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                
                tmp = copy.deepcopy(dataDict)
                res.append(tmp)

                cur.execute("insert into resalehouseinfo values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (housecode, title, herf, positionInfo0, positionInfo1, avgPrice.replace(",", ""), totalPrice, houseInfo, dataDict["updateTime"]))
                
                
    df = pd.DataFrame(res)
    
    date = time.strftime('%Y%m%d%H%M%S',time.localtime())
    df.to_csv((dataPath + "resale{}.csv").format(date), header=False, index=False)

    conn.commit()
    cur.close()
    conn.close()