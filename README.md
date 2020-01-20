
##django 进行数据迁移命令
    python manage.py makemigrations  #根据app下的migrations目录中的记录，检测当前model层代码是否发生变化？
    python manage.py migrate         #把orm代码转换成sql语句去数据库执行
    python manage.py migrate --fake  #只记录变化，不提交数据库操作
	
	
##容器服务部署
	进入容器：nvidia-docker exec -it 279ffbd028c5 /bin/bash
	进入代码所在目录：cd /usr/share/auto_eoms/bin/server
	服务启动命令：(nohup python3 manage.py runserver 0.0.0.0:8888 > out.log &)