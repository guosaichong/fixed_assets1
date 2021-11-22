from datetime import datetime
import math


def get_months(datetype):
    """计算传入日期到现在的间隔月数
    datetype:datetime.date类型
    """
    dt=datetime.strptime(str(datetype),'%Y-%m-%d') 
    days=(datetime.now()-dt).days
    months=math.ceil(days/30)
    return months
