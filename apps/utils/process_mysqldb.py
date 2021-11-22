import datetime
import pymysql

connection = pymysql.connect(
    host="localhost", user="test", password="123456", database="fixed_assets")
cursor = connection.cursor()


for i in range(1, 101):
    for j in [8,9,10,11,12,13,14,15,16]:
        s = datetime.datetime.combine((datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day) +datetime.timedelta(days=i)),datetime.time(j,00))
        print(s,type(s))
        cursor.execute(
            "INSERT INTO `unloading_time`(`time`)VALUES('%s');" % (s))

connection.commit()
connection.close()
