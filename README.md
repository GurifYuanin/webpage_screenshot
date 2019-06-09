# 网页截图服务

## 简介
用于进行网页截图，生成 Data URI 返回。

## 快速开始

+ 下载 chrome 浏览器
+ 下载 chrome driver，下载地址：[http://npm.taobao.org/mirrors/chromedriver/](http://npm.taobao.org/mirrors/chromedriver/)
+ 将 chrome driver 加入到 PATH
+ 启动项目
```shell
# 安装并进入 virtualenv
$ pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
# 安装依赖模块
$ pip install -e .
# 初始化数据库
$ flask init-db
# 开发
$ FLASK_ENV=development flask run
# 启动服务器
$ waitress-serve --port=8084 --call 'app:create_app'
```