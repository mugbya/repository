# repository

> repository for ITSS


#### OAuth2.0

- [Django实现简单OAuth2.0认证服务](http://bozpy.sinaapp.com/blog/27)



## 使用

### 安装依赖

    pip install -r requirements.txt

### 建立数据模型

version 1.8

    python3  manage.py syncdb

version 1.9

    python3 manage.py makemigrations app
    python3 manage.py migrate


### 创建系统管理者（首次不用执行）

     python3 manage.py createsuperuser


### 重建索引 （如果实现了搜索功能）

    python manage.py rebuild_index


### 运行服务器

    python3 manage.py runserver 0.0.0.0:8000


### 实际部署需要将静态文件

    python manage.py collectstatic
