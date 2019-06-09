# 网页截图服务

## 简介
用于进行网页截图，生成图片 base64 Data URI 后发送给回调地址。

## 快速开始

+ 下载 chrome 浏览器
+ 下载 chrome driver，下载地址：[http://npm.taobao.org/mirrors/chromedriver/](http://npm.taobao.org/mirrors/chromedriver/)
+ 将 chrome driver 加入到 PATH
+ 启动项目
```shell
# 安装并进入 virtualenv
$ git clone git@github.com:GurifYuanin/webpage_screenshot.git
$ cd webpage_screenshot
$ pip install virtualenv
$ virtualenv venv
$ . venv/bin/activate
# 安装依赖模块
$ pip install -e .
# 初始化数据库
$ flask init-db
# 本地开发，http://localhost:5000
$ FLASK_ENV=development flask run
# 启动服务器，http://0.0.0.0:8084
$ waitress-serve --port=8084 --call 'app:create_app'
```

### 路由

#### 创建截图
路径：/api/screenshot
方法：POST
+ param {string} screenshot_url 截图地址
+ param {string} callback_url 回调地址
+ return {object} 返回内容
```python
{
  "callback_url": string,
  "screenshot_url": string,
  "image_name": string,
  "message": string
}
```
截图成功后，将向`callback_url`发起一次 HTTP POST 请求，请求参数为：
```python
{
  "base64_image": string
}
```

#### 获得截图
路径：/api/screenshot
方法：GET
+ param {string} screenshot_url 截图地址
+ return {object} 返回内容
```python
{
  "screenshot_url": string,
  "base64_image": string,
  "message": string
}
```