import asyncio

from prpc.client import ClientFactory


client = ClientFactory().connect('localhost', 12345)
client.cast('__main__.foo', 'arg1', foo='bar')


async def do_call():
    res = await client.call('__main__.foo', 'arg1', foo='bar')
    print('got res', res)


loop = asyncio.get_event_loop()
loop.run_until_complete(do_call())
