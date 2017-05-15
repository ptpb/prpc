def rpc(func):
    func._rpc = True
    return func
