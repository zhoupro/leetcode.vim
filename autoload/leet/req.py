import requests
import sqlite3

import os

try:
    import vim
except ImportError:
    vim = None

class req():

    LC_BASE = 'https://leetcode.com'
    LC_LOGIN = LC_BASE + '/accounts/login/'

    def get_curl(self):
        cookiepath = os.getenv('cookie_path')
        session = requests.Session()
        cookie = self._getcookiefromchrome('.leetcode.com',cookiepath)
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
