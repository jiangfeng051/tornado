#date:2018/8/28


#tornado配置
settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret' : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
}

#数据库配置
PY_MYSQL_CONN_DICT = {
    "host": '192.168.112.74',
    "port": 3306,
    "user": 'root',
    "passwd": 'zentech#123',
    "db": 'k8sharbor',
    "charset": 'utf8'
}