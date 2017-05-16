from prpc.client import ClientFactory

client = ClientFactory().connect('localhost', 12345)
client.cast('__main__.foo', 'arg1', foo='bar')
