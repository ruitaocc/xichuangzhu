西窗烛
===

http://www.xichuangzhu.com

何当共剪西窗烛，却话巴山夜雨时。
<small>——李商隐《夜雨寄北》</small>

部署方法：

（1）在MySQL数据库中新建数据库'xichuangzhu'，使用phpmyadmin导入xcz.sql
（2）使用pip（全局）安装依赖包：requests, Flask-WTF, WTForms, MySQL-python, markdown2 
（3）创建配置文件：将config.py复制到/var/www/flaskconfig/xichuangzhu.config.py，并修改其中的配置项
（4）使用Gunicorn部署即可
