import datetime
import pymysql

connection = pymysql.connect(
    host="localhost", user="test", password="123456", database="fixed_assets")
cursor = connection.cursor()

# 生成一号库用的卸货时间
# for i in range(1, 101):
#     for j in [8,9,10,11,12,13,14,15,16]:
#         s = datetime.datetime.combine((datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day) +datetime.timedelta(days=i)),datetime.time(j,00))
#         print(s,type(s))
#         cursor.execute(
#             "INSERT INTO `unloading_time`(`time`)VALUES('%s');" % (s))

# 生成二号库用的卸货时间
for i in range(1, 101):
    for j in ["08:00","08:40","9:20","10:00","10:40","11:20","12:00","12:40","13:20","14:00","14:40","15:20","16:00"]:
        s = datetime.datetime.combine((datetime.date(datetime.datetime.now().year,datetime.datetime.now().month,datetime.datetime.now().day) +datetime.timedelta(days=i)),datetime.time(int(j[:2]),int(j[3:5])))
        print(s,type(s))
        cursor.execute(
            "INSERT INTO `unloading_time2`(`time`)VALUES('%s');" % (s))

connection.commit()
connection.close()
