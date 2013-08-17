西窗烛
===

http://www.xichuangzhu.com

何当共剪西窗烛，却话巴山夜雨时。

部署：

1. 在MySQL数据库中新建数据库'xichuangzhu'，使用phpmyadmin导入xcz.sql
2. 使用pip（全局）安装依赖包：requests, Flask, Flask-WTF, WTForms, MySQL-python 
3. 创建配置文件：将config保存为/var/www/flaskconfig/xichuangzhu.config.py，并填充其中所有的缺失配置项
4. python run.py
