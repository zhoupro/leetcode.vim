from . import   mycfg

class leetsubmit():
    session=""
    headers = ""
    LC_BASE = ''
    LC_PROBLEM = ''
    LC_SUBMISSIONS =  ''
    LC_SUBMISSION =  ''
    LC_SUBMIT = ''


    def __init__(self, session, headers, source="leet"):
        self.session= session
        self.headers = headers

        self.LC_BASE = mycfg.getConfig(source,"LC_BASE")
        self.LC_PROBLEM= mycfg.getConfig(source,"LC_PROBLEM")
        self.LC_SUBMISSION= mycfg.getConfig(source,"LC_SUBMISSION")
        self.LC_SUBMISSIONS= mycfg.getConfig(source,"LC_SUBMISSIONS")
        self.LC_SUBMIT= mycfg.getConfig(source,"LC_SUBMIT")
        self.LC_GRAPHQL= mycfg.getConfig(source,"LC_GRAPHQL")

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
        return self.get_submit(sid)

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


    def submit_solution(self,slug, filetype, code=None, problem=None):
        if not problem:
            return None

        if code is None:
            return None

        code = self._remove_description(code)

        headers =  self.headers

        headers['Referer'] = self.LC_PROBLEM.format(slug=slug)
        body = {'data_input': problem['testcase'],
                'lang': filetype,
                'question_id': str(problem['id']),
                'test_mode': False,
                'typed_code': code,
                'judge_type': 'large'}
        url = self.LC_SUBMIT.format(slug=slug)
        res = self.session.post(url, json=body, headers=headers)
        if res.status_code != 200:
            return None
        return res.json()['submission_id']

    def _remove_description(self, code):
        eod = code.find('[End of Description]')
        if eod == -1:
            return code
        eol = code.find('\n', eod)
        if eol == -1:
            return ''
        return code[eol+1:]

    def get_submit(self,slug):
        headers = self.headers
        headers['Referer'] = self.LC_PROBLEM.format(slug=slug)
        body = {'query': '''query mySubmissionDetail($id: ID!) {
                  submissionDetail(submissionId: $id) {
                    id
                    code
                    runtime
                    memory
                    rawMemory
                    statusDisplay
                    timestamp
                    lang
                    isMine
                    passedTestCaseCnt
                    totalTestCaseCnt
                    sourceUrl
                    question {
                      titleSlug
                      title
                      translatedTitle
                      questionId
                      __typename
                    }
                    ... on GeneralSubmissionNode {
                      outputDetail {
                        codeOutput
                        expectedOutput
                        input
                        compileError
                        runtimeError
                        lastTestcase
                        __typename
                      }
                      __typename
                    }
                    submissionComment {
                      comment
                      flagType
                      __typename
                    }
                    __typename
                  }
                }''',
                'variables': {'id': slug},
                'operationName': 'mySubmissionDetail'}
        res = self.session.post(self.LC_GRAPHQL, json=body, headers=headers)
        if res.status_code != 200:
            return None

        q = res.json()['data']['submissionDetail']

        submission = {
            'id': q["id"],
            'code': q["code"].split("\n"),
            'passed':q["passedTestCaseCnt"],
            'total': q["totalTestCaseCnt"],
            'error': [],
            'stdout': [],
            'filetype': q["lang"],
            'testcase': q["outputDetail"]["lastTestcase"],
            'expected_answer': q["outputDetail"]["expectedOutput"],
            'answer': q["outputDetail"]["codeOutput"],
            'state': q["statusDisplay"],
            'runtime': q["runtime"],
            'problem_id': q["question"]["questionId"],
            'slug': q["question"]["titleSlug"]
        }

        return submission

