envPython为Python虚拟环境
如果不使用虚拟环境的话
在server.wsgi中需删去3行
不使用虚拟环境时建议通过which python确认当前所使用的解释器，防止解释错误（apache2报500code，error.log中提示为moudle not found）
xxq.conf需放置在/etc/apache2/sites-avavilable中
需安装libapache2-mod-wsgi-py3
方式为sudo apt install libapache2-mod-wsgi-py3
后看到提示wsgi is enabled后说明可以正常使用
否则请手动开启wsgi
sudo a2enable wsgi
