import requests

from requests import utils
import browser_cookie3
from . import   mycfg

class req():

    LC_BASE = ''
    LC_LOGIN = ''
    source = ''


    def get_curl(self, source="leet"):

        self.source = source

        self.LC_BASE = mycfg.getConfig(source,"LC_BASE")
        self.LC_LOGIN= mycfg.getConfig(source,"LC_LOGIN")

        session = requests.Session()
        cj = browser_cookie3.load()
        dt = utils.dict_from_cookiejar(cj)
        session.cookies = utils.add_dict_to_cookiejar(session.cookies, dt)
        res = session.get(self.LC_LOGIN)
        if res.status_code != 200:
            return False
        return session


    def make_headers(self, session):

        headers = {'Origin': self.LC_BASE,
             'Referer': self.LC_BASE,
             'X-CSRFToken': session.cookies['csrftoken'],
             'X-Requested-With': 'XMLHttpRequest'}
        return headers
