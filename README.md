西窗烛
===

http://www.xichuangzhu.com

何当共剪西窗烛，却话巴山夜雨时。

部署：

1. 在MySQL数据库中新建数据库'xcz'，使用phpmyadmin导入xcz.sql
2. 使用pip（全局）安装requirements.txt中所列的package(requests, Flask, Flask-WTF, MySQL-python, flask-debugtoolbar, Flask-SQLAlchemy)
3. git clone整个项目文件夹到/var/www下，并运行git checkout sqla切换到sqla分支
4. 创建配置文件：将config另存为/var/www/flaskconfig/xichuangzhu.config.py，并填充其中所有的缺失配置项
5. 根据config.py中IMAGE_PATH建立同名同路径的文件夹（即：/var/www/xcz_uploads/work_imgs/）
6. python run.py
