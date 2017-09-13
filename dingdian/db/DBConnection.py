import pymysql
from dingdian.items import DingdianItem
config = {
        'host':'127.0.0.1',
        'port':3306,
        'user':'root',
        'password':'',
         'db':'media',
        'charset':'utf8mb4',
        #cursor类型默认获取数据是元组
        'cursorclass':pymysql.cursors.DictCursor,
}


db = pymysql.connect(**config)
cursor = db.cursor()
area_id = 52
cursor.execute('select * from t_area where area_id = %s', area_id)
data = cursor.fetchall()
for area in data:
        print(area)
        print(area['area_name'])
print('data:', data)


class MySqlDB:
        def __init__(self):
                self.dbargs = dict({
                'host':'127.0.0.1',
                'port':3306,
                'user':'root',
                'password':'',
                 'db':'media',
                'charset':'utf8mb4',
                #cursor类型默认获取数据是元组
                'cursorclass':pymysql.cursors.DictCursor,
                })

        def get_conn(self):
                return pymysql.connect(**self.dbargs)

        def save_item(self, item):
                conn = self.get_conn()
                cursor = conn.cursor()

                sql = 'insert into t_novel (name, novel_url, status, serial_number, category) values  \
                        (%s, %s, %s, %s, %s)'
                try:
                        cursor.execute(sql, (item['name'], item['novel_url'], item['status'], item['serial_number'], item['category']))
                        print(sql)
                        conn.commit()
                except Exception as e:
                        print(e)
                        conn.rollback()
                cursor.close()
                cursor.close()

db = MySqlDB()
novel = DingdianItem()
novel['name'] = 'test'
novel['novel_url'] = 'www.baidu.com'
novel['status'] = 0
novel['serial_number'] = 22
novel['category'] = '玄幻'

print(novel)
db.save_item(novel)




