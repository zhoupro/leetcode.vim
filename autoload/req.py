import importlib
class req():
    arg = "leet"
    def __init__(self, arg):
        self.arg = arg

    def __call__(self, arg):
        print(arg)

    def get_curl(self, source):
        req = self._get_req_imp()
        return req.req().get_curl(source)

    def make_headers(self, session):
        req = self._get_req_imp()
        return req.req().make_headers(session)



    def _get_req_imp(self):
        importClass = self.arg+"."+"req"
        req=importlib.import_module(importClass)
        return req

if __name__ == "__main__":
    x = req("leet");
    session = x.get_curl()
    print(x.make_headers(session))
