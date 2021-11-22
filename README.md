# fixed_assets1
固定资产管理系统
对IT设备进行管理，增加，修改，删除。分类查询显示，IT设备按类别分类，按所属部门分类，按存放位置分类。
使用方法：
安装依赖库 pip install -r requirements.txt -i https:pypi.douban.com/simple
改配置文件，新建一个数据库。
修改utils.email_serve的配置，用户忘记密码时，邮箱用来给用户发送密码，邮箱设置ACCOUNT，PASSWORD，HOST，PORT
生成数据库表
python run.py db init
python run.py db migrate
python run.py db upgrade
需要向数据库中的表手动添加几个数据
category:设备类别表，手动添加IT设备类别名称，如：电脑，打印机。
department:所属部门表，手动添加设备所属的部门名称和领导，如：（行政部，张三）。
location:存放位置表，手动添加设备存放位置名称，如：一楼大厅。
role:用户角色表，手动添加注册用户的角色，如：一般用户，管理员。

