from bs4 import BeautifulSoup
import json
import re

class leetsubmit():
    session=""
    headers = ""
    LC_BASE = 'https://leetcode.com'
    LC_PROBLEM = LC_BASE + '/problems/{slug}/description'
    LC_SUBMISSIONS = LC_BASE + '/api/submissions/{slug}'
    LC_SUBMISSION = LC_BASE + '/submissions/detail/{submission}/'


    def __init__(self, session, headers):
        self.session= session
        self.headers = headers

    def get_submissions(self, slug):
        headers = self.headers
        headers['Referer'] = self.LC_PROBLEM.format(slug=slug)
        url = self.LC_SUBMISSIONS.format(slug=slug)
        res = self.session.get(url, headers=headers)
        if res.status_code != 200:
            return None
        submissions = []
        for r in res.json()['submissions_dump']:
            s = {
                'id': r['url'].split('/')[3],
                'time': r['time'].replace('\xa0', ' '),
                'status': r['status_display'],
                'runtime': r['runtime'],
            }
            submissions.append(s)
        return submissions
    def get_submission(self, sid):
        headers =  self.headers
        url = self.LC_SUBMISSION.format(submission=sid)
        res = self.session.get(url, headers=headers)
        if res.status_code != 200:
            return None

        # we need to parse the data from the Javascript snippet
        s = res.text
        submission = {
            'id': sid,
            'state': int(self._group1(re.search(r"status_code: parseInt\('([^']*)'", s),  'not found')),
            'runtime': self._group1(re.search("runtime: '([^']*)'", s), 'not found'),
            'passed': self._group1(re.search("total_correct : '([^']*)'", s), 'not found'),
            'total': self._group1(re.search("total_testcases : '([^']*)'", s), 'not found'),
            'testcase': self._split(self._unescape(self._group1(re.search("input : '([^']*)'", s), ''))),
            'answer': self._split(self._unescape(self._group1(re.search("code_output : '([^']*)'", s), ''))),
            'expected_answer': self._split(self._unescape(self._group1(re.search("expected_output : '([^']*)'", s),
                                                        ''))),
            'problem_id': self._group1(re.search("questionId: '([^']*)'", s), 'not found'),
            'slug': self._group1(re.search("editCodeUrl: '([^']*)'", s), '///').split('/')[2],
            'filetype': self._group1(re.search("getLangDisplay: '([^']*)'", s), 'not found'),
            'error': [],
            'stdout': [],
        }


        # the punctuations and newlines in the code are escaped like '\\u0010' ('\\' => real backslash)
        # to unscape the string, we do the trick '\\u0010'.encode().decode('unicode_escape') ==> '\n'
        submission['code'] = self._break_code_lines(self._unescape(self._group1(
            re.search("submissionCode: '([^']*)'", s), '')))

        dist_str = self._unescape(self._group1(re.search("runtimeDistributionFormatted: '([^']*)'", s),
                                     '{"distribution":[]}'))
        dist = json.loads(dist_str)['distribution']
        dist.reverse()

        # the second key "runtime" is the runtime in milliseconds
        # we need to search from the position after the first "runtime" key
        prev_runtime = re.search("runtime: '([^']*)'", s)
        if not prev_runtime:
            my_runtime = 0
        else:
            my_runtime = int(self._group1(re.search("runtime: '([^']*)'", s[prev_runtime.end():]), 0))

        accum = 0
        for runtime, frequency in dist:
            accum += frequency
            if my_runtime >= int(runtime):
                break

        submission['runtime_percentile'] = '{:.1f}%'.format(accum)
        return submission


    def _group1(self,match, default):
        if match:
            return match.group(1)
        return default


    def _unescape(self,s):
        return s.encode().decode('unicode_escape')

    def _split(self,s):
        # str.split has an disadvantage that ''.split('\n') results in [''], but what we want
        # is []. This small function returns [] if `s` is a blank string, that is, containing no
        # characters other than whitespaces.
        if s.strip() == '':
            return []
        return s.split('\n')


    def _break_code_lines(self,s):
        return s.replace('\r\n', '\n').replace('\xa0', ' ').split('\n')
