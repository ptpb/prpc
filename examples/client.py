from prpc.client import run_client


async def foo(client):
    res = await client.call('__main__.foo', 'arg1', foo='bar')
    print('got', res)


run_client(foo, host='::1', port=12345)
