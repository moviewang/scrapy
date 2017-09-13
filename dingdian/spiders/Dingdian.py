import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from dingdian.items import DingdianItem
from  dingdian.db.DBConnection import MySqlDB

class MySpider(scrapy.Spider):
    name = 'dingdian'
    allowed_domain = ['x23us']
    bash_url = 'http://www.x23us.com/class/'
    bash_suffix = '.html'
    ca = {
        1 : '玄幻魔法',
        2 : '武侠修真',
        3 : '都市言情',
        4 : '历史军事',
        5 : '侦探推理',
        6 : '网游动漫',
        7 : '科幻小说',
        8 : '恐怖灵异',
        9 : '散文诗词',
        10 : '其他',
    }

    def start_requests(self):
        for i in range(1, 11):
            url = self.bash_url + str(i) + '_1' + self.bash_suffix
            yield Request(url, self.parse)

    def parse(self, response):
        print('reponse text:', response.text)
        max_num = BeautifulSoup(response.text, 'lxml').find('div', class_='pagelink').find_all('a')[-1].get_text()
        print('max_num:', max_num)
        print('response url：', response.url)
        bash_url = str(response.url)[:-7]
        print('bash_url:', bash_url)
        for num in range(1, int(max_num) + 1):
            url = bash_url + '_' + str(num) + self.bash_suffix
            yield Request(url, callback=self.get_name)

    def get_name(self, response):
        print('get_name url:', response.url)
        cid = str(response.url)[:-7]
        c_id = cid[cid.rfind('/') + 1 : cid.rfind('_')]
        print('cid:', c_id)
        trs = BeautifulSoup(response.text, 'lxml').find_all('tr', bgcolor='#FFFFFF')
        print('trs:',trs)
        db = MySqlDB()
        for tr in trs:
            novel_name = tr.find('a', target="_blank").get_text()
            novel_url = tr.find('a')['href']
            author = tr.find_all('td')[2].get_text()
            status = tr.find_all('td')[-1].get_text()
            serial_number = tr.find_all('td')[-3].get_text()
            print('novel_name:', novel_name)
            print('novel_url:', novel_url)
            print('author:', author)
            print('status:', status)
            print('serial_number:', serial_number)
            print('category:', self.ca[int(c_id)])

            '''data persis'''
            novel = DingdianItem()
            novel['name'] = novel_name
            novel['novel_url'] = novel_url
            novel['status'] = status
            novel['serial_number'] = serial_number
            novel['category'] = self.ca[int(c_id)]

            print(novel)
            db.save_item(novel)

