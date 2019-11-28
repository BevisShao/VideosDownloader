#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import asyncio
import aiohttp
import time


async def do_work(n):
    sem = asyncio.Semaphore(5, loop=loop)
    print('do_work(%s)' % n)
    async with sem:
        # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False, keepalive_timeout=5,)) as session:
        #     res = await session.get(url='https://www.baidu.com')
        #     print('第{}次请求，响应码：{}'.format(n, res.status))
        print('==========={}======== {}'.format(n, sem._value))
        await asyncio.sleep(3)
        print('第{}次请求，'.format(n))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(do_work(i)) for i in range(1000)]
    loop.run_until_complete(asyncio.wait(tasks))
