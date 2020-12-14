from bs4 import BeautifulSoup

import requests
import time


class CrwalerLianjia():
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.109 Safari/537.36'}
        self.url = 'https://sh.lianjia.com/ershoufang/putuo/pg{0}p1p2/'
        'https://sh.lianjia.com/ershoufang/putuo/pg2dp1l2p1p2/'



    def getList(self):
        for i in range(1, 101):
            print(i)
            htmlStr = requests.get(self.url.format(i), headers=self.header).content
            soup = BeautifulSoup(htmlStr, 'lxml')
            sellListContent = soup.select('.sellListContent li.LOGCLICKDATA')
            for sell in sellListContent:
                try:
                    # 标题
                    title = sell.select('div.title a')[0].string
                    # 先抓取全部的div信息，再针对每一条进行提取
                    houseInfo = list(sell.select('div.houseInfo')[0].stripped_strings)
                    # 楼盘名字
                    loupan = houseInfo[0]
                    # 对楼盘的信息进行分割
                    info = houseInfo[0].split('|')
                    # 房子类型
                    house_type = info[1].strip()
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
                    data_dict = {}
                    data_dict['title'] = title
                    data_dict['loupan'] = loupan
                    data_dict['house_type'] = house_type
                    data_dict['area'] = area
                    data_dict['toward'] = toward
                    data_dict['renovation'] = renovation
                    data_dict['positionInfo'] = positionInfo
                    data_dict['totalPrice'] = totalPrice
                    data_dict['unitPrice'] = unitPrice

                    print(data_dict)
                except Exception as e:
                    print(e)
                    continue

            time.sleep(3)

    def getDetail(self):
        pass


if __name__ == '__main__':
    CrwalerLianjia().getList()
