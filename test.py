import time
import asyncio


# 定义异步函数
async def hello():
    time.sleep(1)
    print(2)


def run():
    loop.run_until_complete(hello())
    print(1)


loop = asyncio.get_event_loop()
if __name__ == '__main__':
    run()
