# repository

> repository for ITSS



#### Views使用

##### 类通用试图

- [如何正确使用 CBVs (Class-based views)](http://www.weiguda.com/blog/11/)
- [Classy Class-Based Views](http://ccbv.co.uk/)
- [Class-based generic views 基于类的通用视图](http://django-14-tkliuxing.readthedocs.org/en/latest/topics/class-based-views.html)

#### OAuth2.0

- [Django实现简单OAuth2.0认证服务](http://bozpy.sinaapp.com/blog/27)



## 使用

### 安装依赖

    pip install -r requirements.txt

### 建立数据模型

    python3  manage.py syncdb

### 创建系统管理者（首次不用执行）

     python3 manage.py createsuperuser


### 重建索引 （如果实现了搜索功能）

    python manage.py rebuild_index


### 运行服务器

    python3 manage.py runserver 0.0.0.0:8000


### 实际部署需要将静态文件

    python manage.py collectstatic
