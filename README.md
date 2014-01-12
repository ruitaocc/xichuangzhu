西窗烛
===

http://www.xichuangzhu.com（域名备案中，请暂时访问：http://115.29.147.82/）

何当共剪西窗烛，却话巴山夜雨时。

Lovely build with Flask & Bootstrap3.

部署：

1. 在MySQL中新建数据库'xcz'，使用phpmyadmin导入xcz.sql
2. sudo apt-get install libmysqlclient-dev python-dev
3. git clone项目文件夹到/var/www
4. sudo pip install -r requirements.txt
5. 将xichuangzhu目录下的config文件另存为config./var/www/flaskconfig/xichuangzhu/config.py，并填充其中所有的缺失配置项
6. python run.py
