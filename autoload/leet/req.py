import requests
import sqlite3

from . import   mycfg

import os

try:
    import vim
except ImportError:
    vim = None

class req():

    LC_BASE = ''
    LC_LOGIN = ''
    source = ''

    def __init__(self, source="leet"):
        self.source = source

        self.LC_BASE = mycfg.getConfig(source,"LC_BASE")
        self.LC_LOGIN= mycfg.getConfig(source,"LC_LOGIN")


    def get_curl(self):
        cookiepath = os.getenv('cookie_path')
        if cookiepath == None:
            cookiepath = '/home/prozhou/.mozilla/firefox/c0lpjfry.default-release/cookies.sqlite'

        if self.source == "leet":
            site = ".leetcode.com"
        else:
            site = ".leetcode-cn.com"

        session = requests.Session()
        cookie = self._getcookiefromchrome(site , cookiepath)
        session.cookies = requests.utils.add_dict_to_cookiejar(session.cookies, cookie)
        res = session.get(self.LC_LOGIN)
        if res.status_code != 200:
            return False
        return session


    def _getcookiefromchrome(self,host='.oschina.net',cookiepath='/data/www/cookie'):
        sql="select host,name,value from moz_cookies where host='%s'" % host
        with sqlite3.connect(cookiepath) as conn:
            cu=conn.cursor()
            cookies={name:value for host,name,value in cu.execute(sql).fetchall()}
        return cookies

    def make_headers(self, session):

        headers = {'Origin': self.LC_BASE,
             'Referer': self.LC_BASE,
             'X-CSRFToken': session.cookies['csrftoken'],
             'X-Requested-With': 'XMLHttpRequest'}
        return headers
