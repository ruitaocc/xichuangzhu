西窗烛
===

http://www.xichuangzhu.com

何当共剪西窗烛，却话巴山夜雨时。

部署：

1. 在MySQL中新建数据库'xcz'，使用phpmyadmin导入xcz.sql
2. sudo pip install -r requirements.txt（安装过程中任何问题都可google解决）
3. git clone整个项目文件夹到/var/www
4. 创建配置文件：将config另存为/var/www/flaskconfig/xichuangzhu.config.py，并填充其中的缺失配置项
5. 根据config.py中IMAGE_PATH建立同名同路径的文件夹，即/var/www/xcz_uploads/work_imgs/
6. python run.py
