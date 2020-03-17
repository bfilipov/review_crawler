import asyncio
from proxybroker import Broker

proxy_list = []


async def show(proxies):
    count = 0
    while True:
        proxy = await proxies.get()
        if proxy is None:
            break
        proxy_list.append(f'{proxy.host}:{proxy.port}')
        count += 1
        if count % 10 == 0:
            print(f'Found {count} proxies.')

proxies = asyncio.Queue()
broker = Broker(proxies)
tasks = asyncio.gather(
    broker.find(types=['HTTP', 'HTTPS'], limit=300),
    show(proxies))

loop = asyncio.get_event_loop()
loop.run_until_complete(tasks)
with open('proxies', 'w') as f:
    [f.write("%s\n" % item) for item in proxy_list]
