import requests
import aiohttp
import asyncio
import os
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
from tqdm import tqdm
import configparser
from threading import Thread
import time
import concurrent.futures as cf


class TianXianTV(object):
    # base_url = settings.BASE_URL
    # urls = [base_url.format(str(i).rjust(3, '0')) for i in range(0, 222)]
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.addHandler(logging.StreamHandler())
    current_path = os.path.abspath(__file__)
    cfg_base_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    logger.info('tianxian.py里的base_path:{}'.format(cfg_base_path))
    # base_path = settings.BASE_PATH
    path = ''
    # 设置浏览器请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"]=("Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36")

    def __init__(self):
        self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                # "Referer" : "",
        }
        self.dict_cookies = {}
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(self.cfg_base_path + '\\settings.cfg', encoding='utf-8')
        # self.section = self.config_parser.sections()
        # print('sections:{}'.format(self.section))
        self.base_url = self.config_parser.get('DOWNLOAD_URL', 'BASE_URL')
        self.base_path = self.config_parser.get('DOWNLOAD_PATH', 'BASE_PATH')

    def __del__(self):
        if self.__dict__.get('browser'):
            # print(self.__dict__)
            self.browser.delete_all_cookies()
            self.browser.close()

    def process_cookies(self, cookies):
        """
        处理Cookies
        :param cookies:
        :return:
        """
        for cookie in cookies:
            self.dict_cookies[cookie['name']] = cookie['value']
        return self.dict_cookies

    def get_info(self, url):
        self.browser = webdriver.PhantomJS(desired_capabilities=self.dcap)
        self.browser.get(url)
        cookies = self.browser.get_cookies()
        self.process_cookies(cookies)
        iframe = self.browser.find_elements_by_tag_name('iframe')[0]
        # print(iframe)
        self.browser.switch_to.frame(iframe)
        text_browser = self.browser.page_source
        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(text_browser)
        video_url = re.search('.*?video:\'(.*?)\'', text_browser, re.S).group(1)
        print('video_url:{}'.format(video_url))
        self.title = re.search('.*?<title>(.*?)</title>', text_browser, re.S).group(1)
        self.title = self.title.split()[0]
        assert self.title is not None, 'title为空。'
        print('title:{}'.format(self.title))
        self.path = self.base_path + r'\{}'.format(self.title)
        path_exist = os.path.exists(self.path)
        if not path_exist:
            os.mkdir(self.path)
        self.logger.info('当前视频文件的base路径：{}'.format(self.path))
        return video_url, self.title

    def get_m3u8_txt(self, url):
        response = requests.get(url, headers=self.headers, cookies=self.dict_cookies)
        # text = response.text.encode()
        text = response.text
        print('获得的m3u8文本的内容：{}'.format(text))
        result_m3u8 = re.search('.*?/(.*)\.', text, re.S).group(1) + '.m3u8'
        print('result_m3u8:{}'.format(result_m3u8))
        assert result_m3u8 is not None, 'result_m3u8为空。'
        ts_txt_url = self.base_url + result_m3u8
        response_ts = requests.get(url=ts_txt_url, headers=self.headers)
        response_content = response_ts.text
        with open(self.path + r'\index.m3u8', 'w') as f:
            # while True:
            #     chunk = response_content.read(1024)
            #     if not chunk:
            #         break
            f.write(response_content)
        return

    def get_ts_urls(self):
        self.logger.info('正在批量获取ts文件的url...')
        ts_urls = []
        index_path = self.path + r'\index.m3u8'
        print('index_path:{}'.format(index_path))
        with open(index_path) as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('/'):
                    line = re.search('^/(.*?)\.', line).group(1)
                    line += '.ts'
                    ts_urls.append(line)
        ts_urls = list(map(lambda x: self.base_url + x, ts_urls))
        print('获得的所有ts文件的urls:{}'.format('|'.join(ts_urls)))

        return ts_urls

    def get_threadpool(self, url, n):
        file_name = self.path + r'\{}.ts'.format(n)
        response = self.fetch_threadpool(url=url, file_name=file_name, headers=self.headers, cookies=self.dict_cookies)
        file_size = int(response.headers['content-length'])
        if os.path.exists(file_name):
            first_byte = os.path.getsize(file_name)
        else:
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        header_params = {'Range': f'bytes={first_byte}-{file_size}'}
        self.headers.update(header_params)
        print('当前的headers:{}'.format(self.headers))
        with tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=file_name) as pbar:
            self.fetch_threadpool(url, file_name, pbar=pbar, headers=self.headers)

    def fetch_threadpool(self, url, file_name, pbar=None, headers=None, **kwargs):
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        session = requests.session()
        session.keep_alive = False
        if headers.get('Range'):
            resp = session.get(url, headers=headers, **kwargs)
            print('下载ts文件的status_code:{}和reason:{}'.format(resp.status_code, resp.reason))
            with open(file_name, 'ab') as f:
                print('打开文件：')
                chunk = resp.content
                f.write(chunk)
        else:
            resp = session.get(url, **kwargs)
            return resp

    def get_files(self):
        self.logger.info('正在合并视频...')
        lists = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                first_name, last_name = os.path.splitext(file)
                if last_name == '.ts':
                    print('first_name:{}'.format(first_name))
                    lists.append(first_name)
        print("list:{}".format(lists))
        # lists_int = list(map(lambda x: int(x), lists)).sort()
        lists_int = list(map(lambda x: int(x), lists))
        lists_int.sort()
        # sorted(lists_int)
        print("list_int:{}".format(lists_int))
        return lists_int

    def get_mp4_lists(self, file_last_name='.mp4'):
        lists = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                first_name, last_name = os.path.splitext(file)
                if last_name == file_last_name:
                    lists.append(first_name)
        return lists

    def process_ts(self):
        #     shell_str = '|'.join(tmp)
        #     shell_str = 'ffmpeg -i \"concat:'+ shell_str + '\" -acodec copy -vcodec copy -absf aac_adtstoasc ' + filename
        #     os.system&#40;shell_str&#41;
        mp4_lists = self.get_mp4_lists('.mp4')
        new_name = len(mp4_lists) if mp4_lists else 0
        os.chdir(self.path)
        shell_str1 = '|'.join(['{}.ts'.format(i) for i in self.get_files()])
        print('shell_str1:{}'.format(shell_str1))
        shell_str2 = 'ffmpeg -i "concat:{}" -c copy {}-{}.mp4'.format(shell_str1, self.title, new_name)
        print('shell_str2:{}'.format(shell_str2))
        os.system(shell_str2)

    def start(self):
        new_loop = asyncio.new_event_loop()
        thread = Thread(target=self.start_new_thread, args=(new_loop,))
        thread.start()

    async def run_threadpool(self, url, n, loop):
        with cf.ThreadPoolExecutor(max_workers=10) as executor:  # 设置10个线程
            print('start: ', url)
            # loop = asyncio.get_event_loop()
            try:
                loop.run_in_executor(executor, self.get_threadpool, *[url, n])
            except Exception as e:
                print(e)
            print('end:', url)

    def start_new_thread(self, loop):
        video_url, title = self.get_info(url=self.config_parser.get('DOWNLOAD_URL', 'URL'))
        self.get_m3u8_txt(video_url)
        urls = self.get_ts_urls()
        # urls_lists = ['https://www.baidu.com', 'https://www.qq.com', 'https://weibo.com', 'https://weibo.cn']
        asyncio.set_event_loop(loop)
        tasks = [asyncio.ensure_future(self.run_threadpool(url=url, n=urls.index(url), loop=loop)) for url in urls]
        # loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    TianXiantv = TianXianTV()
    # TianXiantv.start()
    TianXiantv.start_new_thread()
    # video_url, title = TianXiantv.get_info(url=TianXiantv.config_parser.get('DOWNLOAD_URL', 'URL'))
    # TianXiantv.get_m3u8_txt(video_url)
    # urls = TianXiantv.get_ts_urls()
    # tasks = [asyncio.ensure_future(TianXiantv.get(url, urls.index(url))) for url in urls]
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait(tasks))
    # TianXiantv.process_ts()



