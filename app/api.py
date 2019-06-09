#!/usr/bin/python
# coding=utf-8
import os
import base64
import requests
from time import sleep

from flask import (
    Blueprint, request, make_response, jsonify
)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

bp = Blueprint('api', __name__, url_prefix='/api')

# 初始化选项
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--no-sandbox')  # 禁用 sandbox
chrome_options.add_argument('--disable-gpu')  # 禁用 gpu 渲染


# 图片临时文件地址
SCREENSHOTS_DIR = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'screenshots')
# 最多保存多少张图片文件
MAX_IMAGES_NUMBER = 100


def generate_response(message='OK', status=200, **kwargs):
    json = {
        'message': message
    }
    for key in kwargs:
        json[key] = kwargs[key]
    return make_response(jsonify(json), status)


# from: https://cloud.tencent.com/developer/article/1406655
def generate_base64(path):
    file = open(path, 'rb')
    base64_image = base64.b64encode(file.read())
    file.close()
    return base64_image


def generate_image_name(screenshot_url):
    return str(hash(screenshot_url)) + '.png'


def generate_image_full_path(screenshot_url=None, image_name=None):
    if image_name is None:
        if screenshot_url is None:
            raise ValueError('缺少参数，image_name 和 screenshot_url 至少需要一个')
        else:
            image_name = generate_image_name(screenshot_url=screenshot_url)
    image_full_path = os.path.join(SCREENSHOTS_DIR, image_name)
    return image_full_path


def generate_formatted_url(url):
    url = str(url).strip()
    if url.startswith('http') is True:
        return url
    else:
        return 'http://' + url


def clear_extra_images():
    screenshots = [
        os.path.join(SCREENSHOTS_DIR, screenshot) for screenshot in os.listdir(SCREENSHOTS_DIR)
    ]
    screenshots_number = len(screenshots)
    if screenshots_number > MAX_IMAGES_NUMBER:
        # 按照最后修改时间进行排序
        screenshots.sort(lambda a, b: int(os.path.getmtime(a) -
                                          os.path.getmtime(b)))
        for i in range(screenshots_number - MAX_IMAGES_NUMBER):
            os.remove(screenshots[i])


@bp.route('screenshot', methods=['GET', 'POST'])
def screenshot():
    if request.method == 'POST':
        screenshot_url = generate_formatted_url(
            request.form.get('screenshot_url'))
        callback_url = generate_formatted_url(request.form.get('callback_url'))
        if screenshot_url is None:
            return generate_response(message='缺少截图地址', status=400)
        elif callback_url is None:
            return generate_response(message='缺少回调地址', status=400)
        else:
            # 发起请求并进行截图，保存到本地
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.maximize_window()
            browser.get(screenshot_url)
            image_name = generate_image_name(screenshot_url=screenshot_url)
            image_full_path = generate_image_full_path(image_name=image_name)
            browser.save_screenshot(image_full_path)
            browser.close()

            clear_extra_images()

            # 读取截图生层 base64
            base64_image = generate_base64(image_full_path)
            requests.post(callback_url, data={
                'base64_image': base64_image
            })
            return generate_response(
                screenshot_url=screenshot_url,
                callback_url=callback_url,
                image_name=image_name,
            )
    elif request.method == 'GET':
        screenshot_url = generate_formatted_url(request.args.get(
            'screenshot_url'))
        image_full_path = generate_image_full_path(
            screenshot_url=screenshot_url)
        if os.path.exists(image_full_path):
            base64_image = generate_base64(image_full_path)
            return generate_response(
                screenshot_url=screenshot_url,
                base64_image=base64_image
            )
        else:
            return generate_response(message='该页面未进行过截图')


@bp.route('screenshot_callback', methods=['POST'])
def screenshot_callback():
    base64_image = request.form.get('base64_image', '')
    print base64_image
    return generate_response(
        base64_image=base64_image
    )
