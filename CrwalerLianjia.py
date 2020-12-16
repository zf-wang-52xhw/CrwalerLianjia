from bs4 import BeautifulSoup

import datetime
import requests
import time


class CrwalerLianjia():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}
        self.url = 'https://sh.lianjia.com/ershoufang/putuo/pg{0}p1p2l2/'
        'https://sh.lianjia.com/ershoufang/putuo/pg2dp1l2p1p2/'

    def getList(self):
        for i in range(1, 101):
            print(i)
            htmlStr = requests.get(self.url.format(i), headers=self.header).content
            soup = BeautifulSoup(htmlStr, 'lxml')
            sellListContent = soup.select('.sellListContent li.LOGCLICKDATA')
            for sell in sellListContent:
                try:
                    # 详情url
                    detailUrl = sell.select('div.title a')[0].attrs['href']
                    # 标题
                    title = sell.select('div.title a')[0].string
                    # 先抓取全部的div信息，再针对每一条进行提取
                    houseInfo = list(sell.select('div.houseInfo')[0].stripped_strings)
                    # 楼盘名字
                    loupan = houseInfo[0]
                    # 对楼盘的信息进行分割
                    info = houseInfo[0].split('|')
                    # 房子类型
                    houseType = info[1].strip()
                    # 面积大小
                    area = info[2].strip()
                    # 房间朝向
                    toward = info[3].strip()
                    # 装修类型
                    renovation = info[4].strip()
                    # 房屋地址
                    positionInfo = ''.join(list(sell.select('div.positionInfo')[0].stripped_strings))
                    # 房屋总价
                    totalPrice = ''.join(list(sell.select('div.totalPrice')[0].stripped_strings))
                    # 房屋单价
                    unitPrice = list(sell.select('div.unitPrice')[0].stripped_strings)[0]

                    # 声明一个字典存储数据
                    dataDict = {}
                    dataDict['title'] = title
                    dataDict['loupan'] = loupan
                    dataDict['houseType'] = houseType
                    dataDict['area'] = area
                    dataDict['toward'] = toward
                    dataDict['renovation'] = renovation
                    dataDict['positionInfo'] = positionInfo
                    dataDict['totalPrice'] = totalPrice
                    dataDict['unitPrice'] = unitPrice
                    dataDict['detailUrl'] = detailUrl
                    self.getDetail(dataDict)
                except Exception as e:
                    print(e)
                    continue

            time.sleep(3)

    def getDetail(self, dataDict):
        try:
            htmlStr = requests.get(dataDict['detailUrl'], headers=self.header).content
            soup = BeautifulSoup(htmlStr, 'lxml')
            # 挂牌日期
            dataDict['listingDate'] = soup.select('.introContent .transaction li span')[1]
            # 上次交易日期
            dataDict['lastTradingDate'] = soup.select('.introContent .transaction li span')[1]
            # 抓取时间
            dataDict['lastTradingDate'] = datetime.datetime.now()
            print(dataDict)
            print(dataDict['lastTradingDate'] )
        except Exception as e:
            print(e)


if __name__ == '__main__':
    CrwalerLianjia().getList()
