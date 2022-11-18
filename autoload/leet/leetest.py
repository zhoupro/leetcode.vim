class leetest():
    session=""
    headers = ""
    LC_BASE = 'https://leetcode.cn'
    LC_PROBLEM = LC_BASE + '/problems/{slug}/description'
    LC_TEST = LC_BASE + '/problems/{slug}/interpret_solution/'

    def __init__(self, session, headers,source):
        self.session= session
        self.headers = headers
        _ = source

    def test_solution(self,problem_id, slug, filetype, code, test_input):
        code = self._remove_description(code)

        headers =  self.headers
        headers['Referer'] = self.LC_PROBLEM.format(slug=slug)
        body = {'data_input': test_input,
                'lang': filetype,
                'question_id': str(problem_id),
                'test_mode': False,
                'typed_code': code}
        url = self.LC_TEST.format(slug=slug)
        res = self.session.post(url, json=body, headers=headers)
        if res.status_code != 200:
            return None
        return res.json()['interpret_id']

    def _remove_description(self, code):
        eod = code.find('[End of Description]')
        if eod == -1:
            return code
        eol = code.find('\n', eod)
        if eol == -1:
            return ''
        return code[eol+1:]
