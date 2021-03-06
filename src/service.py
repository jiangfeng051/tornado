#date:2018/8/29

import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from config import settings

from src.Handler import login,index,logout,harbor

# class LoginHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.render('login.html')


# settings = {
#     'template_path': 'template',
#     'static_path': 'static',
#     'static_url_prefix': '/static/',
#     'cookie_secret' : "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
# }

application = tornado.web.Application([
    (r'/login',login.LoginHandler),
    (r'/index',index.IndexHandler),
    (r'/logout', logout.LogoutHandler),
    (r'/harbor',harbor.HarborHandler),
    (r'/listdeploy',index.ListDeployHandler),
    (r'/rollback',index.RollbackHandler),
],**settings.settings)


if __name__ == '__main__':
    application.listen(8081)
    tornado.ioloop.IOLoop.instance().start()

